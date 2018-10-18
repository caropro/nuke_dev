#coding=utf-8
import nuke
import track_init
import track_dist_init
import all_task_src
import reimport

nuke.menu('Nuke').addCommand("strack_track/track init",track_init.main)
nuke.menu('Nuke').addCommand("strack_track/track dist init",track_dist_init.main)
nuke.menu('Nuke').addCommand("strack_track/all task source",all_task_src.main)
nuke.menu('Nuke').addCommand("strack_track/update source",reimport.main)