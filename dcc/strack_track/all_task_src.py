from strack_globals import StrackGlobals
from std_strack.get_root_dir import get_root_dir
import nuke
import os
st = StrackGlobals.st


def get_src_path(shot_id,project_id):
    shot = StrackGlobals.st.shot.find("id=%s" % shot_id, StrackGlobals.st.shot.fields)
    sequence_id = shot.get("sequence_id")
    shot_name = shot.get("code")
    project = StrackGlobals.st.project.find("id=%s" % project_id)
    project_name = project.get("code")

    if sequence_id:
        sequence = StrackGlobals.st.sequence.find("id={}".format(sequence_id))
        sequence_name = sequence.get("code")
    else:
        sequence_name = ""

    version_path = ''
    # get format path
    format_dir = "elements/processed/format"
    format_path = os.path.normpath(os.path.join(project_name, "sequences", sequence_name, shot_name, format_dir))
    format_full_path = os.path.join(get_root_dir(StrackGlobals.st, StrackGlobals.current_project), format_path)
    if os.path.exists(format_full_path):
        versions = os.listdir(format_full_path)
        versions.sort(key=lambda x: int(x.split("v")[-1]))
        the_latest_version = versions[-1]
        version_path = os.path.join(format_full_path, the_latest_version)
        # nuke.message("from the reformat")
    # get retime path
    if not version_path:
        retime_dir = "elements/processed/retime"
        retime_path = os.path.normpath(os.path.join(project_name, "sequences", sequence_name, shot_name, retime_dir))
        retime_full_path = os.path.join(get_root_dir(StrackGlobals.st, StrackGlobals.current_project), retime_path)
        if os.path.exists(retime_full_path):
            versions = os.listdir(retime_full_path)
            versions.sort(key=lambda x: int(x.split("v")[-1]))
            the_latest_version = versions[-1]
            version_path = os.path.join(retime_full_path, the_latest_version)
            # nuke.message("from the retime")
    # get the iplate path
    if not version_path:
        iplate_dir = "elements/iplate"
        iplate_path = os.path.normpath(os.path.join(project_name, "sequences", sequence_name, shot_name, iplate_dir))
        full_path = os.path.join(get_root_dir(StrackGlobals.st, StrackGlobals.current_project), iplate_path)
        versions = os.listdir(full_path)
        versions.sort(key=lambda x: int(x.split("v")[-1]))
        try:
            the_latest_version = versions[-1]
            version_path = os.path.join(full_path, the_latest_version)
            # nuke.message("from the iplate")
        except:
            nuke.message("no resource")
    return version_path


def main():
    # get the current project id
    current_project = StrackGlobals.current_project
    current_project_id = current_project.get("id")
    current_project_name = current_project.get("code")
    x=0
    y=0
    count_row = 1
    # this is the tracking step id
    step_id = 43
    #filter
    filter_code = nuke.getInput('Change label',current_project_name)
    # select the tracking task which fit the step id and the project id
    track_tasklist = st.task.select("step_id=%s and project_id=%s" % (step_id, current_project_id), fields=[])

    for task in track_tasklist:
        shot_id = task.get("item_id")
        shot_code = st.shot.find("id=%s"% shot_id).get("code")
        if filter_code and not shot_code.startswith(filter_code):
            continue
        version_path = get_src_path(shot_id,current_project_id)
        read_source = nuke.getFileNameList(version_path)[0]
        readfile = nuke.createNode("Read")
        read_path = os.path.join(version_path, read_source)
        readfile['file'].fromUserText(read_path)
        readfile["ypos"].setValue(y)
        readfile["xpos"].setValue(x)
        x+=150
        if count_row%10 == 0:
            y+=150
            x = 0
        count_row += 1

    nuke.message("done")
