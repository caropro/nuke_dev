#coding=utf-8
import nuke
import read_writenode

nuke.menu('Nuke').addCommand("common_func/utilities/Read Write Node File",read_writenode.run,"ctrl+alt+r")