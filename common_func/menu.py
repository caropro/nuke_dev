import nuke
from nukescripts import panels
import batch_render_front
import file_import
import auto_layout
import LayerShuffler

nuke.menu('Nuke').addCommand("common_func/batch_render_front",batch_render_front.main)
nuke.menu('Nuke').addCommand("common_func/file_read&write",file_import.run)
nuke.menu('Nuke').addCommand("common_func/auto_layout",auto_layout.main,"shift+l")

panels.registerWidgetAsPanel("LayerShuffler.LayerShuffler", "Layer Shuffler", "LayerShufflerPanelId")