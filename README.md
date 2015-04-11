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
  
    @app.route("/")
    def cheese_eating_animals():
	client.set_current_db('animal')
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
    
    # only have to enter password once
    client.set_current_db('db_one')
    

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
    

