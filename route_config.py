from flask import Flask, g, Blueprint
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

#verifies the session_id to see if its valid
#returns 0 if the session_id is valid
#returns 1 if the session_id exists, but is inactive
#returns 2 if the session_id does not exist
@router.route('/verify_id/<session_id>')
def r_verify_id(session_id):
    return verify_ID(session_id)

#returns the list of players as an array
@router.route('/get_player_list/<session_id>')
def r_get_list(session_id):
    return get_player_list(session_id)

#returns the names of the top 3 players
@router.route('/leaderboard/<session_id>')
def r_leaderboard(session_id):
    return leaderboard(session_id)

#returns the score of the player with the given name
@router.route('/get_score/<session_id>/<name>')
def r_get_score(session_id, name):
    return get_score(name, session_id)

#returns the answer of the given player
@router.route('/get_answer/<session_id>/<name>')
def r_get_answer(session_id, name):
    return get_answer(name, session_id)

#returns the question of the given player
@router.route('/get_question/<session_id>/<name>')
def r_get_question(session_id, name):
    return get_question(name, session_id)
    
#This is POST method which stores students details.
#creates a session with the next available session_id
@router.route('/add_session_ID', methods=['POST', 'GET'])
def r_add_session_ID():
    return add_session_ID()

#creates a player with the given name in the given session
#returns true if the player was created
#returns false is the name was already taken
@router.route('/store_player/<session_id>/<name>', methods=['POST', 'GET'])
def r_store_player(session_id, name):
    return store_player(name, session_id)

#removes a player with the given name from the given session
#returns true is the player was removed
#returns false if there is no player with the given name
@router.route('/remove_player/<session_id>/<name>', methods=['POST', 'GET'])
def r_remove_player(session_id, name):
    return remove_player(name, session_id)

#updates the score of the given player by the given amount
@router.route('/update_score/<session_id>/<name>/<score>', methods=['POST', 'GET'])
def r_update_score(session_id, name, score):
    return update_score(name, session_id, score)

#updates the answer of the given player
@router.route('/update_answer/<session_id>/<name>/<answer>', methods=['POST', 'GET'])
def r_update_answer(session_id, name, answer):
    return update_answer(name, session_id, answer)

#updates the question of the given player
@router.route('/update_question/<session_id>/<name>/<question>', methods=['POST', 'GET'])
def r_update_question(session_id, name, question):
    return update_question(name, session_id, question)

#deactivates the session_id given
@router.route('/deactivate/<session_id>', methods=['POST', 'GET'])
def r_deactivate(session_id):
    return deactivate(session_id)

@router.route('/set_phase/<session_id>/<num>', methods=['POST', 'GET'])
def r_set_phase(session_id,num):
    return set_phase(session_id,num)

@router.route('/get_phase/<session_id>')
def r_get_phase(session_id):
    return get_phase(session_id)

# This method executes after every API request.
@router.after_request
def after_request(response):
    return response
