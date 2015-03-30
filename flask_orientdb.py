from pyorient import OrientDB as OrientDBPy
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack
import pyorient


class OrientDB(object):
    def __init__(self, app=None, password=None, username='root', host='localhost', port=2424):

        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        """
        """
        self.app = app
        self.config = config 
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)
        # register extension with app only to say "I'm here"
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['orientdb'] = self

    def config(self, password, username, host, port):
        self.app.config.setdefault('ORIENTDB_PASSWORD', password)
        self.app.config.setdefault('ORIENTDB_USERNAME', username)
        self.app.config.setdefault('ORIENTDB_HOST', host)
        self.app.config.setdefault('ORIENTDB_PORT', port)

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
                ctx.orient_db_client = OrientDBPy(self.app.config.get('ORIENTDB_HOST'), self.app.config.get('ORIENTDB_PORT'))

            if not hasattr(ctx, 'orient_db_connection'):
                ctx.orient_db_connection = ctx.orient_db_client.connect(self.app.config.get('ORIENTDB_USERNAME'),
                                                                      self.app.config.get('ORIENTDB_PASSWORD'))

        # TODO load record?
        def wrapper(*args, **kw):
            if name == 'db_create' and not args:
                args = (pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY)
            # check if this is needed
            if name == 'db_exists' and len(args) == 1:
                db_name = args[0]
                args = (db_name, pyorient.STORAGE_TYPE_MEMORY)
            if name == 'data_cluster_add' and len(args) == 1:
                cluster_name = args[0]
                args = (cluster_name, pyorient.CLUSTER_TYPE_PHYSICAL)
            if name == 'db_open':
                arg1 = args[0]
                args = (arg1, 'admin', 'admin')
            return getattr(ctx.orient_db_client, name)(*args, **kw)
        return wrapper

    def __setitem__(self, key, value):
        pass