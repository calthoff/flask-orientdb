from flask import Flask
from flask.ext.orientdb import OrientDB
import unittest


class FlaskOrientDBTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.orient = OrientDB(app=self.app, password="B0FC9CF1CBEAD07351C4C30197C43BE2D611E94AFAFA7EF4B4AAD3262F7907DB")

    def test_flaskorient_config(self):
        self.assertEqual(self.app.config['ORIENTDB_HOST'], 'localhost')
        self.assertEqual(self.app.config['ORIENTDB_PORT'], 2424)
        self.assertEqual(self.app.config['ORIENTDB_USERNAME'], 'root')

    # def test_flaskorient_session(self):
    #     #unittest.TestCase.assertIsInstance(self.connection(), int)
    #     self.assertIsInstance(self.app.ctx, int)

    def test_flaskorient_connected(self):
        assert self.orient.connected is True

    def test_flaskorient_teardown(self):
        # 0.9 and later
        self.orient.teardown()
        assert self.orient.connected is False
        # # 0.7 to 0.8
        # self.app.teardown_request(self.orient.teardown)
        # assert self.orient.connected is False
        # # Older Flask versions
        # self.app.after_request(self.orient.teardown)
        # assert self.orient.connected is False


