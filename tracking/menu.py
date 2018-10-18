#coding=utf-8
import nuke
import track_init
import track_dist_init
import csv_import_file

nuke.menu('Nuke').addCommand("track/track init",track_init.main)
nuke.menu('Nuke').addCommand("track/track dist init",track_dist_init.main)
nuke.menu('Nuke').addCommand("track/csv file import",csv_import_file.main)