import os
import configparser
from flask import Flask, request, abort
from flask_pymongo import PyMongo
from route_config import router
from flask.json import JSONEncoder
from flask_cors import CORS
from bson import json_util, ObjectId
from datetime import datetime, timedelta

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config["MONGO_URI"] = config['PROD']['DB_URI']
    CORS(app)
    app.json_encoder = MongoJsonEncoder
    app.register_blueprint(router)
    return app

app = create_app()

if __name__ == "__main__":
    app.run()
