#coding=utf-8
import nuke
import sys
sys.path.append(r"C:\Users\admin\Desktop\strack_desktop_Ver1.6.0-beta_win-vs08-py27\Lib\strack_desktop\custom\dccApp\nuke\dev_func\debug\pycharm-debug.egg")
import debug

nuke.menu('Nuke').addCommand("dev/Debug",debug.run)