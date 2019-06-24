# coding=utf8
import nuke

def read_node_count():
    nodes = nuke.selectedNodes("Read")
    nuke.message(u"read节点数量为:%s个"%len(nodes))
    print(len(nodes))
    return

def change_node_color():
    nodes = nuke.selectedNodes()
    nuke.message(u"请选择节点颜色")
    color_value =nuke.getColor()
    if not color_value:
        return
    for node in nodes:
        node["tile_color"].setValue(int(color_value))
    return




