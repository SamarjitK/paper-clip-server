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

        db["sessions"].insert_one({"session_id": x,
                                   "player_ids":[],
                                   "players": [],
                                   "active": True,
                                   "phase": 0}
        )
        return str(x)
    except Exception as e:
        return e

def verify_ID(session_id):
    try:
        if int(session_id) in db["session_list"].find_one().get("session_ids"): 
            if db["sessions"].find_one({"session_id": int(session_id)})["active"]:
                return "0"
            return "1"
        return "2"
    except Exception as e:
        return e

def get_player_list(session_id):
    try:
        return db["sessions"].find_one({"session_id": int(session_id)}).get("player_ids")
    except Exception as e:
        return e

def store_player(name, session_id):
    try:
        if str(name) not in get_player_list(session_id):
            db["sessions"].update_one(
                { "session_id": int(session_id)},
                { "$push": {"player_ids": str(name)}}
            )

            db["sessions"].update_one(
                { "session_id": int(session_id)},
                { "$push": {"players": {"name": str(name), 
                                        "question": "", 
                                        "answer": "",
                                        "score": int(0)}}}
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

            db["sessions"].update_one(
                { "session_id": int(session_id)},
                { "$pull": {"players": {"name": str(name)}}}
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
            if x[i]["name"] == str(name):
                db["sessions"].update_one(
                    {"session_id": int(session_id)},
                    {"$inc": {f"players.{i}.score": int(score)}}
                )
                return str(x[i]["score"] + int(score))
    except Exception as e:
        return e

def get_phase(session_id):
    try:
        return str(db["sessions"].find_one({"session_id": int(session_id)}).get("phase"))
    except Exception as e:
        return e

def set_phase(session_id,num):
    try:
        db["sessions"].update_one(
            { "session_id": int(session_id)},
            { "$set": {"phase": int(num)}}
        )
        return str(db["sessions"].find_one({"session_id": int(session_id)}).get("phase"))
    except Exception as e:
        return e

def get_answer(name, session_id):
    try:
        x = list(db["sessions"].find_one({"session_id": int(session_id)}).get("players"))
        for cur in x:
            if cur["name"] == name:
                return str(cur["answer"])
    except Exception as e:
        return e

def update_answer(name, session_id, answer):
    try:
        x = list(db["sessions"].find_one({"session_id": int(session_id)}).get("players"))
        for i in range(len(x)):
            if x[i]["name"] == str(name):
                db["sessions"].update_one(
                    {"session_id": int(session_id)},
                    {"$set": {f"players.{i}.answer": str(answer)}})
                return str(x[i]["score"])
    except Exception as e:
        return e

def get_question(name, session_id):
    try:
        x = list(db["sessions"].find_one({"session_id": int(session_id)}).get("players"))
        for cur in x:
            if cur["name"] == name:
                return str(cur["question"])
    except Exception as e:
        return e

def update_question(name, session_id, question):
    try:
        x = list(db["sessions"].find_one({"session_id": int(session_id)}).get("players"))
        for i in range(len(x)):
            if x[i]["name"] == str(name):
                db["sessions"].update_one(
                    {"session_id": int(session_id)},
                    {"$set": {f"players.{i}.question": str(question)}})
                return str(question)
    except Exception as e:
        return e

def deactivate(session_id):
    try:
        db["sessions"].update_one(
            { "session_id": int(session_id)},
            { "$set": {"active": False}}
        )
        return "True"
    except Exception as e:
        return e

def leaderboard(session_id):
    try:
        x = list(db["sessions"].find_one({"session_id": int(session_id)}).get("players"))
        sorted_list= sorted(x, key=lambda x: x["score"], reverse=True)
        sliced_list = sorted_list[0:3]
        return list([cur["name"] for cur in sliced_list])
    except Exception as e:
        return e