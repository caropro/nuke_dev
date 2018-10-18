import nuke
import BTRD
import candw
import candwb
import file_import

#nuke.addBeforeFrameRender(creatDir.main)
#nuke.addOnCreat(creatDir.main)
#myToolbar=nuke.toolbar('my nodes')

#myToolbar.addcommand("sb",lambda: nuke.createNode("creatDir"))



#nuke.menu("Nodes").addCommand('BTRD',lambda: nuke.createNode("BTRD"))
nuke.menu('Nuke').addCommand("plugin/batch render",BTRD.main)
nuke.menu('Nuke').addCommand("plugin/import and write",candw.candw)
nuke.menu('Nuke').addCommand("plugin/single i&w",candwb.candw)
nuke.menu('Nuke').addCommand("plugin/file_import",file_import.run)