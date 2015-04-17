from flask.ext.orientdb import OrientDB
from flask import Flask

def setup_db():
    client.db_create('animal', 'graph', 'plocal')
    client.set_db('animal')
    # Create the Vertex Animal
    client.command("create class Animal extends V")

    # # Insert a new value
    client.command("insert into Animal set name = 'rat', specie = 'rodent'")
    # Create the vertex and insert the food values

    client.command('create class Food extends V')
    client.command("insert into Food set name = 'pea', color = 'green'")

     # # Create the edge for the Eat action
    client.command('create class Eat extends E')

    # Lets the rat likes to eat pea
    eat_edges = client.command(
        "create edge Eat from ("
        "select from Animal where name = 'rat'"
        ") to ("
        "select from Food where name = 'pea'"
        ")"
    )

if __name__ == '__main__':
    app = Flask(__name__)
    client = OrientDB(app=app, server_pw='B0FC9CF1CBEAD07351C4C30197C43BE2D611E94AFAFA7EF4B4AAD3262F7907DB')
    with app.app_context():
        if not client.db_exists():
            setup_db()