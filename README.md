*Not finished yet

<h3>Flask-OrientDB</h3>
Flask-OrientDB simplifies using OrientDB with Flask by providing an interface to Pyorient, 
a Python driver for OrientDB, and providing support for using multiple OrientDB databases.

### Installation

### Example 
    from flask import Flask
    from flask.ext.orientdb import OrientDB
    
    app = Flask(__name__)
    client = OrientDB(app=app, server_username=your_username, server_password=your_password)
    client.set_current_db('animal')
    
    @app.route("/")
    def cheese_eating_animals():
        client.query("select * from Animal")
        animal_list = []
        cheese_eaters = client.command("select expand( in( Eat )) from Food where name = 'pea'")
        return ','.join([cheese_eaters[0].name, cheese_eaters[0].species])
    
    if __name__ == "__main__":
            app.run()
            
    #For this example to work you need a database and schema set up, please see the example 
    folder for a working demo.

### Pyorient Commands
Check Pyorient's documentation https://github.com/mogui/pyorient for a
complete list of commands.

### Multiple Databases
    app = Flask(__name__)
    client = OrientDB(app=app, server_username=your_username, server_password=your_password)
    
    client.set_current_db('db_one', username=your_username, password=your_password)
    db_one_length = client.db_size()
    
    client.set_current_db('db_two', username=your_username, password=your_password)
    db_two_length = client.db_size()

### Default Configuration Values
'ORIENTDB_AUTO_OPEN': True
'ORIENTDB_SERVER_PASSWORD': None
'ORIENTDB_SERVER_USERNAME': 'root'
'ORIENTDB_HOST': 'localhost'
'ORIENTDB_PORT' '2424' 

Set 'ORIENTDB_AUTO_OPEN' to False to stop Flask_OrientDB from automatically
opening a database connection to self.current_database when a
method requiring a database connection is called.
    
### Edit Configuration
    app = Flask(__name__)
    client = OrientDB(app=app, server_password=your_password)
    app.config['ORIENTDB_AUTO_OPEN'] = False
    
### API Documentation
class flask_orientdb.OrientDB(app=app, server_username='root', server_password=None host=host, port=port)
This class is used to integrate OrientDB into a Flask application.
Parameters:	
app - The Flask application will be bound to this MongoKit instance. If an app is not provided at                  initialization time than it must be provided later by calling init_app() manually.

server_username- Username of the OrientDB server to connect to. 

server_password- Password of the OrientDB server to connect to. 

host- The address of the OrientDB server to connect to. 

port- The port of the OrientDB server to connect to.

client_connected():
Returns whether the client is connected

database_connected()
Returns database connection status to OrientDB server
server_connected():
Returns whether the server is connected

init_app(app=app, server_username='root', server_password=None                                                     host=host, port=port)
This method connects your app with this extension. Flask- OrientDB handles 
connecting and disconnecting from OrientDB
Parameters:	Same as __init__ parameters. 

set_current_db(db_name, db_username=admin, db_password=admin)
Set the database you want to use. When current_db is called, it registers your database so if you've already 
called set__current_db on one of your databases, the second time you call it you do not need to provide a          password. Username and password default to admin because new OrientDB databases default to admin when they are     created.
   
