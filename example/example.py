from flask import Flask
from flask.ext.orientdb import OrientDB


if __name__ == '__main__':
    app = Flask(__name__)
    client = OrientDB(app=app, server_password='B0FC9CF1CBEAD07351C4C30197C43BE2D611E94AFAFA7EF4B4AAD3262F7907DB')
