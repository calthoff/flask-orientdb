from flask import Flask
from flask.ext.orientdb import OrientDB

app = Flask(__name__)
app.debug = True
client = OrientDB(app=app, server_password=your_password)
client.set_current_db('animal')

@app.route("/")
def cheese_eating_animals():
    client.query("select * from Animal")
    animal_list = []
    cheese_eaters = client.command("select expand( in( Eat )) from Food where name = 'pea'")
    return ','.join([cheese_eaters[0].name, cheese_eaters[0].species])

if __name__ == "__main__":
        app.run()