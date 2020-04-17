from flask import Flask, request, url_for, jsonify,redirect, render_template
from flask_pymongo import PyMongo
import requests
import json
from pymongo import MongoClient
from bson import json_util
import win32api


application = app = Flask (__name__)
client = MongoClient("mongodb://thanmai:thanmai@thanmaik-shard-00-00-xfua4.mongodb.net:27017,thanmaik-shard-00-01-xfua4.mongodb.net:27017,thanmaik-shard-00-02-xfua4.mongodb.net:27017/test?ssl=true&replicaSet=ThanmaiK-shard-0&authSource=admin&retryWrites=true&w=majority")



@app.route('/')
def index():
    return render_template('index.html')

#use this route only if the data is to be pulled manually
@app.route('/mnlrefresh')
def ref():
    db = client.weather
    while True:
        r = requests.get("https://www.ncdc.noaa.gov/cag/global/time-series/globe/land_ocean/ytd/12/1880-2016.json")
        if r.status_code == 200:
            data = r.json()
            db.weather.insert_one(data)
            break
        else:
            exit()
    return render_template('index.html')


@app.route('/weather')
def wthr():
    return render_template('weather.html')


@app.route('/weather/wresult',methods = ['POST'])
def rslt():
    db = client.weather
    yr = request.form['year']
    collection = db['weather']
    cursor = collection.find({})
    if(yr == ''):
        return'''
        <p>Please specify a value.</p>
        '''
    
    elif(int(yr)<1880 or int(yr)>2016):
        
        return '''
        <p>Please go back and enter the value within the specified range.</P>
        '''
    else: 
        for document in cursor:
            final = json.dumps(document, indent=4, default=json_util.default)
            file1=json.loads(final)
        rprt = file1['data'][yr]

        return render_template('wresult.html',rprt=rprt)

@app.route("/visualize")
def vis():
    return render_template("tableau.html")

