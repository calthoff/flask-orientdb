from flask import Flask
from flask.ext.orientdb import OrientDB
import unittest
import pyorient


class FlaskOrientDBTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        ctx = cls.app.test_request_context()
        ctx.push()
        cls.db_name = 'wow1d3d'
        cls.password = "B0FC9CF1CBEAD07351C4C30197C43BE2D611E94AFAFA7EF4B4AAD3262F7907DB"
        cls.client = OrientDB(app=cls.app,
                               server_pw=cls.password)
        if cls.client.db_exists(cls.db_name):
            cls.client.db_drop(cls.db_name)
            cls.client.db_create(cls.db_name, 'graph', 'plocal')
        else:
            cls.client.db_create(cls.db_name, 'graph', 'plocal')
        cls.client.set_db(cls.db_name)
        cls.test_class = 'test_class'
        sql = "CREATE CLASS %s" % cls.test_class
        cls.client.command(sql)
        cls.test_cluster_id = cls.client.data_cluster_add('test_cluster', 'physical')
        rec = { '@my_class': { 'accommodation': 'house', 'work': 'office', 'holiday': 'sea' }}
        cls.rec_position = cls.client.record_create(cls.test_cluster_id, rec)

    def tearDown(cls):
        cls.client.set_db(cls.db_name)
        if cls.client.connection:
            if cls.client.connection._connection.db_opened:
                # close db connection to test if failure on method that needs to open db connection
                cls.client.db_close()

    def test_flaskorient_config(cls):
        cls.assertEqual(cls.app.config['ORIENTDB_HOST'], 'localhost')
        cls.assertEqual(cls.app.config['ORIENTDB_PORT'], 2424)
        cls.assertEqual(cls.app.config['ORIENTDB_SERVER_USERNAME'], 'root')
        cls.assertIsInstance(cls.app.config['ORIENTDB_SERVER_PASSWORD'], str)
        cls.assertEqual(cls.app.config['ORIENTDB_AUTO_OPEN'], True)

    def test_connect_to_db(cls):
        cls.assertIsInstance(cls.client._connect_to_db(), list)

    def test_flaskorient_teardown(cls):
        # open db connection
        cls.client.db_size()
        cls.client._teardown()
        assert cls.client.connection is None

    ####################### test pyorient functionality ######################################################
    def test_db_drop(cls):
        db_drop_name = 'db_drop'
        cls.client.db_create(db_drop_name, 'graph', 'plocal')
        cls.client.db_drop(db_drop_name)

    def test_db_list(cls):
        cls.assertIsInstance(cls.client.db_list(), pyorient.types.OrientRecord)

    def test_db_exists(cls):
        assert cls.client.db_exists(cls.db_name, 'plocal') is True
        assert cls.client.db_exists('dfsfdsfsd', 'plocal') is False

    def test_reloaddb(cls):
        cls.assertIsInstance(cls.client.db_reload(), list)

    def test_db_size(cls):
        cls.assertIsInstance(cls.client.db_size(), int)

    def test_db_open(cls):
        cls.assertIsInstance(cls.client.db_open(cls.db_name, 'admin', 'admin'), list)

    def test_command(cls):
        cls.assertIsInstance(cls.client.command("CREATE CLASS test_command"), list)
        cls.assertIsInstance(cls.client.command("DROP CLASS test_command"), list)

    def test_make_a_query(cls):
        sql = "select from %s" % cls.test_class
        cls.assertIsInstance(cls.client.query(sql), list)

    def test_async_query(cls):
        def _my_callback(for_every_record):
            pass
            result = cls.client.query_async("select from test_class", 10, '*:0', _my_callback)

    # clusters
    def test_add_cluster(cls):
        cls.assertIsInstance(cls.client.data_cluster_add('create_cluster_test', 'physical'), int)

    def test_data_cluster_drop(cls):
        delete_cluster = 'dc'
        cls.client.data_cluster_add(delete_cluster, 'physical')
        cls.client.data_cluster_drop(delete_cluster)

    def test_data_cluster_data_range(cls):
        cls.assertIsInstance(cls.client.data_cluster_data_range(cls.test_cluster_id), list)

    def test_record_create(cls):
        rec = { '@my_class': {'accommodation': 'house', 'work': 'office', 'holiday': 'sea'}}
        cls.assertIsInstance(cls.client.record_create(cls.test_cluster_id, rec), pyorient.types.OrientRecord)

    def test_data_cluster_count(cls):
        cls.assertIsInstance(cls.client.data_cluster_count([cls.test_cluster_id]), int)

    #records
    def test_update_record(cls):
        rec3 = { '@my_class': {'accommodation': 'hotel', 'work': 'home', 'holiday': 'hills'}}
        cls.assertIsInstance(cls.client.record_update(cls.rec_position._rid,
                              cls.rec_position._rid, rec3, cls.rec_position._version), list)

    def test_db_count_records(cls):
        cls.assertIsInstance(cls.client.db_count_records(), int)

    def test_record_load(cls):
        cls.client.record_load( cls.rec_position._rid )

    def test_record_delete(cls):
        pass

    def test_sql_batch(cls):
        cmd = ("begin;"
        "let a = create vertex set script = true;"
        "let b = select from v limit 1;"
        "let e = create edge from $a to $b;"
        "commit retry 100;")
        cls.assertIsInstance(cls.client.batch(cmd), list)