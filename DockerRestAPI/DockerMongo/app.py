import os
import flask
from flask import request,Flask, redirect, url_for, request, render_template
from flask_restful import Resource, Api
from pymongo import MongoClient
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import logging
import json
from bson import json_util
from flask_restful import reqparse
from flask import request

# Instantiate the app
app = Flask(__name__)

CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY
api = Api(app) #make api
client = MongoClient('mongodb://db:27017/')
db = client.tododb

@app.route('/')
def todo():
    return render_template('calc.html')

@app.route("/_new", methods=['GET', 'POST'])
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    km = request.form['km']
    totalDist = request.form['distance']
    startTime = request.form['begin_time']
    startDate = request.form['begin_date']
    totalDist = float(totalDist)
    try:
        km = float(km)
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
def display():
    if db.tododb.count({}) != 0:
        _items = db.tododb.find().sort( [('distance', 1)] )
        items = [item for item in _items]
        return render_template('display.html', items=items)
    else:
        flask.flash("error: you haven't entered any times".format())
        return redirect('/')

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    db.tododb.drop()
    return redirect('/')


class Allj(Resource):
    def get(self, id):
        db.tododb.find().sort( [('distance', 1)] )
        _items = db.tododb.find({},{ "_id": 0, "opentime": 1, "closetime": 1})
        items = [item for item in _items]
        open = []
        close = []
        for Item in items:
            open.append(Item['opentime'])
            close.append(Item['closetime'])
        if str(id) == 'listAll':
            return {'opentimes': open, 'closetimes': close} 
        if str(id) == 'listCloseOnly':
            return {'closetimes': close}
        if str(id) == 'listOpenOnly':
            return {'opentimes': open}
        else:
            return "api not found"

class Allc(Resource):
    def get(self, id):
        db.tododb.find().sort( [('distance', 1)] )
        _items = db.tododb.find({},{ "_id": 0, "opentime": 1, "closetime": 1})
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
            return "api not found"      

# Create routes
# Another way, without decorators
api.add_resource(Allj, '/<id>', '/<id>/json')
api.add_resource(Allc, '/<id>/csv')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80, debug=True)

# Create routes
# Another way, without decorators









