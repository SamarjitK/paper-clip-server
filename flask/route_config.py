from flask import Flask
from api.api_student import *
from db.db_config import *
# app reference
app = Flask(__name__)

# This method executes before any API request
@app.before_request
def before_request():
    g.db = get_db()


# This method returns students list
# and by default method will be GET
@app.route('/api/students')
def get_students_list():
    return get_student()

# This is POST method which stores students details.
@app.route('/api/storestudents', methods=['POST'])
def store_student_data():
    return store_student()

# This method executes after every API request.
@app.after_request
def after_request(response):
    return response
