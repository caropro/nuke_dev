import nuke
import rename_readnode
import create_task


nuke.menu('Nuke').addCommand("producer/rename_read_node",rename_readnode.main)
nuke.menu('Nuke').addCommand("producer/create_task",create_task.main)
