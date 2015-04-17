<h3>Flask-OrientDB</h3>
Flask-OrientDB simplifies using OrientDB with Flask by handling opening and closing your database connection
using Pyorient, a Python driver for OrientDB.

### Installation

### Example 
    from flask import Flask
    from flask.ext.orientdb import OrientDB
    
    app = Flask(__name__)
    client = OrientDB(app=app, server_un=your_un, server_pw=your_pw)
  
    @app.route("/")
    def cheese_eating_animals():
        client.set_db('animal', 'admin', 'my_pw')
        client.query("select * from Animal")
        cheese_eaters = client.command("select expand( in( Eat )) \
        from Food where name = 'pea'")
        return ','.join([cheese_eaters[0].name, cheese_eaters[0].species])
    
    if __name__ == "__main__":
            app.run()
            
    #For this example to work you need a database and schema set up.
    #Run create_db in the example folder to setup the db.

### Set Database
Set the OrientDB database you want to use. 
Username and password default to OrientDB's default 'admin', 'admin'
    
    app = Flask(__name__)
    client = OrientDB(app=app, server_un=your_un, server_pw=your_pw)
    client.set_db('mydb', 'admin', 'my_pw')

### Pyorient Commands
The following commands differ from pyorient:    
    # pyorient db_create   <br>
    client.db_create( db_name, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY ) <br>
    # flask-orientdb db_create   <br>
    client.db_create( db_name, 'graph', 'memory')    <br>
    <br>
    # pyorient db_exists <br>
    client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY ) <br>
    # flask-orientdb-createdb
    client.db_exists( db_name, 'memory') <br>
    <br>
    # pyorient cluster_add <br>
    client.data_cluster_add('my_cluster_1234567', pyorient.CLUSTER_TYPE_PHYSICAL <br>
    # flask-orientdb cluster_add <br>
    client.data_cluster_add( 'my_cluster_1234567','physical') <br>
    
    

flask-orientdb options for db_create: 'graph', 'document'. <br>
flask-orientdb options for db_exists: 'memory', 'local', 'plocal' <br>
flask-orientdb options for cluster_add: 'physical', 'memory' <br>
 <br>
Check Pyorient's documentation https://github.com/mogui/pyorient for a
complete list of commands. 


### Default Configuration Values
'ORIENTDB_AUTO_OPEN': True <br>
'ORIENTDB_SERVER_PASSWORD': None <br>
'ORIENTDB_SERVER_USERNAME': 'root' <br>
'ORIENTDB_HOST': 'localhost' <br>
'ORIENTDB_PORT': '2424'  <br>
'ORIENTDB_DB': None

Set 'ORIENTDB_AUTO_OPEN' to False to stop Flask_OrientDB from automatically
opening a database connection to self.current_database when a method requiring
a database connection is called.
