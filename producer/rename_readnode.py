#coding=utf-8
import nuke

def main(*args):
    BackdropNode = nuke.selectedNodes("BackdropNode")[0]
    BackdropNode_name = BackdropNode["name"].getValue()
    user_name = BackdropNode["label"].getValue()
    count = 0
    for node in nuke.selectedNodes("Read"):
        if count == 0:
            node["name"].setValue("%s_%s"%(user_name,BackdropNode_name))
        else:
            node["name"].setValue("%s_%s_%s" % (user_name,BackdropNode_name, count))
        count += 1