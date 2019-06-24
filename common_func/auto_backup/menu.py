#coding=utf-8
import nuke
import autobackup

nuke.menu("Nuke").addCommand("common_func/autoBackup/select back up path",autobackup.open_backup_dir)
nuke.addOnScriptSave(autobackup.make_backup)




