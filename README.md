*Not finished yet

<h3>Flask-OrientDB</h3>
Flask-OrientDB simplifies using OrientDB with Flask by providing an interface to Pyorient, 
a Python driver for OrientDB.

### Installation

### Example 
    from flask import Flask
from flask.ext.orientdb import OrientDB


if __name__ == '__main__':
    app = Flask(__name__)
    client = OrientDB(app=app, server_password='B0FC9CF1CBEAD07351C4C30197C43BE2D611E94AFAFA7EF4B4AAD3262F7907DB')
    if not client.db_exists('animal'):
        client.db_create("animal", 'graph', 'plocal')

    client.set_current_db('animal')

    # Create the Vertex Animal
    client.command("create class Animal extends V")

    # Insert a new value
    client.command("insert into Animal set name = 'rat', specie = 'rodent'")

    # query the values
    client.query("select * from Animal")

    # Create the vertex and insert the food values

    client.command('create class Food extends V')
    client.command("insert into Food set name = 'pea', color = 'green'")

    # Create the edge for the Eat action
    client.command('create class Eat extends E')

    # Lets the rat likes to eat pea
    eat_edges = client.command(
        "create edge Eat from ("
        "select from Animal where name = 'rat'"
        ") to ("
        "select from Food where name = 'pea'"
        ")"
    )

    # Who eats the peas?
    pea_eaters = client.command("select expand( in( Eat )) from Food where name = 'pea'")
    for animal in pea_eaters:
        print(animal.name, animal.specie)

### Usage
    Check Pyorient's documentation https://github.com/mogui/pyorient for a
    complete list of commands.

### Default Configuration Values
    'ORIENTDB_AUTO_OPEN': True
    'ORIENTDB_SERVER_PASSWORD': None
    'ORIENTDB_SERVER_USERNAME': 'root'
    'ORIENTDB_HOST': 'localhost'
    'ORIENTDB_PORT' '2424' 
    
    Set 'ORIENTDB_AUTO_OPEN' to False to stop Flask_OrientDB from automatically
    opening a database connection to 'ORIENTDB_CURRENT_DATABASE' (if set) when a
    method requiring a database connection is called.
    
### API Documentation
    class flask_orientdb.OrientDB(app=None)
    This class is used to integrate OrientDB into a Flask application.
    Parameters:	
    
    client_connected():
    Returns whether the client is connected
    
    server_connected():
    returns whether the server is connected
    
    database_connected()
    Returns database connection status to OrientDB server
    
    set_current_db(db_name, db_username=admin, db_password=admin)
    Set the database you want to work on
    
    init_app(app)
    Parameters:	
    This method connects your app with this extension. Flask- OrientDB handles 
    connecting and disconnecting from OrientDB
