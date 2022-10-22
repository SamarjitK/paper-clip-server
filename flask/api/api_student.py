from flask import request, g
import uuid
from utils.uitils import *


# This method is to fetch the students details
def get_student():
    if request.method == 'GET':
        data_cursor = g.db.execute("SELECT * "
                                   "FROM StudentTable")
        data = data_cursor.fetchall()
        user_data = [{'ID': row[0], 'NAME': row[1],
                      'RollNo': row[2], 'Address': row[3],
                      'CLASS': row[4], 'DOB': row[5],
                      'Gender': row[6]} for row in data]
        return success_response(user_data,
                                "These are the students "
                                "stored into records")


# This method is to store the students details
def store_student():
    if request.method == 'POST':
        data = request.json
        user_cursor = g.db.execute("SELECT * FROM "
                                   "StudentTable WHERE "
                                   "NAME=? OR RollNo=? ",
                                   (data["name"],
                                    data["RollNo"]))
        if len(user_cursor.fetchall()) >= 1:
            return success_message("Student details is "
                                   "already Stored !!")
        else:
            query = ('INSERT INTO StudentTable (ID, NAME, RollNo, '
                     'Address, CLASS, DOB, gender) '
                     ' VALUES (:ID, :NAME, :RollNo, '
                     ':Address, :CLASS, :DOB, :GENDER);')
            param = {
                'ID': str(uuid.uuid4()),
                'NAME': data["name"],
                'RollNo': data["RollNo"],
                'Address': data["address"],
                'CLASS': data["class"],
                'DOB': data["dob"],
                'GENDER': data["gender"]
            }
            g.db.execute(query, param)
            g.db.commit()
            data_cursor = g.db.execute("SELECT * FROM "
                                       "StudentTable WHERE NAME=? OR "
                                       "RollNo=? ",
                                       (data["name"],
                                        data["RollNo"]))
            data = data_cursor.fetchall()
            user_data = [{'ID': row[0], 'NAME': row[1],
                          'RollNo': row[2], 'Address': row[3],
                          'CLASS': row[4], 'DOB': row[5],
                          'Gender': row[6]} for row in data]
            return success_response(user_data,
                                    "These are the students "
                                    "stored into records")
    else:
        return error_response("Invalid method[GET/POST]")
