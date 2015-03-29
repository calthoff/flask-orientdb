<h3>flask-orientdb</h3>

app = Flask(__name__)
orient_client = OrientDB(your_password, app=app)
print orient_client.db_list()
