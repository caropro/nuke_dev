#coding=utf-8
import sys
import subprocess

def open_folder(path):
	if sys.platform=="darwin":
		subprocess.check_call(["open",path])
	if sys.platform=="linux2":
		subprocess.check_call(["gnome-open", path])
	if sys.platform=="windows":
		subprocess.check_call(['explorer',path])
