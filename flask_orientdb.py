from pyorient import OrientDB as OrientDBPy
import pyorient
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack
from collections import namedtuple


def db_create(name, type, memory):
    if type == 'graph':
        db_type = pyorient.DB_TYPE_GRAPH
    elif type == 'document':
        db_type =pyorient.DB_TYPE_DOCUMENT
    else:
        raise Exception('invalid argument provided to create_db()')
    if memory == 'local':
        memory_location = pyorient.STORAGE_TYPE_LOCAL
    elif memory == 'plocal':
        memory_location  = pyorient.STORAGE_TYPE_PLOCAL
    elif memory == 'memory':
        memory_location = pyorient.STORAGE_TYPE_MEMORY
    else:
        raise Exception('invalid argument provided to createdb()')
    return name, db_type, memory_location


def data_cluster_add(cluster_name, type):
    if type == 'physical':
        cluster_type = pyorient.CLUSTER_TYPE_PHYSICAL
    elif type == 'memory':
        cluster_type = pyorient.CLUSTER_TYPE_MEMORY
    return cluster_name, cluster_type


class OrientDB(object):
    def __init__(self, app=None, server_un='root', server_pw=None, host='localhost', port=2424):
        self.Database = namedtuple('Database', 'db_name, db_username, db_password')
        if app is not None:
            self.init_app(app, server_un=server_un, server_pw=server_pw, host=host, port=port)
        else:
            self.app = None

    def init_app(self, app, server_pw, server_un='root', host='localhost', port=2424):
        """
        Sets up configuration and adds teardown methods to Flask.
        """
        if not app:
            raise Exception('pass in a flask app')
        self.app = app
        self.app.config.setdefault('ORIENTDB_AUTO_OPEN', True)
        self.app.config.setdefault('ORIENTDB_SERVER_PASSWORD', server_pw)
        self.app.config.setdefault('ORIENTDB_SERVER_USERNAME', server_un)
        self.app.config.setdefault('ORIENTDB_HOST', host)
        self.app.config.setdefault('ORIENTDB_PORT', port)
        self.app.config.setdefault('ORIENTDB_DB', None)
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise faargsll back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self._teardown)
        else:
            app.teardown_request(self._teardown)
        # register extension with app
        if 'orientdb' not in app.extensions:
            app.extensions['orientdb'] = self

    @property
    def connection(self):
        ctx = stack.top
        if hasattr(ctx, 'orientdb_client'):
            return ctx.orientdb_client

    def create_client(self):
        ctx = stack.top
        ctx.orientdb_client = OrientDBPy(self.app.config.get('ORIENTDB_HOST'), self.app.config.get('ORIENTDB_PORT'))

    def set_db(self, db_name, db_username='admin', db_password='admin'):
        self.app.config['ORIENTDB_DB'] = self.Database(db_name, db_username, db_password)

    def _connect_to_db(self):
        if self.connection:
            return self.connection.db_open(self.app.config.get('ORIENTDB_DB').db_name, self.app.config.get('ORIENTDB_DB').db_username,
                                           self.app.config.get('ORIENTDB_DB').db_password)
        else:
            raise Exception("tried to connect to db without client. Use set_current_db")

    def _teardown(self, *args):
        """Close the connection to current OrientDB database."""
        if self.connection:
            self.connection.db_close()
            ctx = stack.top
            del ctx.orientdb_client

    def __getattr__(self, name, *args, **kwargs):
        ctx = stack.top
        if not ctx:
            raise Exception('No context available, call within a view function')
        if not self.connection:
            self.create_client()
        # create new session id if it does not exist
        if self.connection._connection.session_id == -1:
            self.create_client()
            ctx.orientdb_client.connect(self.app.config.get('ORIENTDB_SERVER_USERNAME'), self.app.config.get('ORIENTDB_SERVER_PASSWORD'))
        # method names that need a database connection opened
        connection_needed = ['db_size', 'db_count_records', 'command', 'query', 'data_cluster_add',
                             'data_cluster_drop', 'data_cluster_count', 'data_cluster_data_range',
                             'record_create', 'record_load', 'record_update', 'batch', 'db_reload']
        if name in connection_needed and self.app.config.get('ORIENTDB_AUTO_OPEN'):
            self._connect_to_db()
        elif name in connection_needed:
            raise Exception(
                'Error either ORIENTDB_DB is not configured or ORIENTDB_AUTO_OPEN is set to False')

        def wrapper(*args, **kw):
            if name == 'db_create':
                args = db_create(args[0], args[1], args[2])
            if name == 'data_cluster_add':
                args = data_cluster_add(args[0], args[1])
            return getattr(ctx.orientdb_client, name)(*args, **kw)
        return wrapper