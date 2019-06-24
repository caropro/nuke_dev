#coding=utf-8
#author:Jonathon Woo
#version:1.0.0

import nuke
def knobChanged() :
    if nuke.thisKnob().name() == "selected" :
        current_node = nuke.thisNode()
        current_node["label"].setValue(current_node["label"].getValue())

def createStrackNode():
    current_node = nuke.allNodes("strack.gizmo")
    if current_node:
        nuke.delete(current_node[0])
        nuke.message("Keep single strack node in current scene")
    node = nuke.createNode('strack.gizmo')
    node["label"].setValue( "<font size=\"3\" color =#548DD4><b> Frame range :</b></font> <font color = red> [value this.input0.first] - [value this.input0.last] </font><script type='text/python'>count=[value this.input0.first] - [value this.input0.last]</script>\n输出路径：[knob this.Strack.file]\n输入错误判断：[value input.error]\n起始帧数：[knob this.first]\n终止帧数：[knob this.last]\n[knob this.tile_color this.Strack.tile_color]\n")