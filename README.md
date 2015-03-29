<h3>flask-orientdb</h3>

app = Flask(__name__) <br>
orient_client = OrientDB(your_password, app=app)  <br>
print orient_client.db_list()  <br>
 
