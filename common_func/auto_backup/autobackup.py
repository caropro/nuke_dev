# coding=utf-8
import nuke
import sys
import subprocess
import os
import time

# the path to store the backup files
backup_dir = "{}/nuke_backups".format(os.path.expanduser("~"))
# the number of backup files
number_of_backup = 5


def open_folder(path):
	if sys.platform == "darwin":
		subprocess.check_call(["open", path])
	if sys.platform == "linux2":
		subprocess.check_call(["gnome-open", path])
	if sys.platform == "windows" or sys.platform == "win32":
		subprocess.check_call(['explorer', path])


def get_script_name():
	script = nuke.root().name()
	script_name = os.path.basename(script)
	script_name = os.path.splitext(script_name)[0]

	return script_name


def open_backup_dir():
	script_name = get_script_name()
	script_backup_dir = "{}/{}".format(backup_dir, script_name)
	if os.path.exists(script_backup_dir):
		open_folder(script_backup_dir)
	else:
		nuke.message("Create a file to save before open the autosave folder")

def make_backup():
	script_name = get_script_name()
	script_backup_dir = "{}/{}".format(backup_dir, script_name)
	current_time = time.strftime("%y%m%d-%H%M")
	if not os.path.isdir(script_backup_dir):
		os.makedirs(script_backup_dir)

	try:
		nuke.removeOnScriptSave(make_backup)
		nuke.scriptSave("{}/back_up_{}_{}.nk".format(script_backup_dir, current_time, script_name))
		nuke.addOnScriptSave(make_backup)
	except:
		nuke.message("Could not write a backup file")

	delete_older_backup_version(script_backup_dir)

def delete_older_backup_version(path):
	"""

	:param path:
	:return:
	"""
	files_list = []
	keep_list = []

	for filename in os.listdir(path):
		if os.path.splitext(filename)[1] == '.nk':
			files_list.append(filename)

	if len(files_list) > number_of_backup:
		keep_list = files_list[-number_of_backup:]
	else:
		return

	for filename in files_list:
		if filename not in keep_list:
			file_to_delete = "{}/{}".format(path,filename)
			if os.path.isfile(file_to_delete):
				os.remove(file_to_delete)