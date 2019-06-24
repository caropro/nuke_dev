#coding=utf-8
#author:Jonathon Woo
#version:1.0.0
import nuke

def main():
    origin_nodes = nuke.selectedNodes()
    origin_nodes.sort(key=lambda x: x.xpos())
    for node in origin_nodes:
        nuke.autoplace(node)
    nodes = nuke.selectedNodes()
    nodes.sort(key=lambda x: x.xpos())

    current_xpos_list = [node.xpos() for node in nodes]

    count = 0
    for node_x in current_xpos_list:
        print node_x
        if count == 0:
            origin_nodes[count].setXpos(node_x)
        else:
            origin_nodes[count].setXpos(node_x + 150 * count)
        print count
        count += 1
