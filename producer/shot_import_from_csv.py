#coding=utf-8
#author:Jonathon Woo
#version:1.0.0
from strack_globals import StrackGlobals
from std_strack.get_root_dir import get_root_dir

st = StrackGlobals.st
import csv
import nuke
import os

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *


class dir_locate(QDialog):
    def __init__(self, parent=None):
        super(dir_locate, self).__init__(parent)

    def return_dir(self):
        s = QFileDialog.getOpenFileName(self, u'获取csv文件', "/", "*.csv")
        return str(s[0])


def main():
    error_list = []
    csv_file = dir_locate().return_dir()
    print
    csv_file
    if not os.path.isfile(csv_file):
        return
    shot_list = []

    with open(csv_file, mode='r') as infile:
        reader = csv.reader(infile)
        for rows in reader:
            try:
                print(rows[0])
                shot_list.append(rows[0].strip())
            except:
                continue

    value = nuke.getInput("每行个数")
    try:
        int_value = int(value)
    except:
        if nuke.ask("未输入每行个数，默认100，是否继续?"):
            int_value = 100
        else:
            return
    count = 1
    x_dist = 0
    y_dist = 0
    for shot_name in shot_list:
        shot = st.shot.find("code = %s" % shot_name, StrackGlobals.st.shot.fields)
        if not shot:
            error_list.append(shot_name)
            continue
        project_id = shot.get("project_id")
        sequence_id = shot.get("sequence_id")

        project = StrackGlobals.st.project.find("id=%s" % project_id)
        project_name = project.get("code")

        epi_name = ""
        if sequence_id:
            sequence = StrackGlobals.st.sequence.find("id={}".format(sequence_id))
            sequence_name = sequence.get("code")
            epi_id = StrackGlobals.st.sequence.find("id={}".format(sequence_id), ["episode_id"]).get("episode_id")
            if epi_id:
                epi_name = StrackGlobals.st.episode.find("id=%s" % epi_id).get("code")
        else:
            sequence_name = ""
            epi_name = ""

        version_path = ''
        # get format path
        format_dir = "elements/processed/reformat"
        format_path = os.path.normpath(
            os.path.join(project_name, epi_name, "sequences", sequence_name, shot_name, format_dir))
        format_full_path = os.path.join(get_root_dir(StrackGlobals.st, StrackGlobals.current_project), format_path)
        if os.path.exists(format_full_path):
            try:
                versions = os.listdir(format_full_path)
                versions.sort(key=lambda x: int(x.split("v")[-1]))
                the_latest_version = versions[-1]
                version_path = os.path.join(format_full_path, the_latest_version)
            except:
                nuke.message("%s: reformat错误！！！！" % shot_name)
        # get retime path
        if not version_path:
            retime_dir = "elements/processed/retime"
            retime_path = os.path.normpath(
                os.path.join(project_name, epi_name, "sequences", sequence_name, shot_name, retime_dir))
            retime_full_path = os.path.join(get_root_dir(StrackGlobals.st, StrackGlobals.current_project), retime_path)
            if os.path.exists(retime_full_path):
                try:
                    versions = os.listdir(retime_full_path)
                    versions.sort(key=lambda x: int(x.split("v")[-1]))
                    the_latest_version = versions[-1]
                    version_path = os.path.join(retime_full_path, the_latest_version)
                except:
                    nuke.message("%s :retime错误！！！！" % shot_name)
        # get the iplate path
        if not version_path:
            iplate_dir = "elements/iplate"
            iplate_path = os.path.normpath(
                os.path.join(project_name, epi_name, "sequences", sequence_name, shot_name, iplate_dir))
            full_path = os.path.join(get_root_dir(StrackGlobals.st, StrackGlobals.current_project), iplate_path)
            versions = os.listdir(full_path)
            versions.sort(key=lambda x: int(x.split("v")[-1]))
            try:
                the_latest_version = versions[-1]
                version_path = os.path.join(full_path, the_latest_version)
            except:
                nuke.message("%s :no resource" % shot_name)
                continue
        print(version_path)
        read_source = nuke.getFileNameList(version_path)[0]
        readfile = nuke.createNode("Read")
        read_path = os.path.join(version_path, read_source)
        readfile['file'].fromUserText(read_path)

        readfile.setXpos(x_dist)
        readfile.setYpos(y_dist - 150)
        readfile["disable"].setValue(1)

        if count < int_value:
            x_dist += 200
        else:
            y_dist += 450
            x_dist = 0
            count = 0
        count += 1
    nuke.message("Done!!!")
    return nuke.message(str(error_list))

