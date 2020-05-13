from utils import getAbsPath, restartProgram
from infi.systray import SysTrayIcon
import sys, os, subprocess, signal
from notificationsManager import notify
import subprocess

class Tray:

    def __init__(self, MODE, VALUE, MODE_EXERCICES, EXERCICES):
        self.MODE = MODE
        if self.MODE == 0:
            self.menu_options = (
                ("Mode : Repeat", None, self._openConfig),
                ("Every : " + str(VALUE) + "s", None, self._openConfig),
                ("Sequence's type : " + ((MODE_EXERCICES == 1) and "Randomized" or "Ordered"), None, self._openConfig),
                ("Exercices loaded : " + str(EXERCICES), None, self._openConfig),
                ("Reload", None, self._reload))
        elif self.MODE == 1:
            self.menu_options = (
                ("Mode : Intervals", None, self._openConfig),
                ("Hours : " + str(VALUE[0]), None, self._openConfig),
                ("Number of sessions per interval: " + str(VALUE[1]), None, self._openConfig),
                ("Time between two sessions : " + str(VALUE[2]) + "s", None, self._openConfig),
                ("Sequence's type : " + ((MODE_EXERCICES == 1) and "Randomized" or "Ordered"), None, self._openConfig),
                ("Exercices loaded : " + str(EXERCICES), None, self._openConfig),
                ("Reload", None, self._reload))
        
        self.icon = getAbsPath("./config/icon.ico")
        self.name = "Workout Starter Pack"
        self.tray = SysTrayIcon(self.icon, self.name, self.menu_options , on_quit=self.quitTray)


    def init_icon_tray(self):
        self.tray.start()

    #Open the config file
    def _openConfig(self):
        config = getAbsPath('./config/config.ini')
        subprocess.Popen(["start", config])

    #Reload the whole program
    def _reload(self):
        self.tray.shutdown()
        restartProgram()

    #Quit the program and shutdown the tray
    def quitTray(self, t=0):
        notify("Workout Starter Pack", "Quitting.")
        os.kill(os.getpid(), signal.SIGINT)