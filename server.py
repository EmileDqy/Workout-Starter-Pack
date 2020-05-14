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

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300

lasttrigger = [0, -1]

tray = None

PORT = 5000
HTML = "workoutGUI"

Listexercises = []
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
    global Listexercises, INDEX, VALUE, TYPE, NAME, tray, lasttrigger
    
    #Update the exercise's information (iterations)
    config.updateExercise(Listexercises[INDEX][0])

    if INDEX < len(Listexercises) - 1:
        INDEX += 1
        VALUE = Listexercises[INDEX][1]
        TYPE = Listexercises[INDEX][2]
        NAME = Listexercises[INDEX][0]
        isLast = 0
        if INDEX == len(Listexercises) - 1:
            isLast = 1
        data = {
            "name" : NAME,
            "value" : VALUE,
            "type" : TYPE,
            'isLast' : isLast
        }
        notify("Workout Starter Pack", "Next exercise : " + NAME + " " + ((TYPE == 0) and "x"+ str(VALUE) or str(VALUE)+"s"), 5)
        return render_template(HTML + '.html',  data=data)
    else:
        config.updateLastTrigger(*lasttrigger)
        notify("Workout Starter Pack", "Session finished!", 5, threaded=False)
        restartProgram()

@app.route('/', methods=['GET'])
def index():
    global Listexercises, VALUE, TYPE, NAME, INDEX
    isLast = 0
    if INDEX == len(Listexercises) - 1:
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

# exercises : LIST(name, value, type)  
def run(lastTrigger, ListexercisesExt, PORT, tray_):
    global INDEX, Listexercises, VALUE, TYPE, NAME, tray, lasttrigger
    lasttrigger = lastTrigger
    tray = tray_
    INDEX = 0
    Listexercises = ListexercisesExt[:]
    NAME = Listexercises[INDEX][0]
    VALUE = Listexercises[INDEX][1]
    TYPE = Listexercises[INDEX][2]
    
    webbrowser.open('http://localhost:' + str(PORT) + "/", new=1, autoraise=True)
    app.run(port=PORT)