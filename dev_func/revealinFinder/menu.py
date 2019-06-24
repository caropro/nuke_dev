#coding=utf-8
import nuke
import revealinfinder


node_classes = ["Read","Write","Camera","Camera2","ReadGeo","ReadGeo2","WriteGeo"]
# nuke.menu('Nuke').addCommand("utilities/add_openpath_to_node",revealinfinder.add,"alt+o")
nuke.menu('Nuke').addCommand("utilities/添加查找路径",revealinfinder.add,"alt+o")

for node in node_classes:
	nuke.addOnUserCreate(revealinfinder.add_reveal_button,nodeClass=node)
	nuke.addKnobChanged(revealinfinder.reveal_in_finder,nodeClass=node)

#定义这个node的knob产生变化后运行的判断