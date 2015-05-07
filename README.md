<h3>Flask-OrientDB</h3>
Flask-OrientDB simplifies using OrientDB with Flask by providing an interface between Flask and Pyorient, 
a Python driver for OrientDB.

### Installation
pip install flask-orientdb

### Example 
    from flask import Flask
    from flask.ext.orientdb import OrientDB
    
    app = Flask(__name__)
    app.debug = True
    client = OrientDB(app=app, server_pw=your_server_pw)
    db_name = 'test_db'
    db_type = 'plocal'
    client.set_db(db_name)
    
    @app.route("/")
    def home():
        # connect operations can be called without 'with client.connection()'
        if not client.db_exists(db_name, db_type):
            client.db_create(db_name, 'graph', db_type)
            
            # db operations need to be called within 'with client.connection()'
            with client.connection():
                client.command("CREATE CLASS Animal")
                client.command("INSERT INTO Animal set name = 'lizard', \
                              species = 'reptile'")
        with client.connection():
            result = client.query("SELECT * FROM Animal")
        return result[0].name
    
    if __name__ == "__main__":
            app.run()

### Create Client & Set Database
Instantiating the OrientDB object 

    app = Flask(__name__)
    client = OrientDB(flask_app, server_un='root', server_pw=None, 
                     host='localhost', port=2424)
 
 creates the following configuration values stored in your Flask app configuration: <br>
    'ORIENTDB_SERVER_PASSWORD': None <br>
    'ORIENTDB_SERVER_USERNAME': 'root' <br>
    'ORIENTDB_HOST': 'localhost' <br>
    'ORIENTDB_PORT': '2424'  <br>
    'ORIENTDB_DB': None

Set the OrientDB database you want to use. 
Username and password default to OrientDB's default 'admin', 'admin'

    client.set_db('mydb', 'admin', 'my_pw')
    
Change configuration

    app.config['ORIENTDB_SERVER_PASSWORD'] = my_new_pw

### Connection
When you are inside a Flask view function, a connection to OrientDB is established. You can use connect operations 
from inside a view function without doing anything. Using db_open operations from inside a view function must be done within 'with client.connection():' For a list of connect operations and db_open operations see 
http://orientdb.com/docs/last/Network-Binary-Protocol.html#introduction. <b>Do not call connect operations within 'with client.connection()', only use db_open operations.</b>


### Pyorient Commands
The following commands differ from pyorient:    
    
    # pyorient db_create   
    client.db_create( db_name, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY ) 
    # flask-orientdb db_create  
    client.db_create( db_name, 'graph', 'memory')   
 
    # pyorient db_exists
    client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY )
    # flask-orientdb-createdb
    client.db_exists( db_name, 'memory') 
    
    # pyorient cluster_add 
    client.data_cluster_add('my_cluster_1234567', pyorient.CLUSTER_TYPE_PHYSICAL
    # flask-orientdb cluster_add 
    client.data_cluster_add( 'my_cluster_1234567','physical') 
    
    

flask-orientdb options for db_create: 'graph', 'document'. <br>
flask-orientdb options for db_exists: 'memory', 'local', 'plocal' <br>
flask-orientdb options for cluster_add: 'physical', 'memory' <br>
 <br>
Check Pyorient's documentation https://github.com/mogui/pyorient for a
complete list of commands.

### Contribute
Pull requests are welcome. <br>
Feedback and comments are appreciated. Send to coryedwardalthoff@gmail.com.
