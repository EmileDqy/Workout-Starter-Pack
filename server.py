from flask import Flask, request, render_template, jsonify, json, url_for, redirect
from flask_wtf.csrf import CSRFProtect
import sys
import os
import webbrowser
import subprocess
import signal
import time

from utils import getAbsPath, restartProgram
import config
from notificationsManager import notify

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, static_url_path="/static", static_folder=static_folder, template_folder=template_folder)
else:
    app = Flask(__name__, static_url_path='/static')

lasttrigger = [0, -1]

tray = None

PORT = 5000
HTML = "workoutGUI"

ListExercices = []
INDEX = 0
VALUE = 1
TYPE = 0
NAME = ""

csrf = CSRFProtect(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY 

@csrf.exempt
@app.route('/process',methods=['POST'])
def process():
    global ListExercices, INDEX, VALUE, TYPE, NAME, tray, lasttrigger
    
    #Update the exercice's information (iterations)
    config.updateExercice(ListExercices[INDEX][0])

    if INDEX < len(ListExercices) - 1:
        INDEX += 1
        VALUE = ListExercices[INDEX][1]
        TYPE = ListExercices[INDEX][2]
        NAME = ListExercices[INDEX][0]
        isLast = 0
        if INDEX == len(ListExercices) - 1:
            isLast = 1
        data = {
            "name" : NAME,
            "value" : VALUE,
            "type" : TYPE,
            'isLast' : isLast
        }
        notify("Workout Starter Pack", "Next exercice : " + NAME + " " + ((TYPE == 0) and "x"+ str(VALUE) or str(VALUE)+"s"), 5)
        return render_template(HTML + '.html',  data=data)
    else:
        config.updateLastTrigger(*lasttrigger)
        notify("Workout Starter Pack", "Session finished!", 5, threaded=False)
        restartProgram()

@app.route('/', methods=['GET'])
def index():
    global ListExercices, VALUE, TYPE, NAME, INDEX
    isLast = 0
    if INDEX == len(ListExercices) - 1:
        isLast = 1
    data = {
            "name" : NAME, 
            "value" : VALUE,
            "type" : TYPE,
            "isLast" : isLast
    }
    return render_template(HTML + '.html',  data=data)

def get_file_content(uuid):
    with open('./static/'+ NAME + "/" +uuid+'.json', 'r') as file:
        return file.read()

# Exercices : LIST(name, value, type)  
def run(lastTrigger, ListExercicesExt, PORT, tray_):
    global INDEX, ListExercices, VALUE, TYPE, NAME, tray, lasttrigger
    lasttrigger = lastTrigger
    tray = tray_
    INDEX = 0
    ListExercices = ListExercicesExt[:]
    NAME = ListExercices[INDEX][0]
    VALUE = ListExercices[INDEX][1]
    TYPE = ListExercices[INDEX][2]
    
    webbrowser.open('http://localhost:' + str(PORT) + "/", new=1, autoraise=True)
    app.run(port=PORT)