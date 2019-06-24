#coding=utf-8
import nuke
import os
import sys
try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

"""
this module contains functionality of notifying the user when a render is finished.
This is done by playing a sound and showing a notification window.
"""

show_notification=True

play_sound=True

sound_file ="{}/01.wav".format(os.path.dirname(__file__))

def notify_user():

	if play_sound:
		QSound.play(sound_file)

	if show_notification:
		nuke.message("Finished rendering")
