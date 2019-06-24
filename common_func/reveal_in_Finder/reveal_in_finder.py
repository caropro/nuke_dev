#coding=utf-8
import nuke
import subprocess
import sys
import os

def add_reveal_button():
	"""
	add custom button,and tab
	为节点添加按钮和tab栏
	define a function to detect the change of this knob and run the function when the user push the button
	:return:
	"""
	print("Add button")

	node = nuke.thisNode()
	button_reveal=nuke.PyScript_Knob("revealInFinder","reveal in finder ",'')
	button_reveal_delete=nuke.PyScript_Knob("deletetheKnob","delete the tab",'')
	tab_custom = nuke.Tab_Knob("custom","custom")
	node.addKnob(tab_custom)
	node.addKnob(button_reveal)
	node.addKnob(button_reveal_delete)

def reveal_in_finder():
	"""
	点击删除按钮，删除面板按钮和这个tab
	click the delete button delete this tab
	点击reveal in finder在文件浏览器中查看路径对应文件
	click the reveal in finder open the file path in file explore
	:return:
	"""
	node = nuke.thisNode()
	knob = nuke.thisKnob()
	knobs=node.knobs()
	if knob.name()=="deletetheKnob":
		print("testfile")
		nuke.removeKnobChanged(knob, node=node)
		node.removeKnob(knob)
		node.removeKnob(knobs["revealInFinder"])
		node.removeKnob(knobs["custom"])
	if knob.name()=="revealInFinder":
		path = os.path.dirname(node["file"].getValue())
		if os.path.isdir(path):
			open_folder(path)
		else:
			nuke.message("can not open in finder")


def open_folder(path):
	if sys.platform=="darwin":
		subprocess.check_call(["open",path])
	if sys.platform=="linux2":
		subprocess.check_call(["gnome-open", path])
	if sys.platform=="windows":
		subprocess.check_call(['explorer',path])


node_classes = ["Read","Write","Camera","Camera2","ReadGeo","ReadGeo2","WriteGeo"]
def add():
	node = nuke.selectedNode()
	print(node)
	if node.Class() in node_classes:
		if not node.knobs().get("custom"):
			button_reveal=nuke.PyScript_Knob("revealInFinder","reveal in finder ",'')
			button_reveal_delete=nuke.PyScript_Knob("deletetheKnob","delete the tab",'')
			tab_custom = nuke.Tab_Knob("custom","custom")
			node.addKnob(tab_custom)
			node.addKnob(button_reveal)
			node.addKnob(button_reveal_delete)
			nuke.addKnobChanged(reveal_in_finder, node=node)
			print(tab_custom, node)
			node.removeKnob(tab_custom)
		else:
			nuke.message("the custom tab already exit,please delete that first")
	else:
		nuke.message("this node does not have the filepath")
#if someone delete the tab Not on purpose,use this function can add the tab to this node
