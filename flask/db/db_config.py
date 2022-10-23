from flask import current_app, g
from flask_pymongo import PyMongo

from werkzeug.local import LocalProxy
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId

# The method returns the database instance
def get_db():
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db
       
    return db

db = LocalProxy(get_db)

def get_sample():
    try:
        return str(db["session_list"].find_one().get("next_session_id"))
    except Exception as e:
        return e

def add_session_ID():
    try:
        x = db["session_list"].find_one().get("next_session_id")
        db["session_list"].update_one(
            { "id": "list"},
            { "$push": {"session_ids": x}}
        )
        db["session_list"].update_one(
            { "id": "list"},
            { "$set": {"next_session_id": x + 1}}
        )
        return str(x)
    except Exception as e:
        return e

def verify_ID(session_id):
    try:
        if int(session_id) in db["session_list"].find_one().get("session_ids") :
            return "True"
        return "False"
    except Exception as e:
        return e

def get_player_list(session_id):
    try:
        return db["sessions"].find_one({"session_id": int(session_id)}).get("player_ids")
    except Exception as e:
        return e

def store_player(name, session_id):
    try:
        if name not in db["sessions"].find_one({"session_id": int(session_id)}).get("player_ids"):
            db["sessions"].update_one(
                { "session_id": int(session_id)},
                { "$push": {"player_ids": name}}
            )

            db["sessions"].update_one(
                { "session_id": int(session_id)},
                { "$push": {"player": {{"name": str(name), 
                                        "question": "", 
                                        "answer": "",
                                        "score": 0}}}}
            )
            return "True"
        return "False"
    except Exception as e:
        return e

def remove_player(name, session_id):
    try:
        if name in db["sessions"].find_one({"session_id": int(session_id)}).get("player_ids"):
            db["sessions"].update_one(
                { "session_id": int(session_id)},
                { "$pull": {"player_ids": name}}
            )
            return "True"
        return "False"
    except Exception as e:
        return e

def get_score(name, session_id):
    try:
        x = list(db["sessions"].find_one({"session_id": int(session_id)}).get("players"))
        for cur in x:
            if cur["name"] == name:
                return str(cur["score"])
    except Exception as e:
        return e

def update_score(name, session_id, score):
    try:
        x = list(db["sessions"].find_one({"session_id": int(session_id)}).get("players"))
        for i in range(len(x)):
            x[i].name == name
            if cur["name"] == name:
                db["sessions"].update_one(
                    {"session_id": int(session_id), "session_id.players.name": str(name)},
                    {"$inc": {"players.$[].score": int(score)}})
                return "True"
    except Exception as e:
        return e

def leaderboard(session_id):
    try:
        l = []
        for x in get_player_list(session_id):
            db["sessions"].find_one({session_id: int(session_id)})
        print("hi")
    except Exception as e:
        return e