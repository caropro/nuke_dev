import nuke
import rename_readnode
import create_roto_task
import create_paint_task
import create_comp_task
import ooh_deal
import shot_import_from_csv

nuke.menu('Nuke').addCommand("producer/backdrop_rename_read_node",rename_readnode.main)
nuke.menu('Nuke').addCommand("producer/create_comp_task",create_comp_task.main)
nuke.menu('Nuke').addCommand("producer/create_roto_task",create_roto_task.main)
nuke.menu('Nuke').addCommand("producer/create_paint_task",create_paint_task.main)
nuke.menu('Nuke').addCommand("producer/ooh_deal",ooh_deal.main)
nuke.menu('Nuke').addCommand("producer/shot_import_from_csv",shot_import_from_csv.main)