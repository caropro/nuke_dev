#coding=utf-8
import os
import nuke
def main():
    target_node = nuke.selectedNode()
    if target_node.Class() != "Read": pass
    # get target node's position value
    pos_x, pos_y = target_node.xpos(), target_node.ypos()
    # get target node's channels and layers
    channels = target_node.channels()
    nukeLayers = nuke.layers()
    nukeLayers.remove("rgb")
    nukeLayers.remove("rgba")
    nukeLayers.remove("alpha")

    layerNames = []
    for i in channels:
        t = i.split(".")
        t.pop(1)
        layerNames.extend(t)

    passes = []
    for layer in nukeLayers:
        if layer in layerNames:
            passes.append(layer)

    main_dot = nuke.Node("Dot")

    main_dot_y = main_dot.ypos()
    if main_dot_y != pos_y + 150:
        main_dot.setYpos(int(pos_y + 150))

    main_dot.setInput(0, target_node)
    main_dot_y = main_dot["ypos"].getValue()
    main_dot_x = main_dot["xpos"].getValue()
    multi = 0
    for layer in passes:
        pos_offset = 150 * multi

        dot_node = nuke.Node("Dot")
        dot_node['name'].setValue("%s_dot" % layer)
        dot_node.setInput(0, main_dot)
        dot_node.setXYpos(int(main_dot_x + pos_offset), int(main_dot_y))
        dot_node_y = dot_node.ypos()
        multi = multi + 1

        shuffle_node = nuke.Node("Shuffle")
        shuffle_node['name'].setValue(layer)
        shuffle_node.setInput(0, dot_node)
        shuffle_node["in"].setValue(layer)
        shuffle_node.setYpos(dot_node_y + 150)
    nuke.message("Done!")
    return











