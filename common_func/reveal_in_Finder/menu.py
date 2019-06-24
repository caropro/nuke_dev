#coding=utf-8
import nuke
import reveal_in_finder

node_classes = ["Read","Write","Camera","Camera2","ReadGeo","ReadGeo2","WriteGeo"]
nuke.menu('Nuke').addCommand("common_func/utilities/添加查找路径",reveal_in_finder.add,"alt+o")

for node in node_classes:
	nuke.addOnUserCreate(reveal_in_finder.add_reveal_button,nodeClass=node)
	nuke.addKnobChanged(reveal_in_finder.reveal_in_finder,nodeClass=node)

#定义这个node的knob产生变化后运行的判断