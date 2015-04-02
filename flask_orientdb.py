from pyorient import OrientDB as OrientDBPy
import pyorient
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack
from collections import namedtuple
# TODO check what pyorient.STORAGE_TYPE_MEMORY does


def createdb_args(name, args):
    if args[1] == 'graph':
        # args = (args[0], pyorient.DB_TYPE_GRAPH)
        db_type = pyorient.DB_TYPE_GRAPH
    elif args[1] == 'document':
        # args = (args[0], pyorient.DB_TYPE_DOCUMENT)
        db_type =pyorient.DB_TYPE_DOCUMENT
    else:
        raise Exception('invalid argument provided to create_db()')
    if args[2] == 'local':
        memory_location = pyorient.STORAGE_TYPE_LOCAL
    elif args[2] == 'plocal':
        memory_location  = pyorient.STORAGE_TYPE_PLOCAL
    elif args[2] == 'memory':
        memory_location = pyorient.STORAGE_TYPE_MEMORY
    else:
        raise Exception('invalid argument provided to createdb()')
    return (name, db_type, memory_location)

class OrientDB(object):
    def __init__(self, app=None, database_name=None, database_username='admin', database_password='admin',
                 server_password=None, server_username='root', host='localhost', port=2424):
        self.database_list = []
        self.current_database = None
        if app is not None:
            self.app = app
            self.init_app(self.app, database_name=database_name, database_username=database_username,
                          database_password=database_password, server_password=server_password,
                          server_username=server_username, host=host, port=port)
        else:
            self.app = None

    def init_app(self, app, database_name=None, database_username="admin", database_password="admin",
                 server_password=None, server_username='root', host='localhost', port=2424):
        """
        Sets up configuration and adds teardown methods to Flask.
        """
        self.app = app
        if database_name:
            self.current_database = self.register_db(database_name, database_username, database_password)
        self.app.config.setdefault('ORIENTDB_AUTO_OPEN', True)
        self.app.config.setdefault('ORIENTDB_SERVER_PASSWORD', server_password)
        self.app.config.setdefault('ORIENTDB_SERVER_USERNAME', server_username)
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

    def _create_client(self):
        ctx = stack
        # TODO figure out how to use ctx.top
        if not self.client_connected:
            ctx.orientdb_client = OrientDBPy(self.app.config.get('ORIENTDB_HOST'),
                                             self.app.config.get('ORIENTDB_PORT'))
        return ctx.orientdb_client

    def _connect_to_server(self):
        ctx = stack
        #if not self.server_connected:
        ctx.orientdb_session_id = ctx.orientdb_client.connect(self.app.config.get('ORIENTDB_SERVER_USERNAME'),
                                                                  self.app.config.get('ORIENTDB_SERVER_PASSWORD'))
        return ctx.orientdb_session_id

    def _connect_to_db(self):
        ctx = stack
        ctx.orientdb_db_connection = ctx.orientdb_client.db_open(self.current_database.db_name,
                                                                 self.current_database.db_username,
                                                                 self.current_database.db_password)
        # TODO why is this necessary
        self._connect_to_server()
        return ctx.orientdb_db_connection

    def _teardown(self):
        """Close the connection to current OrientDB database."""
        ctx = stack
        # if hasattr(ctx, 'orientdb_client') and hasattr(ctx, 'orientdb_db_connection'):
        # ctx.orientdb_client.db_close()
        #     del ctx.orientdb_db_connection

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
        ctx = stack
        return getattr(ctx, 'orientdb_client', None) is not None

    @property
    def server_connected(self):
        """Returns OrientDB server connection status."""
        ctx = stack
        return getattr(ctx, 'orientdb_session_id', None) is not None

    @property
    def database_connected(self):
        ctx = stack
        return getattr(ctx, 'orientdb_db_connection', None) is not None

    def __getattr__(self, name, *args, **kwargs):
        # TODO figure out how to use ctx.top
        ctx = stack
        if not self.client_connected:
            self._create_client()
        self._connect_to_server()
        connection_needed = ['db_size', 'db_count_records', 'command']
        # TODO why do I need to connect to server each time
        self._connect_to_server()
        # create database connection if needed
        if name in connection_needed and self.app.config.get('ORIENTDB_AUTO_OPEN') and self.current_database:
            self._connect_to_db()
        elif name in connection_needed:
            raise Exception(
                'Error either ORIENTDB_CURRENT_DATABASE is not configured or ORIENTDB_AUTO_OPEN is set to False')

        def wrapper(*args, **kw):
            # TODO database create already exists corrupts db
            if name == 'db_create':
                if len(args) < 2:
                    raise Exception("Must provide 2 arguments")
                args = createdb_args(args[0], args)
            # if name == 'db_open':
            #     # TODO check order username, password
            #     args = (args[0], self.current_database.db_username, self.current_database.db_password)
            if name == 'db_close':
                del ctx.orientdb_client
                del ctx.orientdb_session_id
                # TODO???
                return
            return getattr(ctx.orientdb_client, name)(*args, **kw)
        return wrapper