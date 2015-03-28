import flask
from flask.ext.orientdb import orientdb
import unittest
import pyorient


class Orientdb_Tests(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask('test')

    def test_flaskorient_config(self):
        unittest.assertEqual(self.app.config['ORIENTDB_HOST'], 'localhost')
        unittest.assertEqual(self.app.config['ORIENTDB_PORT'], '2429')
        unittest.assertEqual(self.app.config['ORIENTDB_USERNAME'], 'root')
        unittest.assertEqual(self.app.config['ORIENTDB_USERNAME'], None)

    def test_flaskorient_connect(self):
        client = orientdb()
        session_id = client.connect( "root", "B0FC9CF1CBEAD07351C4C30197C43BE2D611E94AFAFA7EF4B4AAD3262F7907DB")
        unittest.assertIsInstance(session_id, int)

    def test_flaskorient_teardown(self):
        pass