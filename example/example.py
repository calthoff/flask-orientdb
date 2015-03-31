from flask import Flask
from flask.ext.orientdb import OrientDB


if __name__ == '__main__':
    app = Flask(__name__)
    client = OrientDB(app=app, server_password='B0FC9CF1CBEAD07351C4C30197C43BE2D611E94AFAFA7EF4B4AAD3262F7907DB')


    client.db_size()
    def _my_callback(for_every_record):
        print(for_every_record)


    #print client.db_exists('cory')
    #print client.query("select from my_class", 10, '*:0')

    # if not client.db_exists('test_db'):
    #     client.db_create('test_db')

    # db_list = client.db_list()
    # print db_list
    # # print client.app.config.get('ORIENTDB_CURRENT_DATABASE')
    # client['ORIENTDB_CURRENT_DATABASE'] = 'cory3'
    # # print client.app.config.get('ORIENTDB_CURRENT_DATABASE')
    # print client.db_size()
    # # client.db_open('test_db')
    # # client.command("create class Animal extends V")
    # # client.command("insert into Animal set name = 'rat', specie = 'rodent'")







       #
       #
       # # TODO load record? check if needed for other methods
       #      # if name == 'db_create' and not args:
       #      #     args = (pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY)
       #      # TODO check if this is needed
       #      if name == 'db_exists' and len(args) == 1:
       #          db_name = args[0]
       #          args = (db_name, pyorient.STORAGE_TYPE_MEMORY)
       #      if name == 'data_cluster_add' and len(args) == 1:
       #          cluster_name = args[0]
       #          args = (cluster_name, pyorient.CLUSTER_TYPE_PHYSICAL)

