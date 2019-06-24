#coding=utf-8
import nuke
import edgeNode

nuke.menu("Nuke").addCommand("common_func/utilities/edgeNode/jump to the top node","edgeNode.jump_to_the_edge_node('top')","Ctrl+Shift+.")
nuke.menu("Nuke").addCommand("common_func/utilities/edgeNode/jump to the bottom node","edgeNode.jump_to_the_edge_node('bottom')","Ctrl+Shift+,")
nuke.menu("Nuke").addCommand("common_func/utilities/edgeNode/view top node","edgeNode.view_edge_node('top')","Ctrl+.")
nuke.menu("Nuke").addCommand("common_func/utilities/edgeNode/view bottom node","edgeNode.view_edge_node('bottom')","Ctrl+,")




