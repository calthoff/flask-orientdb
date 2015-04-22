from flask import Flask
from flask.ext.orientdb import OrientDB
import unittest
import pyorient


class FlaskOrientDBTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.db_name = 'tdb'
        # set server password
        cls.password = "B0FC9CF1CBEAD07351C4C30197C43BE2D611E94AFAFA7EF4B4AAD3262F7907DB"
        cls.client = OrientDB(app=cls.app, server_pw=cls.password)
        cls.client.set_db(cls.db_name)
        cls.ctx = cls.app.test_request_context()
        cls.ctx.push()
        # creates client
        cls.app.preprocess_request()
        if cls.client.db_exists(cls.db_name, 'plocal'):
            cls.client.db_drop(cls.db_name)
            cls.client.db_create(cls.db_name, 'graph', 'plocal')
        else:
            cls.client.db_create(cls.db_name, 'graph', 'plocal')
        cls.test_class = 'test_class'
        with cls.client.connection() :
            # create class for other tests
            sql = "CREATE CLASS %s" % cls.test_class
            cls.client.command(sql)
            # create cluster for other tests
            cls.test_cluster_id = cls.client.data_cluster_add('test_cluster', 'physical')
            # create record for other tests
            rec = { '@my_class': { 'accommodation': 'house', 'work': 'office', 'holiday': 'sea' }}
            cls.rec_position = cls.client.record_create(cls.test_cluster_id, rec)

        cls.client._teardown()

    def tearDown(cls):
        cls.client.set_db(cls.db_name)
        cls.client._teardown()

    def test_flaskorient_config(cls):
        cls.assertEqual(cls.app.config['ORIENTDB_HOST'], 'localhost')
        cls.assertEqual(cls.app.config['ORIENTDB_PORT'], 2424)
        cls.assertEqual(cls.app.config['ORIENTDB_SERVER_USERNAME'], 'root')
        cls.assertIsInstance(cls.app.config['ORIENTDB_SERVER_PASSWORD'], str)

    def test_connect_to_db(cls):
        cls.app.preprocess_request()
        cls.assertIsInstance(cls.client._connect_to_db(), list)

    def test_flaskorient_teardown(cls):
        cls.client._teardown()
        assert cls.client.orientdb_client is None

    ####################### test pyorient functionality ########################################
    def test_db_drop(cls):
        cls.app.preprocess_request()
        db_drop_name = 'db_drop'
        cls.client.db_create(db_drop_name, 'graph', 'plocal')
        cls.client.db_drop(db_drop_name)

    def test_db_list(cls):
        cls.app.preprocess_request()
        cls.assertIsInstance(cls.client.db_list(), pyorient.types.OrientRecord)

    def test_db_exists(cls):
        cls.app.preprocess_request()
        assert cls.client.db_exists(cls.db_name, 'plocal') is True
        assert cls.client.db_exists('dfsfdsfsd', 'plocal') is False

    def test_reloaddb(cls):
        cls.app.preprocess_request()
        with cls.client.connection() :
            cls.assertIsInstance(cls.client.db_reload(), list)

    def test_db_size(cls):
        cls.app.preprocess_request()
        with cls.client.connection() :
            cls.assertIsInstance(cls.client.db_size(), int)

    def test_db_open(cls):
        cls.app.preprocess_request()
        cls.assertIsInstance(cls.client.db_open(cls.db_name, 'admin', 'admin'), list)

    def test_command(cls):
        cls.app.preprocess_request()
        with cls.client.connection() :
            cls.assertIsInstance(cls.client.command("CREATE CLASS test_command"), list)
            cls.assertIsInstance(cls.client.command("DROP CLASS test_command"), list)

    def test_make_a_query(cls):
        cls.app.preprocess_request()
        with cls.client.connection() :
            sql = "select from %s" % cls.test_class
            cls.assertIsInstance(cls.client.query(sql), list)

    def test_async_query(cls):
        cls.app.preprocess_request()
        def _my_callback(for_every_record):
            pass
            result = cls.client.query_async("select from test_class", 10, '*:0', _my_callback)

    # cluster
    def test_add_cluster(cls):
        cls.app.preprocess_request()
        with cls.client.connection() :
            cls.assertIsInstance(cls.client.data_cluster_add('create_cluster_test', 'physical'), int)

    # # TODO fix
    # # def test_data_cluster_drop(cls):
    # #     delete_cluster = 'dsdfdsfdsdsfdsffsdd'
    # #     cls.client.data_cluster_add(delete_cluster, 'physical')
    # #     cls.client.data_cluster_drop(delete_cluster)
    # #     cls. cluster_drop = True
    #
    def test_data_cluster_data_range(cls):
        cls.app.preprocess_request()
        with cls.client.connection() :
            cls.assertIsInstance(cls.client.data_cluster_data_range(cls.test_cluster_id), list)

    def test_data_cluster_count(cls):
        cls.app.preprocess_request()
        with cls.client.connection() :
            cls.assertIsInstance(cls.client.data_cluster_count([cls.test_cluster_id]), int)

    # records
    def test_update_record(cls):
        rec3 = { '@my_class': {'accommodation': 'hotel', 'work': 'home', 'holiday': 'hills'}}
        cls.app.preprocess_request()
        with cls.client.connection() :
            cls.assertIsInstance(cls.client.record_update(cls.rec_position._rid,
                                cls.rec_position._rid, rec3, cls.rec_position._version), list)

    def test_record_create(cls):
        cls.app.preprocess_request()
        with cls.client.connection() :
            rec = { '@my_class': {'accommodation': 'house', 'work': 'office', 'holiday': 'sea'}}
            cls.assertIsInstance(cls.client.record_create(cls.test_cluster_id, rec), pyorient.types.OrientRecord)

    def test_db_count_records(cls):
        cls.app.preprocess_request()
        with cls.client.connection() :
            cls.assertIsInstance(cls.client.db_count_records(), int)

    def test_record_load(cls):
        cls.app.preprocess_request()
        with cls.client.connection() :
            cls.assertIsInstance(cls.client.record_load( cls.rec_position._rid), pyorient.types.OrientRecord)

    # todo create this test
    def test_record_delete(cls):
        pass

    # transactions
    def test_transactions(cls):
        # cls.client.set_db('holy',)
        # cls.client.db_open('holy', 'admin','admin')
        cls.app.preprocess_request()
        with cls.client.connection():
            cluster_id = 3

            # execute real create to get some info
            rec = { 'accommodation': 'mountain hut', 'work': 'not!', 'holiday': 'lake' }
            rec_position = cls.client.record_create( cluster_id, rec )

            tx = cls.client.tx_commit()
            tx.begin()


            # create a new record
            rec1 = { 'accommodation': 'home', 'work': 'some work', 'holiday': 'surf' }
            rec_position1 = cls.client.record_create( -1, rec1 )

            # prepare for an update
            rec2 = { 'accommodation': 'hotel', 'work': 'office', 'holiday': 'mountain' }
            update_record = cls.client.record_update( cluster_id, rec_position._rid, rec2, rec_position._version )

            tx.attach( rec_position1 )
            tx.attach( rec_position1 )
            y = tx.attach( update_record )

            res = tx.commit()

    # sessions
    def test_set_token(cls):
        cls.app.preprocess_request()
        cls.assertIsInstance(cls.client.set_session_token(True), pyorient.orient.OrientDB)

    def test_get_session_token(cls):
        cls.app.preprocess_request()
        cls.assertIsInstance(cls.client.get_session_token(), str)

    # # batch
    def test_sql_batch(cls):
        cls.app.preprocess_request()
        with cls.client.connection() :
            cmd = ("begin;"
            "let a = create vertex set script = true;"
            "let b = select from v limit 1;"
            "let e = create edge from $a to $b;"
            "commit retry 100;")
            cls.assertIsInstance(cls.client.batch(cmd), list)