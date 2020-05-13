from win10toast import ToastNotifier
from utils import getAbsPath

def notify(title, message, duration = 10, threaded=True):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=duration, icon_path=getAbsPath("./config/icon.ico"), threaded=threaded)