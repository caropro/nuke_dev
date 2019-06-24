#coding=utf-8
import nuke
import readwrite

nuke.menu('Nuke').addCommand("utilities/Read Write Node File",readwrite.run,"ctrl+alt+r")