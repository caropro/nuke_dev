#coding=utf-8
import pydevd

def run():
	pydevd.settrace('localhost', port=4488, stdoutToServer=True, stderrToServer=True)
