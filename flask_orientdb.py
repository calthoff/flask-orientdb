from pyorient import OrientDB as OrientDBPy
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack
import pyorient


class OrientDB(object):
    def __init__(self, app=None, database_name=None, database_username='admin', database_password='admin',
                 password=None, username='root',host='localhost', port=2424):
        if app is not None:
            self.app = app
            self.init_app(self.app, database_name=database_name, database_username=database_username,
                          database_password=database_password, password=password, username=username, host=host, port=port)
        else:
            self.app = None

    def init_app(self, app, database_name=None, database_username="admin", database_password="admin", password=None,
                 username='root', host='localhost', port=2424):
        """
        """
        self.app = app
        self.app.config.setdefault('ORIENTDB_CURRENT_DATABASE', database_name)
        self.app.config.setdefault('ORIENTDB_DATABASE_USERNAME', database_username)
        self.app.config.setdefault('ORIENTDB_DATABASE_PASSWORD', database_password)
        self.app.config.setdefault('ORIENTDB_AUTO_OPEN', True)
        self.app.config.setdefault('ORIENTDB_SERVER_PASSWORD', password)
        self.app.config.setdefault('ORIENTDB_SERVER_USERNAME', username)
        self.app.config.setdefault('ORIENTDB_HOST', host)
        self.app.config.setdefault('ORIENTDB_PORT', port)
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)
        # register extension with app only to say "I'm here"
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['orientdb'] = self

    @property
    def connected(self):
        """Returns OrientDB connection status."""
        ctx = stack
        return getattr(ctx, 'orient_db_connection', None) is not None

    def teardown(self):
        """Close the connection to OrientDB."""
        ctx = stack
        if hasattr(ctx, 'orient_db_client'):
            ctx.orient_db_client.db_close()
            del ctx.orient_db_client
            del ctx.orient_db_connection

    def __getattr__(self, name, *args, **kwargs):
        ctx = stack
        if not self.connected:
            # TODO figure out how to use ctx.top
            if not hasattr(ctx, 'orient_db_client'):
                ctx.orient_db_client = OrientDBPy(self.app.config.get('ORIENTDB_HOST'),
                                                  self.app.config.get('ORIENTDB_PORT'))

            if not hasattr(ctx, 'orient_db_connection'):
                ctx.orient_db_connection = ctx.orient_db_client.connect(self.app.config.get('ORIENTDB_SERVER_USERNAME'),
                                                                self.app.config.get('ORIENTDB_SERVER_PASSWORD'))
        def wrapper(*args, **kw):
            if name != 'db_open' and self.app.config.get('ORIENTDB_AUTO_OPEN') and\
                    self.app.config.get('ORIENTDB_CURRENT_DATABASE'):
                        ctx.orient_db_client.db_open(self.app.config.get('ORIENTDB_CURRENT_DATABASE'),
                        self.app.config.get('ORIENTDB_DATABASE_USERNAME'),  self.app.config.get('ORIENTDB_DATABASE_PASSWORD'))
            if name == 'db_create' and not args:
                args = (pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY)
            # TODO check if this is needed
            if name == 'db_exists' and len(args) == 1:
                db_name = args[0]
                args = (db_name, pyorient.STORAGE_TYPE_MEMORY)
            if name == 'data_cluster_add' and len(args) == 1:
                cluster_name = args[0]
                args = (cluster_name, pyorient.CLUSTER_TYPE_PHYSICAL)
            if name == 'db_open':
                arg1 = args[0]
                # TODO check order username, password
                args = (arg1, 'ORIENTDB_DATABASE_USERNAME', 'ORIENTDB_DATABASE_PASSWORD')
            # TODO load record? check if needed for other methods
            return getattr(ctx.orient_db_client, name)(*args, **kw)
        return wrapper

    def __setitem__(self, key, value):
        # TODO unhardcode
        orient_config_list = ['ORIENTDB_SERVER_PASSWORD', 'ORIENTDB_SERVER_USERNAME', 'ORIENTDB_HOST', 'ORIENTDB_PORT',
                              'ORIENTDB_CURRENT_DATABASE', 'ORIENTDB_DATABASE_USERNAME', 'ORIENTDB_DATABASE_PASSWORD']
        if key in orient_config_list:
            self.app.config[key] = value