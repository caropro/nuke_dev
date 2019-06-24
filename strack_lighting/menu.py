#coding=utf-8
#coding=utf-8
import nuke
import lgt_auto_comp_half
import lgt_auto_comp
import lgt_layer_shuffle
nuke.menu('Nuke').addCommand("strack_lighting/layer_shuffle",lgt_layer_shuffle.main,"e")
nuke.menu('Nuke').addCommand("strack_lighting/auto_comp_half",lgt_auto_comp_half.main)
nuke.menu('Nuke').addCommand("strack_lighting/auto_comp",lgt_auto_comp.main)