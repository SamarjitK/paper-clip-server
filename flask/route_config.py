from flask import Flask, g, Blueprint
from api.api_player import *
from db.db_config import *
# app reference
# This method executes before any API request
# @app.before_request
# def before_request():
    # g.db = get_db()

router = Blueprint('routes', __name__, )

@router.route("/")
def hello():
    return get_sample()

@router.route('/verify_ID/<id>')
def r_verify_ID(id):
    return verify_ID(id)

@router.route('/get_player_list/<session_id>')
def r_get_list(session_id):
    return get_player_list(session_id)

@router.route('/leaderboard/<session_id>')
def r_leaderboard(session_id):
    return leaderboard(session_id)

@router.route('/get_score/<session_id>/<name>')
def r_get_score(session_id, name):
    return get_score(name, session_id)

# This is POST method which stores students details.
@router.route('/add_session_ID', methods=['POST', 'GET'])
def r_add_session_ID():
    return add_session_ID()

@router.route('/store_player/<session_id>/<name>', methods=['POST', 'GET'])
def r_store_player(session_id, name):
    return store_player(name, session_id)

@router.route('/remove_player/<session_id>/<name>', methods=['POST', 'GET'])
def r_remove_player(session_id, name):
    return remove_player(name, session_id)

@router.route('/update_score/<session_id>/<name>/<score>', methods=['POST', 'GET'])
def r_update_score(session_id, name, score):
    return update_score(name, session_id, score)

# This method executes after every API request.
@router.after_request
def after_request(response):
    return response
