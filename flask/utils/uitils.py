import json
from flask import make_response

JSON_MIME_TYPE = 'application/json; charset=utf-8'
STATUS = 'success'


def json_response(data='', status=200, headers=None):
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = JSON_MIME_TYPE

    return make_response(data, status, headers)


def error_response(error):
    error = json.dumps({'status': 'failed',
                        'error': error})
    return json_response(error)


def success_response(result, message=''):
    format = {'status': 'success',
                  'message': message,
                  'result': result}
    return json_response(json.dumps(format))


def success_message(message):
    format = {'status': 'success',
              'result': message}

    return json_response(json.dumps(format))
