from flask import Flask
from flask.ext.orientdb import OrientDB
import unittest


class FlaskOrientDBTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.db_name = 'test_db'
        self.client = OrientDB(app=self.app,
                               server_password="B0FC9CF1CBEAD07351C4C30197C43BE2D611E94AFAFA7EF4B4AAD3262F7907DB",
                               database_name=self.db_name)
        if not self.client.db_exists('test_db'):
            self.client.db_create('test_db')

    def tearDown(self):
        pass
    def test_flaskorient_config(self):
        self.assertEqual(self.app.config['ORIENTDB_HOST'], 'localhost')
        self.assertEqual(self.app.config['ORIENTDB_PORT'], 2424)
        self.assertEqual(self.app.config['ORIENTDB_SERVER_USERNAME'], 'root')
        self.assertIsInstance(self.app.config['ORIENTDB_SERVER_PASSWORD'], str)
        self.assertEqual(self.app.config['ORIENTDB_AUTO_OPEN'], True)

    # def test_flaskorient_session(self):
    # #unittest.TestCase.assertIsInstance(self.connection(), int)
    #     self.assertIsInstance(self.app.ctx, int)

    def test_flaskorient_connections(self):
        self.client.db_open(self.db_name)
        assert  self.client.client_connected is True
        assert self.client.server_connection is True
        assert self.client.db_connection is False
        # db size needs db connection
        self.client.db_size()
        assert self.client.db_connection is True

    def test_flaskorient_teardown(self):
        self.client.db_size()
        self.client.teardown()
        assert self.client.db_connection is False

    def test_register_db(self):
        new_db = self.client.register_db('test_name', 'test_username', 'test_password')
        assert new_db in self.client.database_list

    def test_set_current_db(self):
        self.client.register_db('test_name', 'test_username', 'test_password')
        self.client.set_current_db('test_name')
        assert self.client.current_database.db_name == 'test_name'
        assert self.client.current_database.db_username == 'test_username'
        assert self.client.current_database.db_password == 'test_password'

    def test_pyorient_functionality(self):
        #TODO add create db needs teardown

        assert self.client.db_exists(self.db_name) is True

        self.assertIsInstance(self.client.db_open(self.db_name), list)

        self.client.db_close()
        assert self.client.server_connection is None
        assert self.client.db_connection is None

        self.assertIsInstance(self.db_list(), dict)

        self.assertIsInstance(self.db_size(), int)

        self.assertIsInstance(self.client.db_count_records(), int)

        #TODO send command, create record, update record, load a record, load a record with cache needs delete in teardown

        self.assertIsInstance(self.client.query("select from my_class", 10, '*:0'), list)

        #TODO make an async query, delete a record, drop a db, creat a new clster

        self.assertIsInstance(self.client.db_reload(), list)

# TODO test to test if flask is calling teardown