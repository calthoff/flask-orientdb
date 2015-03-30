from flask import Flask
from flask.ext.orientdb import OrientDB


if __name__ == '__main__':
    app = Flask(__name__)
    client = OrientDB(app=app, password='B0FC9CF1CBEAD07351C4C30197C43BE2D611E94AFAFA7EF4B4AAD3262F7907DB')
    if not client.db_exists('test_db'):
        client.db_create('test_db')


    db_list = client.db_list()
    print db_list
    # print client.app.config.get('ORIENTDB_CURRENT_DATABASE')
    client['ORIENTDB_CURRENT_DATABASE'] = 'cory3'
    # print client.app.config.get('ORIENTDB_CURRENT_DATABASE')
    print client.db_size()
    # client.db_open('test_db')
    # client.command("create class Animal extends V")
    # client.command("insert into Animal set name = 'rat', specie = 'rodent'")