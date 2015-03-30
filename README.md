<h3>Flask-OrientDB</h3>
Flask-OrientDB simplifies using OrientDB with Flask by providing an interface to Pyorient Python driver.
### Example 
    from flask import Flask
    from flask.ext.orientdb import OrientDB
    
    
    if __name__ == '__main__':
        app = Flask(__name__)
        client = OrientDB(app=app, server_username='my_username', server_password='your_password')
        if not client.db_exists('animal'):
            client.db_create('animal')
        db_list = client.db_list()
        client.command("create class Animal extends V")
        client.command("insert into Animal set name = 'rat', specie = 'rodent'")
        db_size = client.db_size()

### Default Configuration Values
    'ORIENTDB_CURRENT_DATABASE': None
    'ORIENTDB_DATABASE_USERNAME': 'admin'
    'ORIENTDB_DATABASE_PASSWORD': 'admin'
    'ORIENTDB_AUTO_OPEN': True
    'ORIENTDB_SERVER_PASSWORD': None
    'ORIENTDB_SERVER_USERNAME': 'root'
    'ORIENTDB_HOST': 'localhost'
    'ORIENTDB_PORT' '2424'
    
    Set 'ORIENTDB_AUTO_OPEN' to False to stop Flask_OrientDB from automatically
    opening a database connection to 'ORIENTDB_CURRENT_DATABASE' (if set) when a method requiring a 
    database connection is called.
    
### Edit Configuration
    client['ORIENTDB_CURRENT_DATABASE'] = 'new_db'
