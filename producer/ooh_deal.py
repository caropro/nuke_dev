# coding=utf8
from strack_globals import StrackGlobals
from std_strack.get_root_dir import get_root_dir
st = StrackGlobals.st
import nuke
import os

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
import platform

#使用qt控件来获取文件夹路径
class dir_locate(QDialog):
    def __init__(self,path,parent=None):
        super(dir_locate, self).__init__(parent)
        self.path = path
    def return_dir(self):
        s = QFileDialog.getExistingDirectory(self, '获取文件夹位置', self.path)
        return str(s)

def main():
    user = StrackGlobals.me
    user_name = user.get("name")

    path_judge = nuke.ask("是否为检修?")
    key_word = nuke.getInput("分割值")
    if not key_word:
        key_word="_paint_"
    if path_judge:
        print"hahaha"
        shot_list = []
        new_nodes = []
        shot_dict = {}
        for writenode in nuke.allNodes("Write"):
              if key_word in writenode["file"].getValue():
                    shot_name = os.path.basename(writenode["file"].getValue()).split(key_word)[0]
                    shot_list.append(shot_name)
                    shot_dict[shot_name] = writenode
        print shot_list
        if not shot_list:
            nuke.message("没有产生镜头列表，操作结束。")
            return
        viewpath = os.path.join(get_root_dir(StrackGlobals.st, StrackGlobals.current_project),StrackGlobals.current_project.get("code"), "global/ooh")
        print(viewpath)
        dir_widget = dir_locate(viewpath)
        src_path = dir_widget.return_dir()
        if src_path and os.path.isdir(src_path):
            file_candidates = nuke.getFileNameList(src_path)
            for file_ooh in file_candidates:
                file_ooh_fullpath = os.path.join(src_path, file_ooh)
                ooh_shot_name = file_ooh.split(key_word)[0]
                if os.path.isdir(file_ooh_fullpath):
                    continue
                else:
                    ooh_readnode = nuke.createNode("Read")
                    ooh_readnode['file'].fromUserText(file_ooh_fullpath)
                    ooh_readnode["disable"].setValue(1)
                    tar_node = shot_dict.get(ooh_shot_name)
                    if not tar_node:
                        new_nodes.append(ooh_readnode)
                        continue
                    ooh_readnode.setXpos(tar_node.xpos())
                    ooh_readnode.setYpos(tar_node.ypos() + 300)
                    print(new_nodes)
        value = nuke.getInput("每行个数")
        func_deal(new_nodes,user_name,int(value),count = 1,x_dist = -800,y_dist = 0,check=True,key_word=key_word)
        return
    else:
        pass

    #先进行自选导入。如果跳过，则直接处理场景内的文件。
    file_path = True
    while file_path:
        viewpath = os.path.join(get_root_dir(StrackGlobals.st, StrackGlobals.current_project),StrackGlobals.current_project.get("code"), "global/ooh")
        print(viewpath)
        dir_widget = dir_locate(viewpath)
        src_path = dir_widget.return_dir()
        if src_path and os.path.isdir(src_path):
            file_candidates = nuke.getFileNameList(src_path)
            for file_ooh in file_candidates:
                file_ooh_fullpath = os.path.join(src_path, file_ooh)
                if os.path.isdir(file_ooh_fullpath):
                    continue
                else:
                    ooh_readnode = nuke.createNode("Read")
                    ooh_readnode['file'].fromUserText(file_ooh_fullpath)
                    ooh_readnode["disable"].setValue(1)
            file_path = False
        else:
            path_judge = nuke.ask("没有查找路径，将处理工程中文件，是否继续?")
            if path_judge:
                file_path = False
            else:
                return
    all_read_nodes = nuke.allNodes("Read")
    all_read_nodes.sort(key=lambda x: x["file"].getValue())

    value = nuke.getInput("每行个数")
    try:
        int_value = int(value)
    except:
        answer =nuke.ask("未输入每行个数，默认100，是否继续?")
        if answer:
            int_value = 100
        else:
            return
    func_deal(all_read_nodes,user_name,int_value,count = 1,x_dist = 0,y_dist = 0,key_word=key_word)


def func_deal(all_read_nodes,user_name,int_value=100,count = 1,x_dist = 0,y_dist = 0,check=False,key_word="_paint_"):
    for readnode in all_read_nodes:
        input_file_path = readnode["file"].getValue()
        input_file_name = os.path.basename(input_file_path)
        file_name = os.path.splitext(input_file_name)[0]
        if key_word not in file_name:
            continue
        #所有项目都可以用的前提是，外包方100%遵守规范
        shot_name = file_name.split(key_word)[0]
        shot = st.shot.find("code = %s" % shot_name, StrackGlobals.st.shot.fields)
        if not shot:
            nuke.message("镜头不存在:%s" % shot_name)
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

        input_file_dir = os.path.dirname(input_file_path)
        print(input_file_path)
        if platform.system()=="Linux":
            date_name = input_file_dir.split("/")[7]
        else:
            date_name = input_file_dir.split("/")[6]
        output_dir = input_file_path.split(date_name)[0]
        output_path = os.path.normpath(
            os.path.join(output_dir, "reference", date_name,user_name, "{}.%04d.jpeg".format(file_name))).replace("\\", "/")
        print(output_path)
        readnode.setXpos(x_dist)
        readnode.setYpos(y_dist)

        write_node = nuke.createNode("Write")
        write_node['file'].setValue(output_path)
        write_node["file_type"].setValue("jpeg")
        write_node.setInput(0, readnode)
        write_node.setXpos(x_dist)
        write_node.setYpos(y_dist + 200)


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
        read_source = nuke.getFileNameList(version_path)[0]
        readfile = nuke.createNode("Read")
        read_path = os.path.join(version_path, read_source)
        readfile['file'].fromUserText(read_path)
        readfile["frame_mode"].setValue(1)
        readfile["frame"].setValue("1")

        readfile.setXpos(x_dist)
        readfile.setYpos(y_dist - 150)
        readfile["disable"].setValue(1)

        if count < int_value:
            if check:
                x_dist -=150
            else:
                x_dist += 150
        else:
            y_dist += 1000
            x_dist = 0
            count = 0
        count += 1
    return nuke.message("Done!!!")
