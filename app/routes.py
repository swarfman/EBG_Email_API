from flask import render_template, request, jsonify, make_response
from app import app, db
from app.models import User, Email
import sqlalchemy
from flask_migrate import Migrate
from flask_cors import CORS
import requests

@app.route('/')
def homepage():

    return render_template('index.html')


@app.route('/addSTEmail', methods=['POST'])
def add_STEmail():
    info= request.get_json() or {}
    #print(info)
    username = info["username"]
    user = User.query.filter_by(username=username).first()

    print(info['username'])
    email_item = Email(
         body=info['body'] ,
         user=user,
         email_type=info["email_type"]
     )
    print(email_item)

    db.session.add(email_item)
    db.session.commit()
    return jsonify({'response': 'ok'})


@app.route('/login', methods=['POST'])
def login():
    info= request.get_json() or {}

    incorrect_password = {
        'status_code': 400,
        'message': 'password incorrect'
    }

    username = info["username"]
    password = info["password"]
    user = User.query.filter_by(username=username).first()

    if user.password == password:
        return jsonify({'response': 'ok'})
    else:
        return make_response(jsonify(incorrect_password), 400)

@app.route('/getAllEmails', methods=['POST'])
def allEmails():
    info= request.get_json() or {}
    #print(info)
    username = info["username"]
    user = User.query.filter_by(username=username).first()
    JSON_object = user.to_dict()
    return jsonify({"status_code": 200, "data": JSON_object})

@app.route('/deleteEmail/<id>', methods=['DELETE'])
def deleteEmail(id):
    info= request.get_json() or {}
    #print(info)
    username = info["username"]
    user = User.query.filter_by(username=username).first()
    currentEmail = Email.query.get(id)
    user.emails.remove(currentEmail)
    db.session.commit()
    JSON_object = user.to_dict()
    return jsonify({"status_code":200,"data":JSON_object})


@app.route('/addUser', methods=['POST'])
def addUser():
    info = request.get_json() or {}

    item = User(
        name = info["full_name"],
        username = info["username"],
        password = info["password"]
    )

    db.session.add(item)
    db.session.commit()
    return jsonify({"response": "ok"})

@app.route('/index')
def index():
    user = {'username': 'Sean'}

    return render_template('index.html', title='Home', user=user)

