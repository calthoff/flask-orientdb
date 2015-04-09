from pyorient import OrientDB as OrientDBPy
import pyorient
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack
from collections import namedtuple


def db_create(name, type , memory):
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
        self.database_list = []
        self.current_database = None
        if app is not None:
            self.app = app
            self.init_app(self.app, server_un=server_un, server_pw=server_pw, host=host, port=port)
        else:
            self.app = None

    def init_app(self, app, server_pw, server_un='root', host='localhost', port=2424):
        """
        Sets up configuration and adds teardown methods to Flask.
        """
        self.app = app
        # if database_name:
        #     self.current_database = self.register_db(database_name, database_username, database_password)
        self.app.config.setdefault('ORIENTDB_AUTO_OPEN', True)
        self.app.config.setdefault('ORIENTDB_SERVER_PASSWORD', server_pw)
        self.app.config.setdefault('ORIENTDB_SERVER_USERNAME', server_un)
        self.app.config.setdefault('ORIENTDB_HOST', host)
        self.app.config.setdefault('ORIENTDB_PORT', port)
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise faargsll back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self._teardown)
        else:
            app.teardown_request(self._teardown)
        # register extension with app
        # TODO is first part necessary
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['orientdb'] = self
        self._create_client()
        self._connect_to_server()

    def _create_client(self):
        ctx = stack.top
        if not hasattr(ctx, 'orientdb_client'):
            ctx.orientdb_client = OrientDBPy(self.app.config.get('ORIENTDB_HOST'),
                                             self.app.config.get('ORIENTDB_PORT'))
            return ctx.orientdb_client

    def _connect_to_server(self):
        ctx = stack.top
        if not hasattr(ctx, 'orientdb_session_id'):
            ctx.orientdb_session_id = ctx.orientdb_client.connect(self.app.config.get('ORIENTDB_SERVER_USERNAME'),
                                                                  self.app.config.get('ORIENTDB_SERVER_PASSWORD'))
            return ctx.orientdb_session_id

    def _connect_to_db(self):
        ctx = stack.top
        if not hasattr(ctx, 'orientdb_db_connection'):
            ctx.orientdb_db_connection = ctx.orientdb_client.db_open(self.current_database.db_name,
                                                                 self.current_database.db_username,
                                                                 self.current_database.db_password)
            return ctx.orientdb_db_connection

    def _teardown(self):
        """Close the connection to current OrientDB database."""
        ctx = stack.top
        if hasattr(ctx, 'orientdb_db_connection'):
            ctx.orientdb_client.db_close()
            del ctx.orientdb_db_connection

    def _shutdown(self):
        pass

    def _register_db(self, db_name, db_username, db_password):
        if db_username == None:
            db_username = 'admin'
        if db_password == None:
            db_password = 'admin'
        Database = namedtuple('Database', 'db_name, db_username, db_password')
        new_db = Database(db_name, db_username, db_password)
        self.database_list.append(new_db)
        return new_db

    def set_current_db(self, db_name, db_username=None, db_password=None):
        if not db_username:
            for named_db_tuple in self.database_list:
                if named_db_tuple.db_name == db_name:
                    self.current_database = named_db_tuple
                    return
        self._register_db(db_name, db_username, db_password)
        self.set_current_db(db_name)

    @property
    def client_connected(self):
        ctx = stack.top
        return getattr(ctx, 'orientdb_client', None) is not None

    @property
    def server_connected(self):
        """Returns OrientDB server connection status."""
        ctx = stack.top
        return getattr(ctx, 'orientdb_session_ids', None) is not None

    @property
    def db_connected(self):
        ctx = stack.top
        return getattr(ctx, 'orientdb_db_connection', None) is not None

    def __getattr__(self, name, *args, **kwargs):
        ctx = stack.top
        # TODO look for better way to do this maybe within pyorient
        connection_needed = ['db_size', 'db_count_records', 'command', 'query', 'data_cluster_add']
        if name in connection_needed and self.app.config.get('ORIENTDB_AUTO_OPEN'):
            if self.current_database and not hasattr(ctx, 'orientdb_db_connection'):
                self._connect_to_db()
        elif name in connection_needed:
            raise Exception(
                'Error either ORIENTDB_CURRENT_DATABASE is not configured or ORIENTDB_AUTO_OPEN is set to False')

        def wrapper(*args, **kw):
            if name == 'db_create':
                args = db_create(args[0], args[1], args[2])
            if name == 'data_cluster_add':
                args = data_cluster_add(args[0], args[1])
            if name == 'db_close':
                # TODO review this
                    self._teardown()
            if name == 'db_drop':
                # TODO why is this necessary
                del ctx.orientdb_session_id
                self._connect_to_server()
            return getattr(ctx.orientdb_client, name)(*args, **kw)
        return wrapper