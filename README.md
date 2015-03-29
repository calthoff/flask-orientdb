<h3>flask-orientdb</h3>

app = Flask(__name__)
orient_client = OrientDB("B0FC9CF1CBEAD07351C4C30197C43BE2D611E94AFAFA7EF4B4AAD3262F7907DB", app=app)
print orient_client.db_list()
