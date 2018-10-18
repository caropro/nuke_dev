#coding=utf-8
#coding=utf-8
import nuke
import lgt_auto_comp_half
import lgt_auto_comp

nuke.menu('Nuke').addCommand("lighting/auto_comp_half",lgt_auto_comp_half.main)
nuke.menu('Nuke').addCommand("lighting/auto_comp",lgt_auto_comp.main)