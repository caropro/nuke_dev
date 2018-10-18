# coding=utf8
# Copyright (c) 2017 CineUse
import nuke
import re
import os
from strack_globals import StrackGlobals
from std_strack.get_root_dir import get_root_dir

def main():
    #get the task
    item = StrackGlobals.selected_task.get('item')

    #gether the basic info about shot,seq,project
    task_id=StrackGlobals.selected_task.get("id")
    item_id = item.get('item_id')
    project_id=item.get("p_id")
    item_type = item.get('type')

    shot=StrackGlobals.st.shot.find("id=%s" % item_id,StrackGlobals.st.shot.fields)
    sequence_id = shot.get("sequence_id")
    shot_name=shot.get("code")
    project=StrackGlobals.st.project.find("id=%s"%project_id)
    project_name=project.get("code")
    task_name=StrackGlobals.st.task.find("id={}".format(task_id)).get("code")
    user_id=StrackGlobals.st.task.find("id={}".format(task_id)).get("assignee")
    user_name=str(StrackGlobals.st.user.find("id={}".format(user_id)).get("name"))

    if sequence_id:
        sequence=StrackGlobals.st.sequence.find("id={}".format(sequence_id))
        sequence_name=sequence.get("code")
    else:
        sequence_name=""
    
    root = get_root_dir(StrackGlobals.st, StrackGlobals.current_project)
    root_output = 'm:\\'
    #get the tracking info
    version_path=''
    #get format path
    format_dir = "elements/processed/format"
    format_path=os.path.normpath(os.path.join(project_name,"sequences",sequence_name,shot_name,format_dir))
    format_full_path = os.path.join(root, format_path)
    if os.path.exists(format_full_path):
        try:
            versions =os.listdir(format_full_path)
            versions.sort(key=lambda x:int(x.split("v")[-1]))
            the_latest_version=versions[-1]
            version_path=os.path.join(format_full_path,the_latest_version)
            nuke.message("from the reformat")
        except:
            nuke.message(u"reformat错误！！！！")
    #get retime path
    if not version_path:
        retime_dir = "elements/processed/retime"
        retime_path=os.path.normpath(os.path.join(project_name,"sequences",sequence_name,shot_name,retime_dir))
        retime_full_path = os.path.join(root, retime_path)
        if os.path.exists(retime_full_path):
            try:
                versions =os.listdir(retime_full_path)
                versions.sort(key=lambda x:int(x.split("v")[-1]))
                the_latest_version=versions[-1]
                version_path=os.path.join(retime_full_path,the_latest_version)
                nuke.message("from the retime")
            except:
                nuke.message(u"retime错误！！！！")
    #get the iplate path
    if not version_path:
        iplate_dir="elements/iplate"
        iplate_path=os.path.normpath(os.path.join(project_name,"sequences",sequence_name,shot_name,iplate_dir))
        full_path = os.path.join(root,iplate_path)
        versions =os.listdir(full_path)
        versions.sort(key=lambda x:int(x.split("v")[-1]))
        try:
            the_latest_version=versions[-1]
            version_path=os.path.join(full_path,the_latest_version)
            nuke.message("from the iplate")
        except:
            nuke.message("no resource")
            return

    read_source=nuke.getFileNameList(version_path)[0]
    print('read source path %s' % read_source)
    readfile = nuke.createNode("Read")
    read_path=os.path.join(version_path,read_source)
    readfile['file'].fromUserText(read_path)

    output_name=shot_name+"_tracking_"+user_name+"_v01"
    render_path=os.path.join(project_name,"sequences",sequence_name,shot_name,"work/tracking",task_name,"sourceimages",output_name,(output_name+".%04d.jpg"))
    writepath=os.path.join(root_output,render_path)
    writepath=writepath.replace("\\","/")
    writenode=nuke.createNode("Write")
    writenode["file_type"].setValue("jpeg")
    writenode["_jpeg_quality"].setValue(1)
    writenode["file"].setValue(writepath)
    render_dir=os.path.dirname(writepath)
    writenode["beforeRender"].setValue("import os\nif not os.path.exists(r'%s'):\n    os.mkdir(r'%s') "%(render_dir,render_dir))
    retime_value = readfile["last"].getValue()
    nuke.root()["fps"].setValue(25)
    nuke.root()["first_frame"].setValue(1001)
    nuke.root()["last_frame"].setValue(retime_value)

    return

