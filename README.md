<h3>flask-orientdb</h3>
**not finished***
### Example 
    app = Flask(__name__) 
    client = OrientDB(orientdb_password, app=app)  
    if not client.db_exists('test_db', pyorient.STORAGE_TYPE_MEMORY ):
        client.db_create( 'test_db', pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY )
    print client.db_list()  
 
