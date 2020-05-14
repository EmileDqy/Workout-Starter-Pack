import configparser
import ast
from utils import getAbsPath
import datetime

def getBasicInfo():
    config = configparser.ConfigParser()
    config.read(getAbsPath('./config/config.ini'))
    MODE = int(config["WORKOUT"]["MODE"])
    EXERCISES_MODE = int(config["WORKOUT"]["randomize_sequence"])
    EXERCISES_SELECTED = ast.literal_eval(config["WORKOUT"]["EXERCIsES_SELECTED"])
    NUMBER_TO_PICK_PER_SESSION = int(config["WORKOUT"]["exercises_per_session"])
    INFO = [MODE, EXERCISES_MODE, EXERCISES_SELECTED, NUMBER_TO_PICK_PER_SESSION]

    if MODE == 0:
        # INFO = [MODE, EXERCISES_MODE, EXERCISES_SELECTED, NUMBER_TO_PICK_PER_SESSION, TIMER]
        INFO.append(int(config["MODE0 : Repeat"]["TIMER"]))
    
    elif MODE == 1:
        # INFO = [MODE, EXERCISES_MODE, EXERCISES_SELECTED, NUMBER_TO_PICK_PER_SESSION, HOURS, MAXIMUM_NUMBER_OF_SESSIONS_PER_INTERVAL, RECUPERATION_TIME_SECONDS]
        INFO.append(ast.literal_eval(config["MODE1 : Intervals"]["HOURS"]))
        INFO.append(int(config["MODE1 : Intervals"]["MAXIMUM_NUMBER_OF_SESSIONS_PER_INTERVAL"]))
        INFO.append(int(config["MODE1 : Intervals"]["recuperation_time_between_sessions_in_seconds"]))

    return INFO

def getServerConfig():
    config = configparser.ConfigParser()
    config.read(getAbsPath('./config/config.ini'))
    if "PORT" in config.options("EXERCICES"):
        return int(config["SERVER"]["PORT"])
    else:
        print("Switching to default ports : 5000")
        return 5000

def getExerciseByName(name):
    config = configparser.ConfigParser()
    config.read(getAbsPath('./config/config.ini'))
    if name in config.options("EXERCISES"):
        return ast.literal_eval(config["EXERCISES"][name])
    else:
        return False

def getLastTrigger():
    config = configparser.ConfigParser()
    config.read(getAbsPath('./config/config.ini'))
    try : 
        # [iteration, intervalTime]
        return ast.literal_eval(config["MODE1 : Intervals"]["LastTrigger"])
    except:
        return None

def resetConfig():
    pass

def updateLastTrigger(iteration, intervalIndex):
    config = configparser.ConfigParser()
    config.read(getAbsPath('./config/config.ini'))
    
    config["MODE1 : Intervals"]["LastTrigger"] = str([iteration, intervalIndex])

    with open(getAbsPath('./config/config.ini'), 'w') as f:
        config.write(f)

def getInputsConfig():
    config = configparser.ConfigParser()
    config.read(getAbsPath('./config/config.ini'))

    keyboard = config["INPUTS"].getboolean("block_keyboard")
    mouse = config["INPUTS"].getboolean("block_mouse")

    return (keyboard, mouse)

def updateExercise(name):
    config = configparser.ConfigParser()
    config.read(getAbsPath('./config/config.ini'))
    param = ast.literal_eval(config["EXERCISES"][name])
    newParam = str((param[0], str(param[1]), param[2] + 1))
    config["EXERCISES"][name] = newParam
    with open(getAbsPath('./config/config.ini'), 'w') as f:
        config.write(f)