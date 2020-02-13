"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap, sha256
from models import db, Users, Objects, Resource_Centers,Days
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)
from send_sms import my_function

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'dfsh3289349yhoelqwru9g'
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def my_users():
    if request.method == 'GET':
        users = Users.query.all()
        if not users:
            return jsonify({'msg': 'User not found'}), 404

        return jsonify( [x.serialize() for x in users] ), 200


@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        body = request.get_json()

        db.session.add(Users(
            first_name = body["first_name"],
            last_name = body["last_name"],
            email = body["email"],
            password = sha256(body['password'])
        ))
        
        db.session.commit()
        return jsonify({
            'msg': 'User Added!'
        })

@app.route('/add_days', methods=['POST'])
def add_day():
    if request.method == 'POST':
        body = request.get_json()

        db.session.add(Days(
            first_day = body["first_day"],
            second_day = body["second_day"],
            user_id = body["user_id"]
        ))
        
        db.session.commit()
        return jsonify({
            'msg': 'Day Added!',
            "first_day": body["first_day"],
            "second_day": body["second_day"]
        })

@app.route('/get_days', methods=['POST'])
def days_picked():
    if request.method == 'POST':
        body = request.get_json()

        days = Days.query.filter_by(user_id=body['userId'])
        if not days:
            return jsonify({'msg': 'No days found'}), 404

        return jsonify( [x.serialize() for x in days ] ), 200



@app.route('/login', methods=['POST'])
def handle_login():

    body = request.get_json()

    user = Users.query.filter_by(email=body['email'], password=sha256(body['password'])).first()

    if not user:
        return 'User not found', 404
    if not user.email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not user.password:
        return jsonify({"msg": "Missing password parameter"}), 400

    return jsonify({
              'token': create_jwt(identity=1),
              'id': user.id,
              'email': user.email,
              'first_name': user.first_name,
              'last_name': user.last_name
              })


@app.route('/sendmsg', methods=['POST'])
def notification():
    my_function()

#     body = request.get_json()
    
#     if 'message' not in body:
#         raise APIException('must specify message in body', 400)

#     send_sms(body['message'])
    
#     return jsonify({'msg':'message sent!'})


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)