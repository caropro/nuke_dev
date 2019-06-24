# coding=utf8
# Copyright (c) 2017 CineUse
import nuke
import os

def search_run(path,*args):
    print path
    first_layer = nuke.getFileNameList(path)
    node_list = []
    print "test info 1",first_layer
    for first_ff in first_layer:
        first_path = os.path.join(path, first_ff)
        if os.path.isdir(first_path):
            print("FOLDER!!!!!!!!!!!!!!!!!!!!!!")
            search_run(first_path)
        else:
            pathfile = first_path.replace("\\", "/")
            readnode = nuke.createNode("Read")
            readnode['file'].fromUserText(pathfile)
            node_list.append((readnode))
