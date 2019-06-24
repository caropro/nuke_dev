# coding=utf8
import nuke
import os
def main():
    nodes = nuke.selectedNode("Write")
    for n in nodes:
        first = n.firstFrame()
        last=n.lastFrame()
        filename=n['file'].value()
        dirpath = os.path.dirname(filename)
        if os.path.exists(dirpath)==False:
            os.makedirs(dirpath)
            nuke.render(n.name(),first,last,1)
        else:
            nuke.render(n.name(),first,last,1)