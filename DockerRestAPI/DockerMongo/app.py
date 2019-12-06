import os
import flask
from flask import request,Flask, redirect, url_for, request, render_template, request, flash, abort, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import logging
import json
from forms import LoginForm
from flask_wtf.csrf import CSRFProtect
from flask_restful import reqparse
from testToken import generate_auth_token, verify_auth_token
from password import hash_password, verify_password
from flask_login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, 
                            confirm_login, fresh_login_required)

# Instantiate the app
csrf = CSRFProtect()
app = Flask(__name__)
csrf.init_app(app)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY
api = Api(app) #make api
client = MongoClient('mongodb://db:27017/')
db = client.tododb
Userdb = client.todouserdb

#begining of paste


# step 1 in slides
login_manager = LoginManager()
login_manager.setup_app(app)

# step 6 in the slides
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"

# step 2 in slides 
@login_manager.user_loader
def load_user(user_id):
    dbuserOBj = Userdb.todouserdb.find_one({"id": user_id})
    if dbuserOBj != None:
        user = User(dbuserOBj['username'], dbuserOBj['id'])
        if user.has_valid_token():
            return user
    return None

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return True
    
    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True
    
    def has_valid_token(self):
        dbuser = Userdb.todouserdb.find_one({"id": self.id})
        if verify_auth_token(dbuser['token']) == 'Success':
            return True
        else:
            return False
    
    def is_anonymous(self):
        return False       

#end of paste setup

@app.route('/')
@login_required
def todo():
    return render_template('calc.html')

@app.route('/home')
@login_required
def home():
    return render_template('calc.html')

@app.route("/_new", methods=['GET', 'POST'])
@login_required
@csrf.exempt
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    kmL = request.form.getlist('km')
    totalDist = request.form['distance']
    startTime = request.form['begin_time']
    startDate = request.form['begin_date']
    milesL = request.form.getlist('miles')
    totalDist = float(totalDist)
    for i in range(20):
        if kmL[i] != '':
            try:
                km = float(kmL[i])
                miles = float(milesL[i])
            except:
                flask.flash("error: enter a valid distance".format())
                return redirect('/') 
            if km/totalDist >= 1.2:
                flask.flash("error: your brevet distance is more than 20 percent longer than the total race distance".format())
                return redirect('/') 
            if km < 0:
                flask.flash("error: you entered a negative distance".format())
                return redirect('/') 
            

            brevet_start_time = arrow.get(startDate + 'T' + startTime).format()
            
            app.logger.debug("km= {}".format(km))
            app.logger.debug("totalDist= {}".format(totalDist))
            app.logger.debug("start date= {}".format(startDate))
            app.logger.debug("start time= {}".format(startTime))
            app.logger.debug("request.args: {}".format(request.args))

            open_time = acp_times.open_time(totalDist, km, brevet_start_time)
            close_time = acp_times.close_time(totalDist, km, brevet_start_time)
            item_doc = {
                'distance': km,
                'opentime': open_time,
                'closetime': close_time,
                'location': request.form['location']
            }
            db.tododb.insert_one(item_doc)
    return redirect('/') 

@app.route('/display', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def display():
    if db.tododb.count({}) != 0:
        _items = db.tododb.find().sort( [('distance', 1)] )
        items = [item for item in _items]
        return render_template('display.html', items=items)
    else:
        flask.flash("error: you haven't entered any times".format())
        return redirect('/')

@app.route('/reset', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def reset():
    db.tododb.drop()
    return redirect('/')
#begining of paste

@app.route('/register', methods=['POST', 'GET'])
def register():   
    form = LoginForm()
    user = form.username.data
    app.logger.debug("user: {}".format(user))   
    if form.validate_on_submit():
        if Userdb.todouserdb.find({"username": user},{}).count() == 0:
            pas = hash_password(form.password.data)
            id = Userdb.todouserdb.count({})
            item_doc = { 
                        'id' : id,
                        'username': user,
                        'password': pas,
                        'token': ''
                    }
            Userdb.todouserdb.insert_one(item_doc)
            one = Userdb.todouserdb.find_one({"username": user})
            app.logger.debug("userob: {}".format(one['id']))
            return redirect(url_for("login"))
        else:
            flash("that username is already taken")
    one = Userdb.todouserdb.find_one({"username": user})
    app.logger.debug("userob: {}".format(one))
    return render_template('register.html',  title='Register', form=form)
# step 3 in slides

# This is one way. Using WTForms is another way.
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        username = form.username.data
        if Userdb.todouserdb.find({"username": username}).count() == 1:
            dbuser = Userdb.todouserdb.find_one({"username": username})
            if verify_password(form.password.data, dbuser['password']):
                user = User(username,dbuser['id'])
                login_user(user, form.remember_me.data)
                token = generate_auth_token()
                Userdb.todouserdb.update_one(dbuser, {'$set': {'token': token}})
                flash('Logged in successfully.')
                return redirect('/')
            else:
                flash('incorrect Password.')
        else:
            flash('unregistered user')
    return render_template('login.html',  title='Sign In', form=form)


# step 5 in slides
@app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash("Reauthenticated.")
        return redirect(request.args.get("next") or url_for("login"))
    return redirect(url_for("login"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("login"))
#end of paste

@app.route('/api/register/<id>')
@login_required
def users(id): #returns a resources with users usernames based on id
    try:
        id = int(id)
        user = Userdb.todouserdb.find_one({"id": id})
        if user != None:
            return jsonify({'username': user['username'], 'location': id}), 201
        else:
            return abort(400), 400
    except:
        return abort(400), 400

@app.route('/api/token')
@login_required
def get_auth_token(): # returns a valid token in ascii format
    return jsonify({'token': generate_auth_token().decode('ascii') })

@app.route('/<id>')
@login_required
def default(id): # redirects all api request to default Json format
    return redirect('/'+id+'/json')

@app.route('/<id>/json')
@login_required
def Alljson(id): #creates 3 resources of open and close times in json format
    if db.tododb.find().count() != 0:
        app.logger.debug("here".format())
        db.tododb.find().sort( [('distance', 1)] )
        app.logger.debug("here".format())
        top = request.args.get('top', default = 20, type = int)
        _items = db.tododb.find({},{ "_id": 0, "opentime": 1, "closetime": 1}).limit(top)
        items = [item for item in _items]
        open = []
        close = []
        app.logger.debug("here3".format())
        for Item in items:
            open.append(Item['opentime'])
            close.append(Item['closetime'])
        if id == 'listAll': 
            app.logger.debug("here3".format())
            return jsonify({'opentimes': open, 'closetimes': close})
        if str(id) == 'listCloseOnly':
            return jsonify({'closetimes': close})
        if str(id) == 'listOpenOnly':
            return jsonify({'opentimes': open})
        else:
            return abort(401), 401
    else:
        return abort(404), 404

@app.route('/<id>/csv')
@login_required #creates 3 resouces of open and close times in csv format
def Allcsv(id):
    db.tododb.find().sort( [('distance', 1)] )
    top = request.args.get('top', default = 20, type = int)
    _items = db.tododb.find({},{ "_id": 0, "opentime": 1, "closetime": 1}).limit(top)
    items = [item for item in _items]
    open = 'opentimes,'
    close = 'closetimes,'
    for Item in items:
        open += Item['opentime'] + ',' 
        close += Item['closetime'] + ','
    if str(id) == 'listAll': 
        return  open + close
    if str(id) == 'listCloseOnly':
        return close
    if str(id) == 'listOpenOnly':
        return open
    else:
        return abort(401), 401

@app.errorhandler(404)
def error_404(erorr): #handles unfound urls
    return render_template("404.html"), 404 #data, 404


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80, debug=True)

# Create routes
# Another way, without decorators









