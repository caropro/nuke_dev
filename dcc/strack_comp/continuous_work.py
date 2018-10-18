from strack_globals import StrackGlobals
import sys
import os
import nuke
def main():
    st = StrackGlobals.st

    # find current task info
    project_id = StrackGlobals.current_project.get("id")
    step_name = StrackGlobals.selected_task.get("step").get("code")
    task_id = StrackGlobals.selected_task.get("id")
    task_code = StrackGlobals.selected_task.get("code")
    type_t = StrackGlobals.selected_task.get("item").get("type")
    shot_id = StrackGlobals.selected_task.get("item").get("item_id")
    root = st.disk.find("project_id={}".format(project_id), ["setting"])
    project_name = st.project.find("id={}".format(project_id), ['code']).get("code")
    user_id = StrackGlobals.st.task.find("id={}".format(task_id)).get("assignee")
    user_name = str(StrackGlobals.st.user.find("id={}".format(user_id)).get("name"))
    shot = getattr(st, type_t).find("id=%s" % shot_id, ["json"])
    print(shot)
    if sys.platform == "win32":
        root_dir = root.get("setting").get("win_path")
    else:
        root_dir = root.get("setting").get("mac_path") \
            if sys.platform == "darwin" \
            else root.get("setting").get("linux_path")

    item = st.shot.find("id=%s" % shot_id)
    shot_name = item.get("code", None)
    seq_id = item.get("sequence_id", None)
    seq_name = st.sequence.find("id=%s" % seq_id).get("code")
    nuke_path = os.path.join(root_dir, project_name, "sequences", seq_name, shot_name, "work", step_name, task_code, "nuke")
    # get nuke file in the dir
    nukefile_list = [nuke_file for nuke_file in os.listdir(nuke_path) if nuke_file.endswith(".nk")]
    nukefile_list.sort(key=lambda x: x.split("_v")[-1])
    # get the lastest version
    # max_version = max(nukefile_list)
    max_version = nukefile_list[-1]
    # get new file name ,file path,renderpath
    new_v = max_version.split("_v")[-1].split("_e")[0]
    new_e = "%03d" % (int(max_version.split("_e")[-1].replace(".nk", "")) + 1)
    new_filename = "{0}_{1}_{2}_v{3}_e{4}.nk".format(shot_name, step_name, user_name, new_v, new_e)
    new_filepath = os.path.join(nuke_path, new_filename)
    rendername = "{0}_{1}_{2}_v{3}_e{4}".format(shot_name, step_name, user_name, new_v, new_e)
    render_dir = os.path.join(root_dir, project_name, "sequences", seq_name, shot_name, "work", step_name, "renders")
    outname = rendername + ".%04d.dpx"
    outpath = os.path.join(render_dir, rendername, outname).replace("\\", '/')
    # get file path and import
    max_file_path = os.path.join(nuke_path, max_version)
    nuke.scriptOpen(max_file_path)

    # change the render path and render setting
    writenode = nuke.allNodes("Write")
    if writenode:
        if len(writenode) > 1:
            nuke.message("more then one write node exist")
        writenode =[write for write in writenode if write["name"].getValue()=="Strack"][0]
        if not writenode:
            writenode = writenode[0]
    else:
        writenode = nuke.createNode("Write")
    writenode["file"].setValue(outpath)
    writenode["file_type"].setValue("dpx")
    writenode["name"].setValue("Strack")
    writenode["tile_color"].setValue(255)
    # save file
    nuke.scriptSave(new_filepath)
    nuke.scriptClose()
    nuke.scriptOpen(new_filepath)
    nuke.message("last file is %s"%max_version)