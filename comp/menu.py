import nuke
import rename_node
import auto_comp_half
nuke.pluginAddPath("gizmo")

version=nuke.NUKE_VERSION_STRING
if version.startswith("10"):
    gizmo="comp10.gizmo"
else:
    gizmo="comp11.gizmo"
nuke.menu('Nuke').addCommand("comp/rename_node",rename_node.change_root)
nuke.menu('Nuke').addCommand("comp/auto_comp_half",auto_comp_half.main)
nuke.menu('Nuke').addCommand("comp/pack_node", "nuke.createNode(\"%s\")" % gizmo)
tool_bar = nuke.menu('Nodes')
menu = tool_bar.addMenu("test")
menu.addCommand("comp", "nuke.createNode(\"%s\")" % gizmo)