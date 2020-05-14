import time
import ast
import math
import sys
from random import shuffle
import datetime
from threading import Thread
import PyHook3 as pyHook
import pythoncom
import http.client as httplib

from utils import getAbsPath
from notificationsManager import notify
from server import run
from tray import Tray
import config

def has_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False


def init_keyboard(keyboard = True, mouse = True):
    hm = pyHook.HookManager()
    if keyboard:
        hm.KeyDown = OnEvent
        hm.KeyUp = OnEvent
        hm.HookKeyboard()
    if mouse:
        hm.MouseAll = OnEvent
        hm.HookMouse()
    pythoncom.PumpMessages() 

def OnEvent(event):
    return False

#Load EXERCISES configurations
def getListOfEXERCISES(EXERCISES):
    # Init the basic mathematical functions :
    ln = math.log
    log = math.log
    e = math.exp
    sin = math.sin
    cos = math.cos

    # Let's create a list of every exercise's configuration :
    ListEXERCISESHTML = []
    for name in EXERCISES:
        exercise_config = config.getExerciseByName(name)
        if exercise_config != False:
            TYPE, FORMULA, x = exercise_config
            FORMULA.replace("^","**")
            FORMULA.replace("x", "*")
            value = eval(FORMULA)
            ListEXERCISESHTML.append((name, value, TYPE)) #, int(startPos)
            continue
        notify("Workout Starter Pack", "Error: " + name + " not found.", 5)
    
    return ListEXERCISESHTML

def start():
    #First, we get the basic information:
    info = config.getBasicInfo()
    MODE = info[0]
    lastTrigger = config.getLastTrigger()

    # Goal : Get basic config, load config, load tray and determine the TIMER
    if MODE == 0:
        EXERCISES_MODE, EXERCISES_SELECTED, NUMBER_TO_PICK_PER_SESSION, TIMER = info[1:]
        # Get List EXERCISES Config:
        ListEXERCISES = getListOfEXERCISES(EXERCISES_SELECTED)
        # Start STRAY as THREAD
        tray = Tray(MODE, TIMER, EXERCISES_MODE, EXERCISES_SELECTED[:NUMBER_TO_PICK_PER_SESSION])

    elif MODE == 1:
        EXERCISES_MODE, EXERCISES_SELECTED, NUMBER_TO_PICK_PER_SESSION, HOURS, MAXIMUM_NUMBER_OF_SESSIONS_PER_INTERVAL, RECUPERATION_TIME_SECONDS =  info[1:]
        # Get List EXERCISES Config:
        ListEXERCISES = getListOfEXERCISES(EXERCISES_SELECTED)
        # Start STRAY as THREAD
        tray = Tray(MODE, [HOURS, MAXIMUM_NUMBER_OF_SESSIONS_PER_INTERVAL, RECUPERATION_TIME_SECONDS], EXERCISES_MODE, EXERCISES_SELECTED[:NUMBER_TO_PICK_PER_SESSION])
        
        # Get current time and hour : determine TIMER
        
        HOURS.sort()
        expandedIntervals = [[j for j in range(*HOURS[i:i+2])] for i in range(0, len(HOURS), 2)]
        currentDT = datetime.datetime.now()
        n = 0
        if lastTrigger == None:
            lastTrigger = [0, -1]
            notify("Workout Starter Pack", "Error: Couldn't get the last trigger from config. Switching to [0, -1] by default.", 5)
        
        for i in range(len(expandedIntervals)):
            expandedInterval = expandedIntervals[i]
            if currentDT.hour in expandedInterval :
                
                if lastTrigger[0] < MAXIMUM_NUMBER_OF_SESSIONS_PER_INTERVAL and lastTrigger[1] == i :
                    TIMER = RECUPERATION_TIME_SECONDS
                    lastTrigger = [lastTrigger[0] + 1, i]
                
                elif lastTrigger[1] != i:
                    lastTrigger = [1, i]
                    TIMER = 5
                
                else:
                    nextHour = HOURS[0]
                    nextDay = datetime.datetime(currentDT.year, currentDT.month, currentDT.day + 1).day
                    
                    for i in HOURS[::2]: 
                        if i > currentDT.hour:
                            nextHour = i
                            nextDay = currentDT.day

                    nextDateTime = datetime.datetime(currentDT.year, currentDT.month, nextDay, nextHour, 0)
                    TIMER = (nextDateTime - currentDT).total_seconds()
                    print("Skipping to next interval because finished this one")
                    # config.updateLastTrigger(0, -1)
            else:
                n += 1

        # Update current interval and interation in config if currentDT not in any interval
        if n == len(expandedIntervals):
            print("Not in any intverval")
            lastTrigger = [0, -1]
            nextHour = HOURS[0]
            nextDay = datetime.datetime(currentDT.year, currentDT.month, currentDT.day + 1).day

            for i in HOURS[::2]: 
                if i >= currentDT.hour:
                    nextHour = i
                    nextDay = currentDT.day

            nextDateTime = datetime.datetime(currentDT.year, currentDT.month, nextDay, nextHour, 0)
            TIMER = (nextDateTime - currentDT).total_seconds()

    # Notify for the user of what was done
    if len(ListEXERCISES) == 0:
        notify("Workout Starter Pack", "Error: no exercises loaded. Please look at the configuration file. Quitting.", 5)
        sys.exit(0)

    # EXERCISES_MODE : 
    if EXERCISES_MODE == 1:
        shuffle(ListEXERCISES)
        ListEXERCISES[NUMBER_TO_PICK_PER_SESSION:]
    elif EXERCISES_MODE == 0:
        ListEXERCISES[NUMBER_TO_PICK_PER_SESSION:]
    
    # Notify of the next session's content
    names = [i[0] for i in ListEXERCISES]
    notify("Workout Starter Pack", str(len(ListEXERCISES)) + " exercise(s) loaded!\nWaiting " + str(int(TIMER)) + " seconds. \nNext Session : " + " ".join(names) , 5)
    
    # Starting the tray
    tray.init_icon_tray()

    # Sleep TIMER seconds
    time.sleep(TIMER)

    # Redirect the keys and mouse events
    print("Redirecting keys events...")
    inputs = config.getInputsConfig()
    keyboard = Thread(target= lambda : init_keyboard(*inputs))
    keyboard.start()

    # Run the server
    PORT = config.getServerConfig()
    if(has_internet()):
        notify("Workout Starter Pack", ((EXERCISES_MODE == 0) and "Ordered" or "Randomized") + " sequence :\n  - " + "\n  - ".join(names) , 5)
        run(lastTrigger, ListEXERCISES, PORT, tray)
    else:
        notify("Workout Starter Pack", "No internet connection (needed for the webserver)! Stopping...", 5, threaded=False)

if __name__ == "__main__":
    if(has_internet()):
        start()
    else:
        notify("Workout Starter Pack", "No internet connection (needed for the webserver)! Stopping...", 5, threaded=False)