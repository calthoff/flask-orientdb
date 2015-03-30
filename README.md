<h3>flask-orientdb</h3>
Flask-OrientDB simplifies using OrientDB with Flask by providing an interface to Pyorient Python driver.
### Example 
    from flask import Flask
    from flask.ext.orientdb import OrientDB
    
    
    if __name__ == '__main__':
        app = Flask(__name__)
        client = OrientDB(app=app, password='your_password')
        if not client.db_exists('animal'):
            client.db_create('animal')
        db_list = client.db_list()
        client.command("create class Animal extends V")
        client.command("insert into Animal set name = 'rat', specie = 'rodent'")
        db_size = client.db_size()

### Default Configuration
    'ORIENTDB_CURRENT_DATABASE'
    'ORIENTDB_DATABASE_USERNAME'
    'ORIENTDB_DATABASE_PASSWORD'
    'ORIENTDB_AUTO_OPEN'
    'ORIENTDB_SERVER_PASSWORD'
    'ORIENTDB_SERVER_USERNAME'
    'ORIENTDB_HOST'
    'ORIENTDB_PORT'
    
### Edit Configuration
    client['ORIENTDB_CURRENT_DATABASE'] = 'new_db'
