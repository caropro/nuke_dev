import nuke
import os

def main():
    nodes = nuke.allNodes()
    for n in nodes:
        if n.Class()=="Write":
            first = n.firstFrame()
            last=n.lastFrame()   
            filename=n['file'].value()
            print filename
            import os
            dirpath = os.path.dirname(filename)
            print dirpath
            print os.path.exists(dirpath)
            if os.path.exists(dirpath)==False:
                nuke.message("path dosen't exist , will creat it")
                os.makedirs(dirpath)
                nuke.render(n.name(),first,last,1)
                print os.path.exists("%s"% dirpath)
            else:    
                nuke.render(n.name(),first,last,1)