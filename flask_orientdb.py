from pyorient import OrientDB as OrientDBPy
import pyorient

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack
from collections import namedtuple


def convert_memory_location(memory):
    memory_dict = {'local': pyorient.STORAGE_TYPE_LOCAL, 'plocal': pyorient.STORAGE_TYPE_PLOCAL,
                   'memory': pyorient.STORAGE_TYPE_MEMORY}
    if memory in memory_dict:
        return memory_dict[memory]
    else:
        raise Exception('invalid argument provided to createdb()')


def _db_create(name, type, memory):
    """
    :return name, db_type, and memory_location to be used as arguments in
    OrientDB.orientdb_client.db_create(name, type, memory)
    """
    type_dict = {'graph': pyorient.DB_TYPE_GRAPH, 'document':pyorient.DB_TYPE_DOCUMENT}
    if type in type_dict:
        return name, type_dict[type], convert_memory_location(memory)
    else:
        raise Exception('invalid argument provided to create_db()')


def _data_cluster_add(cluster_name, type):
    """
     :return name, db_type, and memory_location to be used as arguments in
    OrientDB.orientdb_client._data_cluster_add(cluster_name, cluster_type)
    """
    cluster_dict = {'physical': pyorient.CLUSTER_TYPE_PHYSICAL, 'memory': pyorient.CLUSTER_TYPE_MEMORY}
    if type in cluster_dict:
        return cluster_name, cluster_dict[type]
    else:
        raise Exception("invalid argument provided to data_cluster_add")


class OrientDB(object):
    """
    Creates class that manages OrientDB database orientdb_clients with Flask.
    :param app: The Flask application bound to this OrientDB instance.
                If an app is not provided at initialization time than it
                must be provided later by calling :meth:`init_app` manually.
    :param server_un: username for your OrientDB server
    :param server_pw: password for your OrientDB server
    :param host: host of your OrientDB server
    :param port: port for your OrientDB server
    """
    def __init__(self, app=None, server_un='root', server_pw=None, host='localhost', port=2424):
        self.Database = namedtuple('Database', 'db_name, db_username, db_password')
        if app is not None:
            self.init_app(app, server_un=server_un, server_pw=server_pw, host=host, port=port)
        else:
            self.app = None

    def init_app(self, app, server_pw, server_un='root', host='localhost',
                 port=2424):
        """
        params: see OrientDB docstring
        """
        if not app:
            raise Exception('pass in a flask app')
        self.app = app
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
        app.before_request(self._before_request)
        # register extension with app
        if 'orientdb' not in app.extensions:
            app.extensions['orientdb'] = self

    def set_db(self, db_name, db_username='admin', db_password='admin'):
        """
        :param db_name: name of the OrientDB database you want to use
        :param db_username: username for the OrientDB database you want to use
        :param db_password: password for the OrientDB database you want to use
        """
        self.app.config['ORIENTDB_DB'] = self.Database(db_name, db_username, db_password)

    def _before_request(self):
        self._create_client()

    def _create_client(self):
        """
        create OrientDB client that is used to execute all Pyorient commands.
        """
        ctx = stack.top
        ctx.orientdb_client = OrientDBPy(self.app.config.get('ORIENTDB_HOST'),
                                        self.app.config.get('ORIENTDB_PORT'))

        ctx.orientdb_client.connect(self.app.config.get('ORIENTDB_SERVER_USERNAME'),
                                        self.app.config.get('ORIENTDB_SERVER_PASSWORD'))

    def _connect_to_db(self):
        """
        call db_open on OrientDB client
        """
        if self.orientdb_client:
            return self.orientdb_client.db_open(self.app.config.get('ORIENTDB_DB').db_name,
                                           self.app.config.get('ORIENTDB_DB').db_username,
                                           self.app.config.get('ORIENTDB_DB').db_password)
        else:
            raise Exception("tried to connect to db without client.")

    @property
    def orientdb_client(self):
        """
        :return OrientDB client that is used to execute all Pyorient commands.
        """
        ctx = stack.top
        if hasattr(ctx, 'orientdb_client'):
            return ctx.orientdb_client

    def _new_orientdb_client(self):
        self._delete_orientdb_client()
        self._create_client()

    def _delete_orientdb_client(self):
        ctx = stack.top
        if hasattr(ctx, 'orientdb_client'):
            del ctx.orientdb_client

    def connection(self):
        return self

    def __enter__(self):
        self._connect_to_db()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.orientdb_client.db_close()
        self._new_orientdb_client()

    def _teardown(self, *args):
        """
        Close the orientdb_client to OrientDB database and delete OrientDB client
        """
        self._delete_orientdb_client()

    def __getattr__(self, name, *args, **kwargs):
        """
        :param name: name of the method called
        :param args: parameters to pass to OrientDB client
        :param kwargs:parameters to pass to OrientDB client
        :return: function that calls the name of the method passed in on the OrientDB client using
        the arguments passed in.
        """

        def wrapper(*args, **kw):
            if name == 'db_create':
                if len(args) != 3:
                    raise Exception('db_create takes 3 arguments')
                args = _db_create(args[0], args[1], args[2])
            if name == 'data_cluster_add':
                if len(args) != 2:
                    raise Exception('db_cluster_add takes 3 arguments')
                args = _data_cluster_add(args[0], args[1])
            if name == 'db_exists':
                if len(args) != 2:
                    raise Exception('db_exists takes 2 arguments')
                args = (args[0], convert_memory_location(args[1]))
            return getattr(self.orientdb_client, name)(*args, **kw)
        return wrapper