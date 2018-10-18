import nuke
import rename_node
import auto_comp_half
import continuous_work
import update_publish_import
nuke.pluginAddPath("gizmo")

version=nuke.NUKE_VERSION_STRING
if version.startswith("10"):
    gizmo="comp10.gizmo"
else:
    gizmo="comp11.gizmo"
nuke.menu('Nuke').addCommand("strack_comp/rename_node",rename_node.change_root)
nuke.menu('Nuke').addCommand("strack_comp/auto_comp_half",auto_comp_half.main)
nuke.menu('Nuke').addCommand("strack_comp/pack_node", "nuke.createNode(\"%s\")" % gizmo)
nuke.menu('Nuke').addCommand("strack_comp/continue",continuous_work.main)
nuke.menu('Nuke').addCommand("strack_comp/update_publish_import",update_publish_import.main)