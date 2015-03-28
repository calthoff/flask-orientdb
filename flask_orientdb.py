import pyorient



client = pyorient.OrientDB("localhost", 2429)
session_id = client.connect( "root", "B0FC9CF1CBEAD07351C4C30197C43BE2D611E94AFAFA7EF4B4AAD3262F7907DB")
#client.db_create( 'test', pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY )
t = client.db_list()
print type(session_id)