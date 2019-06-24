#coding=utf-8
import nuke
import os
import sys


def mkds():
    current_node = nuke.thisNode()
    filepath = os.path.dirname(current_node["file"].getValue())
    if not os.path.exists(filepath):
        os.makedirs(filepath)
