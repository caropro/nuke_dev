import nuke
import rename_node
import auto_comp_half
import continuous_work
import update_publish_import
import check_ascii
import read_node
import strack_render
import os

nuke.pluginAddPath("gizmo")
nuke.pluginAddPath("icon")

version = nuke.NUKE_VERSION_STRING
if version.startswith("10"):
    gizmo = "comp10.gizmo"
else:
    gizmo = "comp11.gizmo"
nuke.menu('Nuke').addCommand("strack_comp/rename_node", rename_node.change_root)
nuke.menu('Nuke').addCommand("strack_comp/auto_comp_half", auto_comp_half.main)
nuke.menu('Nuke').addCommand("strack_comp/pack_node", "nuke.createNode(\"%s\")" % gizmo)
nuke.menu('Nuke').addCommand("strack_comp/continue", continuous_work.main)
nuke.menu('Nuke').addCommand("strack_comp/update_publish_import", update_publish_import.main)
nuke.menu('Nuke').addCommand("strack_comp/check ascii", check_ascii.check_node_ascii)
nuke.menu('Nuke').addCommand("strack_comp/read_node_count", read_node.read_node_count)
nuke.menu('Nuke').addCommand("strack_comp/change_node_color", read_node.change_node_color)

logo = os.path.normpath(os.path.join(os.path.dirname(__file__), "icon", "Ph03nyx-Super-Mario-Retro-Mario-2.ico"))
logo2 = os.path.normpath(os.path.join(os.path.dirname(__file__), "icon", "pointcloud.png"))
te_menu = nuke.menu("Nodes").addMenu("Comp", icon=logo2)
te_menu.addCommand("IBK_lin_v3_3", "nuke.createNode('IBK_lin_v3_3.gizmo')", icon="fun.ico")
te_menu.addCommand("Strack_render", strack_render.createStrackNode, icon="pointcloud.png")
nuke.addKnobChanged(strack_render.knobChanged)