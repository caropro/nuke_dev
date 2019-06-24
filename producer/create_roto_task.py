# coding=utf8
from strack_globals import StrackGlobals
import nuke

st = StrackGlobals.st

def main(*args):
    select = nuke.ask("是否使用所选创建任务?")
    if select:
        nodes = nuke.selectedNodes("Read")
    else:
        select_all = nuke.ask("使用所有节点创建任务?")
        if select_all:
            nodes = nuke.allNodes("Read")
        else:
            nuke.message("任务创建取消")
            return
    current_project_id = StrackGlobals.current_project.get("id")
    for read in nodes:
        user = read["name"].getValue().split("_")[0]
        user_id = st.user.find("name=%s" % user).get("id")
        shot_path = read["file"].getValue()
        shot_name = shot_path.split("/elements")[0].split("/")[-1]
        shot_id = st.shot.find("code=%s" % shot_name).get("id")
        project_id = st.shot.find("code=%s" % shot_name).get("project_id")
        if current_project_id==project_id:
            print "project id Confirm %s %s"%(current_project_id,project_id)
        roto_task = st.task.find("item_id=%s and project_id=%s and code=roto"%(shot_id,project_id))
        if roto_task:
            roto_task_id = roto_task.get("id")
            st.task.update(id=roto_task_id,fields={"assignee":user_id})
            continue
        data = {"approved_version": 001, "assignee": user_id, "cc_id": "", "code": "roto", "current_version": 001,
                "delivered_version": 001, "due_date": "", "item_id": shot_id, "json": "", "level": "", "lock": 0,
                "milestone": 0, "name": "roto", "priority": 30, "project_id": project_id, "status_id": 24, "step_id": 40,
                "sub_date": "", "tag_ids": ""}
        st.task.create(data)
    nuke.message("任务创建完成")