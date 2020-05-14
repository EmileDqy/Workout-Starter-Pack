import sys, os, subprocess, signal

def getAbsPath(file):
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(application_path, file)
    return path

def restartProgram():
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    subprocess.Popen(["start", application_path])

    os.kill(os.getpid(), signal.SIGINT)
