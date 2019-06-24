#coding=utf-8
import nuke
import nukescripts
"""

"""
def jump_to_the_edge_node(place):

	print(place)
	edge_node=get_edge_node(place)
	if edge_node is None:
		return
	nuke.zoom(1, (float(edge_node.xpos()), float(edge_node.ypos())))

def view_edge_node(which):
	"""
	connect the viewer to the first/last node
	:param which:
	:return:
	"""
	viewer_port = 8
	edge_node = get_edge_node(which)
	sel = nuke.selectedNodes()

	if edge_node is None:
		return

	nukescripts.clear_selection_recursive()
	edge_node.setSelected(True)
	nukescripts.connect_selected_to_viewer(viewer_port)
	edge_node.setSelected(False)

	for node in sel:
		node.setSelected(True)

	for node in nuke.allNodes("Viewer"):
		node.setSelected(False)
	print "view node:{}".format(get_edge_node(which).name())

def get_edge_node(which):
	"""
	get the node we need first and then do the jump or the connect viewer
	:param which:
	:return:
	"""
	edge_node=None
	for node in nuke.allNodes():
		if node.Class() != "Viewer":

			if edge_node is None:
				edge_node=node

			if which == "top":
				if node.ypos() < edge_node.ypos():
					edge_node = node

			if which == "bottom":
				if node.ypos() > edge_node.ypos():
					edge_node=node

	return edge_node
	print "get the {} node".format(which)
