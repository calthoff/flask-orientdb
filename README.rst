<h3>Flask-OrientDB</h3>
Flask-OrientDB simplifies using OrientDB with Flask by handling opening and closing your database connection
using Pyorient a Python driver for OrientDB.

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
Username and password default to OrientDB's default 'admin', 'admin'
    app = Flask(__name__)
    client = OrientDB(app=app, server_un=your_un, server_pw=your_pw)
    client.set_db('mydb', 'admin', 'my_pw')

### Pyorient Commands
The following commands differ from pyorient:
'graph' and 'memory' are used instead of pyorient.DB_TYPE_GRAPH and 
pyorient.STORAGE_TYPE_MEMORY. Use 'document' to create a document database.
You can use 'plocal' and 'local' instead of 'memory'.
    client.db_create( db_name, 'graph', 'memory')
    client.db_exists( db_name, 'memory')
    
    # 'physical' is passed in instead of pyorient.CLUSTER_TYPE_PHYSICAL 
    # you can also pass in 'memory'
    new_cluster_id = client.data_cluster_add( 'my_cluster_1234567','physical')

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