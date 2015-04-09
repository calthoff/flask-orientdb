from flask import Flask
from flask.ext.orientdb import OrientDB
import unittest
import pyorient


class FlaskOrientDBTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        ctx = self.app.test_request_context()
        ctx.push()
        self.db_name = 'my_tb4u677'
        self.cluster_name = 'my_test_clust'
        self.password = "B0FC9CF1CBEAD07351C4C30197C43BE2D611E94AFAFA7EF4B4AAD3262F7907DB"
        self.client = OrientDB(app=self.app,
                               server_pw=self.password)
        self.client.set_current_db(self.db_name)

        if not self.client.db_exists(self.db_name):
            self.client.db_create(self.db_name, 'graph', 'plocal')

    def tearDown(self):
        self.client.db_close()

    def test_flaskorient_config(self):
        self.assertEqual(self.app.config['ORIENTDB_HOST'], 'localhost')
        self.assertEqual(self.app.config['ORIENTDB_PORT'], 2424)
        self.assertEqual(self.app.config['ORIENTDB_SERVER_USERNAME'], 'root')
        self.assertIsInstance(self.app.config['ORIENTDB_SERVER_PASSWORD'], str)
        self.assertEqual(self.app.config['ORIENTDB_AUTO_OPEN'], True)

    def test_connect_to_db(self):
        self.assertIsInstance(self.client._connect_to_db(), list)

    def test_flaskorient_teardown(self):
        self.client.db_size()
        self.client._teardown()
        assert self.client.db_connection is None

    def test_register_db(self):
        new_db = self.client._register_db('test_name', 'test_username', 'test_password')
        assert new_db in self.client.database_list

    def test_set_current_db(self):
        self.client.set_current_db('test_name', 'test_username', 'test_password')
        assert self.client.current_database.db_name == 'test_name'
        assert self.client.current_database.db_username == 'test_username'
        assert self.client.current_database.db_password == 'test_password'

    # ###################### test pyorient functionality ######################################################
    def test_db_list(self):
        self.assertIsInstance(self.client.db_list(), pyorient.types.OrientRecord)

    def test_db_exists(self):
        assert self.client.db_exists( self.db_name, 'plocal') is True
        assert self.client.db_exists('dfsfdsfsd', 'plocal') is False

    # ################## pyorient methods that call __attr__ in flask-orientdb #################################
    def test_reloaddb(self):
        self.assertIsInstance(self.client.db_reload(), list)

    def test_db_count_records(self):
        self.assertIsInstance(self.client.db_count_records(), int)

    def test_db_size(self):
        self.assertIsInstance(self.client.db_size(), int)

    def test_db_open(self):
        self.assertIsInstance(self.client.db_open(self.db_name, 'admin', 'admin'), list)

    def test_command(self):
        self.assertIsInstance(self.client.command("CREATE CLASS test_class"), list)
        self.assertIsInstance(self.client.command("DROP CLASS test_class"), list)

    def test_make_a_query(self):
        self.client.command("CREATE CLASS test_class")
        self.assertIsInstance(self.client.query("select from test_class"), list)
        self.client.command("DROP CLASS test_class")

    # def test_async_query(self):
    #     self.client.command("CREATE CLASS test_class")
    #     def _my_callback(for_every_record):
    #         print(for_every_record)
    #     result = self.client.query_async("select from my_class", 10, '*:0', _my_callback)
    #     self.client.command("DROP CLASS test_class")
    #     self.assertIsInstance(result, None)

    # def test_data_cluster_add_drop(self):
    #     self.assertIsInstance(self.client.data_cluster_add(self.cluster_name, 'physical'), int)
    #     assert self.client.data_cluster_drop(self.cluster_name) is True

    # def test_data_cluster_drop(self):
    #     delete_cluster = 'delete_cluster'
    #     self.client.data_cluster_add(delete_cluster, 'physical')
    #     self.client.data_cluster_drop(delete_cluster)

    # def test_data_cluster_data_range(self):
    #     self.assertIsInstance(self.client.data_cluster_data_range(self.cluster_name), list)

    #def test_record_create(self):
    #     rec = { '@my_class': { 'accommodation': 'house', 'work': 'office', 'holiday': 'sea' } }
    #     rec_position =  self.client.record_create( self.cluster_id, rec )

# records, async query, dropdb,clusters, transactions, batch, persistent connections

# TODO pyorient needs a way to delete a class
# TODO pyorient needs a way to delete a cluster and to list all clusters
# TODO test to test if flask is calling teardown
# TODO test opening without connection
# TODO tests for plocal, local, memory should be able to do this with same tests
# TODO pyorient createdb needs option to set username and password