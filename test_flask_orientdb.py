from flask import Flask
from flask.ext.orientdb import OrientDB
import unittest
import pyorient


class FlaskOrientDBTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.db_name = 'the_new_db5'
        self.cluster_name = 'my_test_cluster'
        self.password = "B0FC9CF1CBEAD07351C4C30197C43BE2D611E94AFAFA7EF4B4AAD3262F7907DB"
        self.client = OrientDB(app=self.app,
                               server_password=self.password)
        self.client.set_current_db(self.db_name)
        # Pyorient db exists is broken
        if not self.client.db_exists(self.db_name):
        # TODO why memory doesn't work and plocal does
            self.client.db_create(self.db_name, 'graph', 'plocal')

    def tearDown(self):
        self.client.db_drop(self.db_name)

    def test_flaskorient_config(self):
        self.assertEqual(self.app.config['ORIENTDB_HOST'], 'localhost')
        self.assertEqual(self.app.config['ORIENTDB_PORT'], 2424)
        self.assertEqual(self.app.config['ORIENTDB_SERVER_USERNAME'], 'root')
        self.assertIsInstance(self.app.config['ORIENTDB_SERVER_PASSWORD'], str)
        self.assertEqual(self.app.config['ORIENTDB_AUTO_OPEN'], True)

    def test_create_client(self):
        self.assertIsInstance(self.client._create_client(), pyorient.orient.OrientDB)

    def test_connect_to_server(self):
        self.assertIsInstance(self.client._connect_to_server(), int)

    def test_connect_to_db(self):
        self.assertIsInstance(self.client._connect_to_db(), list)

    # def test_flaskorient_teardown(self):
    #     self.client.db_size()
    #     self.client.teardown()
    #     assert self.client.db_connection is False
    #
    def test_register_db(self):
        new_db = self.client._register_db('test_name', 'test_username', 'test_password')
        assert new_db in self.client.database_list

    def test_set_current_db(self):
        self.client.set_current_db('test_name', 'test_username', 'test_password')
        assert self.client.current_database.db_name == 'test_name'
        assert self.client.current_database.db_username == 'test_username'
        assert self.client.current_database.db_password == 'test_password'

    # test pyorient functionality
    def test_db_list(self):
        self.assertIsInstance(self.client.db_list(), pyorient.types.OrientRecord)

    def test_db_size(self):
        self.assertIsInstance(self.client.db_size(), int)

    def test_db_count_records(self):
        self.assertIsInstance(self.client.db_count_records(), int)

    def test_make_a_query(self):
        self.client.command( "create class my_class extends V")
        self.assertIsInstance(self.client.query("select from my_class", 10, '*:0'), list)

    def test_reloaddb(self):
        self.assertIsInstance(self.client.db_reload(), list)

    # def shutdown(self):
    #     self.assertIsInstance(self.client.shutdown( "root", self.password), list)


    # pyorient methods that call __attr__ in flask-orientdb
    def test_create_drop_db(self):
        test_db2 = 'cd_test'
        self.client.db_create(test_db2, 'graph', 'plocal')
        assert self.client.db_exists(test_db2) is True
        self.client.db_drop(test_db2)
        assert self.client.db_exists(test_db2) is False

    def test_db_open(self):
        self.assertIsInstance(self.client.db_open(self.db_name, 'admin', 'admin'), list)

    def test_command(self):
        self.assertIsInstance(self.client.command( "create class my_class extends V" ), list)

    def test_data_cluster_add(self):
        self.assertIsInstance(self.client.data_cluster_add(self.cluster_name, 'physical'), int)

    # def test_data_cluster_drop(self):
        delete_cluster = 'delete_cluster'
        #self.client.data_cluster_add(delete_cluster, 'physical')
    #     assert self.client.data_cluster_drop(delete_cluster) is True
    #     self.client.db_close()

    def test_data_cluster_data_range(self):
        self.assertIsInstance(self.client.data_cluster_data_range(self.cluster_name), list)

    def test_db_exists(self):
        assert self.client.db_exists( self.db_name, 'plocal') is True
        assert self.client.db_exists('dfsfdsfsd', 'plocal') is False

# TODO test to test if flask is calling teardown
# TODO test opening without connection
# TODO tests for plocal, local, memory should be able to do this with same tests
# TODO pyorient createdb needs option to set username and password