import sys, os, subprocess, signal

def getAbsPath(file):
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    path = os.path.join(application_path, file)
    return path


def restartProgram():
    if hasattr(sys, "frozen"):
        execute = [sys.executable]
    else:
        execute = ["python", __file__]
    subprocess.Popen(execute)
    os.kill(os.getpid(), signal.SIGINT)