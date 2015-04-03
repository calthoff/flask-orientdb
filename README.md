*Not finished yet

<h3>Flask-OrientDB</h3>
Flask-OrientDB simplifies using OrientDB with Flask by providing an interface to Pyorient, 
a Python driver for OrientDB, and makes it easy to manage multiple OrientDB databases.

### Installation

### Example 
    from flask import Flask
    from flask.ext.orientdb import OrientDB
    
    app = Flask(__name__)
    client = OrientDB(app=app, server_un=your_un, server_pw=your_pw)
    client.set_current_db('animal')
    
    @app.route("/")
    def cheese_eating_animals():
        client.query("select * from Animal")
        cheese_eaters = client.command("select expand( in( Eat )) \
        from Food where name = 'pea'")
        return ','.join([cheese_eaters[0].name, cheese_eaters[0].species])
    
    if __name__ == "__main__":
            app.run()
            
    #For this example to work you need a database and schema set up, please see
    the example folder for a working demo.

### Pyorient Commands
Check Pyorient's documentation https://github.com/mogui/pyorient for a
complete list of commands.

### Multiple Databases
    app = Flask(__name__)
    client = OrientDB(app=app, server_un=your_un, server_pw=your_pw)
    
    client.set_current_db('db_one', server_un=your_un, server_pw=your_pw)
    db_one_length = client.db_size()
    
    client.set_current_db('db_two', server_un=your_un, server_pw=your_pw)
    db_two_length = client.db_size()

### Default Configuration Values
'ORIENTDB_AUTO_OPEN': True <br>
'ORIENTDB_SERVER_PASSWORD': None <br>
'ORIENTDB_SERVER_USERNAME': 'root' <br>
'ORIENTDB_HOST': 'localhost' <br>
'ORIENTDB_PORT' '2424'  <br>

Set 'ORIENTDB_AUTO_OPEN' to False to stop Flask_OrientDB from automatically
opening a database connection to self.current_database when a method requiring
a database connection is called.
    
### Edit Configuration
    app = Flask(__name__)
    client = OrientDB(app=app, server_un=your_un, server_pw=your_pw)
    app.config['ORIENTDB_AUTO_OPEN'] = False
    
### API Documentation
<i>class</i> flask_orientdb.<b>OrientDB</b>(<i>app=app, server_username='root', server_password=None host='localhost', port=2424</i>)
<br>This class is used to integrate OrientDB into a Flask application.
<br><i>Parameters</i>:	
<i>app</i> - The Flask application will be bound to this MongoKit instance. If an app is not provided at                  initialization time than it must be provided later by calling init_app() manually.

<i>server_username</i>- Username of the OrientDB server to connect to. 

<i>server_password</i>- Password of the OrientDB server to connect to. 

<i>host</i>- The address of the OrientDB server to connect to. 

<i>port</i>- The port of the OrientDB server to connect to.

<b>client_connected</b><br>
    Returns whether the client is connected

<b>database_connected</b><br>
Returns database connection status to OrientDB server

<b>init_app(</b><i>app=app, server_username='root', server_password=None                                                     host='localhost', port=2424</i><b>)</b><br>
This method connects your app with this extension. Flask- OrientDB handles connecting and disconnecting from OrientDB 
<br><i>Parameters:</i><br>	Same as __init__ parameters.  

<b>set_current_db(</b><i>db_name, db_username=admin, db_password=admin</i><b>)</b><br>
Set the database you want to use. When current_db is called, it registers 
your database so if you've already called set__current_db on one of your      
databases, the second time you call it you do not need to provide a password. Username 
and password default to admin because new OrientDB databases default to admin when they
are created.
  
<b>server_connected</b>
  <br>Returns server connection status to OrientDB server
