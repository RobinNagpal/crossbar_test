import json
import logging
import os
import uuid

import jwt
from flask import Flask, jsonify
from flask import abort
from flask import request
from flask_cors import CORS, cross_origin
from flask import Response

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

from routes.notification import NotificationService

app = Flask(__name__)
CORS(app, support_credentials=True)

jwt_secret = 'jwt_secret'

users = [
    {
        'id': "6a1290b4-a503-4b64-a953-3e89d7cb334b",
        'name': 'Robin Nagpal',
        'email': 'robinnagpal.tiet@gmail.com',
        'password': 'secret'
    },
    {
        'id': str(uuid.uuid4()),
        'name': 'Guneet Kaur',
        'email': '2013nibor@gmail.com',
        'password': 'secret'
    },
    {
        'id': str(uuid.uuid4()),
        'name': 'Joe',
        'email': 'joe@gmail.com',
        'password': 'secret'
    }
]

notification_service = NotificationService()


@app.route('/auth/users', methods=['GET'])
@cross_origin()
def get_users():
    return jsonify({'users': users})


@app.route('/auth/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_task():
    request_json = json.loads(request.data)
    # request_json = request.json
    if not request_json or not 'email' in request_json:
        abort(400)
    if not request_json or not 'password' in request_json:
        abort(400)
    user = find_user_by_email(request_json['email'])
    if not user:
        abort(400)
    if not request_json['password'] == user['password']:
        abort(400)
    user['token'] = jwt_encode(user)
    return jsonify(user), 200


@app.route('/auth/user', methods=['GET'])
@cross_origin()
def get_user():
    token = request.args.get('token')
    decoded = jwt_decode(token)
    user_id = decoded['user_id']
    print(decoded, user_id)
    user = find_user_by_id(user_id)

    return jsonify(user)


@app.route('/notification/notify', methods=['POST'])
@cross_origin(supports_credentials=True)
def send_message_to_user():
    request_json = json.loads(request.data)

    if not request_json or not 'user_id' in request_json:
        abort(400)

    if not request_json or not 'message' in request_json:
        abort(400)

    print("will call notification_service.publish_message to send message")

    notification_service.publish_message(request_json['user_id'], request_json['message'])
    return jsonify(request_json, 201)


def jwt_encode(user):
    payload = {
        'user_id': str(user['id']),
        'email': user['email']
    }
    encode = jwt.encode(payload, jwt_secret, algorithm='HS256')
    return str(encode, 'utf-8')


def jwt_decode(token):
    return jwt.decode(token, jwt_secret, algorithms='HS256')


def find_user_by_email(email):
    for user in users:
        if user['email'] == email:
            return user


def find_user_by_id(id):
    for user in users:
        if user['id'] == id:
            return user


logging.getLogger('flask_cors').level = logging.DEBUG
logging._defaultFormatter = logging.Formatter(u"%(message)s")

if __name__ == '__main__':
    app.run(debug=True)
