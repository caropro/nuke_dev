#coding=utf-8
from strack_globals import StrackGlobals
import nuke

st = StrackGlobals.st

def main(*args):
    current_project_id = StrackGlobals.current_project.get("id")
    for read in nuke.allNodes("Read"):
        user = read["name"].getValue().split("_")[0]
        user_id = st.user.find("name=%s" % user).get("id")
        shot_path = read["file"].getValue()
        shot_name = shot_path.split("/elements")[0].split("/")[-1]
        shot_id = st.shot.find("code=%s" % shot_name).get("id")
        project_id = st.shot.find("code=%s" % shot_name).get("project_id")
        if current_project_id==project_id:
            print "project id Confirm %s %s"%(current_project_id,project_id)
        comp_task = st.task.find("item_id=%s and project_id=%s and code=comp"%(shot_id,project_id))
        if comp_task:
            comp_task_id = comp_task.get("id")
            st.task.update(id=comp_task_id,fields={"assignee":user_id})
            continue
        data = {"approved_version": 001, "assignee": user_id, "cc_id": "", "code": "comp", "current_version": 001,
                "delivered_version": 001, "due_date": "", "item_id": shot_id, "json": "", "level": "", "lock": 0,
                "milestone": 0, "name": "comp", "priority": 30, "project_id": project_id, "status_id": 24, "step_id": 56,
                "sub_date": "", "tag_ids": ""}
        st.task.create(data)