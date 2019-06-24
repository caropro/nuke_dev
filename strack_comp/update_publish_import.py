#coding=utf-8
import NukefileImport
import NukeReadImport
from strack_globals import StrackGlobals
from std_strack.get_root_dir import get_root_dir
from std_strack.get_full_path import get_full_path
import os
import nuke
def main(*args):
    tracking = mp = roto = paint = render = vfx = None
    # get the task
    item = StrackGlobals.selected_task.get('item')

    # gether the basic info about shot,seq,project
    task_id = StrackGlobals.selected_task.get("id")
    item_id = item.get('item_id')

    # 获取跟踪环节的信息。
    tracking_step = StrackGlobals.st.step.find("code=tracking")
    tracking_id = tracking_step.get("id")
    # 根据实体信息，寻找跟踪任务。
    tracking_task_list = StrackGlobals.st.task.select("item_id=%s and step_id=%s" % (item_id, tracking_id))

    for task in tracking_task_list:
        tracking_version_list = StrackGlobals.st.version.select("task_id=%s" % task.get('id'),
                                                                order={"version": "desc"})
        tracking = False
        for version in tracking_version_list:
            tracking_publish_list = StrackGlobals.st.publish.select("version_id in %s" % version.get('id'))
            if not tracking_publish_list:
                continue
            if tracking:
                break
            # 导入文件
            for publish in tracking_publish_list:
                publish_type_id = publish.get("publish_type_id")
                publish_type = StrackGlobals.st.publishType.find("id=%s" % publish_type_id)
                if publish_type.get("name") == 'trk_nuke':
                    print(publish)
                    f = publish.get("file_path", {}).get("path")
                    tracking_full_path = get_full_path(StrackGlobals.st, StrackGlobals.current_project, f)
                    if tracking_full_path:
                        tracking_full_path = tracking_full_path.replace("\\", "/")
                        try:
                            nuke.nodePaste(tracking_full_path)
                            NukefileImport.change_root()
                            tracking = True
                        except:
                            # to break this verion import processing
                            tracking = True
                            nuke.message(u"跟踪文件出现问题，先看网页记录和文件夹信息是否一致")
                if publish_type.get("name") == 'trk_obj':
                    print(publish)
                    f = publish.get("file_path", {}).get("path")
                    obj_full_path = get_full_path(StrackGlobals.st, StrackGlobals.current_project, f)
                    if obj_full_path:
                        obj_full_path = obj_full_path.replace("\\", "/")
                        # try:
                        objnode = nuke.createNode("ReadGeo2")
                        objnode["file"].fromUserText(obj_full_path)
                        NukefileImport.change_root()
                if publish_type.get("name") == 'trk_fbx':
                    print(publish)
                    f = publish.get("file_path", {}).get("path")
                    camera_full_path = get_full_path(StrackGlobals.st, StrackGlobals.current_project, f)
                    if camera_full_path:
                        camera_full_path = camera_full_path.replace("\\", "/")
                        # try:
                        cameranode = nuke.createNode("Camera2")
                        cameranode["read_from_file"].setValue(1)
                        cameranode["file"].setValue(camera_full_path)


    # 获取mp环节的信息。
    try:
        mp_info = StrackGlobals.st.task.find("id=%s"%task_id,["custom"]).get("mp_info")
    except:
        mp_info = None
    # 获取mp环节的信息。
    mp_step = StrackGlobals.st.step.find("code=mattepaints")
    mp_id = mp_step.get("id")
    # 根据实体信息，寻找mp任务。
    if mp_info:
        mp_shot_code = mp_info
        mp_shot_id = StrackGlobals.st.shot.find("code=%s"%mp_shot_code).get("id")
        mp_task_list = StrackGlobals.st.task.select("item_id=%s and step_id=%s" % (mp_shot_id, mp_id))
        for task in mp_task_list:
            mp_version_list = StrackGlobals.st.version.select("task_id=%s" % task.get('id'), order={"version": "desc"})
            mp=False
            for version in mp_version_list:
                mp_publish_list = StrackGlobals.st.publish.select("version_id in %s" % version.get('id'))
                if not mp_publish_list:
                    continue
                if mp:
                    break
                # 导入文件
                for publish in mp_publish_list:
                    print publish
                    publish_type_id = publish.get("publish_type_id")
                    publish_type = StrackGlobals.st.publishType.find("id=%s" % publish_type_id)
                    if publish_type.get("name") == 'mp_img':
                        f = publish.get("file_path", {}).get("path")
                        mp_full_path = get_full_path(StrackGlobals.st, StrackGlobals.current_project, f)
                        if mp_full_path:
                            mp_full_path=mp_full_path.replace("\\","/")
                            if os.path.isdir(mp_full_path):
                                NukeReadImport.search_run(mp_full_path)
                            else:
                                mp_full_path = os.path.dirname(mp_full_path)
                                NukeReadImport.search_run(mp_full_path)
                            NukefileImport.change_root()
                            mp=True
                            break
    if not mp:
        mp_task_list = StrackGlobals.st.task.select("item_id=%s and step_id=%s" % (item_id, mp_id))
        for task in mp_task_list:
            mp_version_list = StrackGlobals.st.version.select("task_id=%s" % task.get('id'),
                                                              order={"version": "desc"})
            mp = False
            for version in mp_version_list:
                mp_publish_list = StrackGlobals.st.publish.select(
                    "version_id in %s" % version.get('id'))
                if not mp_publish_list:
                    continue
                if mp:
                    break
                # 导入文件
                for publish in mp_publish_list:
                    print
                    publish
                    publish_type_id = publish.get("publish_type_id")
                    publish_type = StrackGlobals.st.publishType.find("id=%s" % publish_type_id)
                    if publish_type.get("name") == 'mp_img':
                        f = publish.get("file_path", {}).get("path")
                        mp_full_path = get_full_path(StrackGlobals.st, StrackGlobals.current_project, f)
                        if mp_full_path:
                            mp_full_path = mp_full_path.replace("\\", "/")
                            if os.path.isdir(mp_full_path):
                                NukeReadImport.search_run(mp_full_path)
                            else:
                                mp_full_path = os.path.dirname(mp_full_path)
                                NukeReadImport.search_run(mp_full_path)
                            NukefileImport.change_root()
                            mp = True
                            break

    # 获取roto环节的信息。
    roto_step = StrackGlobals.st.step.find("code=roto")
    roto_id = roto_step.get("id")
    # 根据实体信息，寻找roto任务。
    roto_task_list = StrackGlobals.st.task.select("item_id=%s and step_id=%s" % (item_id, roto_id))

    for task in roto_task_list:
        roto_version_list = StrackGlobals.st.version.select("task_id=%s" % task.get('id'), order={"version": "desc"})
        roto = False
        for version in roto_version_list:
            roto_publish_list = StrackGlobals.st.publish.select("version_id in %s" % version.get('id'))
            if not roto_publish_list:
                continue
            if roto:
                break
            # 导入文件
            for publish in roto_publish_list:
                print
                publish
                publish_type_id = publish.get("publish_type_id")
                publish_type = StrackGlobals.st.publishType.find("id=%s" % publish_type_id)
                if publish_type.get("name") == 'EMATTES':
                    f = publish.get("file_path", {}).get("path")
                    roto_full_path = get_full_path(StrackGlobals.st, StrackGlobals.current_project, f)

                    if roto_full_path:
                        roto_full_path = roto_full_path.replace("\\", "/")
                        if os.path.isdir(roto_full_path):
                            NukeReadImport.search_run(roto_full_path)
                        else:
                            roto_full_path = roto_full_path.replace("%04d", "####").replace("[", "").replace("]", "")
                            readnode = nuke.createNode("Read")
                            readnode['file'].fromUserText(roto_full_path)
                        roto = True

    # 获取paint环节的信息。
    paint_step = StrackGlobals.st.step.find("code=paint")
    paint_id = paint_step.get("id")
    # 根据实体信息，寻找paint任务。
    paint_task_list = StrackGlobals.st.task.select("item_id=%s and step_id=%s" % (item_id, paint_id))

    for task in paint_task_list:
        paint_version_list = StrackGlobals.st.version.select("task_id=%s" % task.get('id'), order={"version": "desc"})
        paint = False
        for version in paint_version_list:
            paint_publish_list = StrackGlobals.st.publish.select("version_id in %s" % version.get('id'))
            if not paint_publish_list:
                continue
            if paint:
                break
            # 导入文件
            for publish in paint_publish_list:
                print
                publish
                publish_type_id = publish.get("publish_type_id")
                publish_type = StrackGlobals.st.publishType.find("id=%s" % publish_type_id)
                if publish_type.get("name") == 'IC':
                    f = publish.get("file_path", {}).get("path")
                    paint_full_path = get_full_path(StrackGlobals.st, StrackGlobals.current_project, f)
                    if paint_full_path:
                        paint_full_path = paint_full_path.replace("\\", "/")
                        if os.path.isdir(paint_full_path):
                            NukeReadImport.search_run(paint_full_path)
                        else:
                            paint_full_path = paint_full_path.replace("%04d", "####").replace("[", "").replace("]", "")
                            readnode = nuke.createNode("Read")
                            readnode['file'].fromUserText(paint_full_path)
                        paint = True

    # 获取render环节的信息。
    render_step = StrackGlobals.st.step.find("code=render")
    render_id = render_step.get("id")
    # 根据实体信息，寻找mp任务。
    render_task_list = StrackGlobals.st.task.select("item_id=%s and step_id=%s" % (item_id, render_id))

    for task in render_task_list:
        render_version_list = StrackGlobals.st.version.select("task_id=%s" % task.get('id'), order={"version": "desc"})
        render = False
        for version in render_version_list:
            render_publish_list = StrackGlobals.st.publish.select("version_id in %s" % version.get('id'))
            if not render_publish_list:
                continue
            if render:
                break
            # 导入文件
            for publish in render_publish_list:
                print
                publish
                publish_type_id = publish.get("publish_type_id")
                publish_type = StrackGlobals.st.publishType.find("id=%s" % publish_type_id)
                if publish_type.get("name") == 'render_exr':
                    f = publish.get("file_path", {}).get("path")
                    render_full_path = get_full_path(StrackGlobals.st, StrackGlobals.current_project, f)
                    if render_full_path:
                        render_full_path = render_full_path.replace("\\", "/")
                        if os.path.isdir(render_full_path):
                            NukeReadImport.search_run(render_full_path)
                        else:
                            render_full_path = os.path.dirname(render_full_path)
                            NukeReadImport.search_run(render_full_path)
                        NukefileImport.change_root()
                        render = True
                        break

    # 获取mp环节的信息。
    vfx_step = StrackGlobals.st.step.find("code=effects")
    vfx_id = vfx_step.get("id")
    # 根据实体信息，寻找mp任务。
    vfx_task_list = StrackGlobals.st.task.select("item_id=%s and step_id=%s" % (item_id, vfx_id))

    for task in vfx_task_list:
        vfx_version_list = StrackGlobals.st.version.select("task_id=%s" % task.get('id'), order={"version": "desc"})
        vfx = False
        for version in vfx_version_list:
            vfx_publish_list = StrackGlobals.st.publish.select("version_id in %s" % version.get('id'))
            if not vfx_publish_list:
                continue
            if vfx:
                break
            # 导入文件
            for publish in vfx_publish_list:
                print
                publish
                publish_type_id = publish.get("publish_type_id")
                publish_type = StrackGlobals.st.publishType.find("id=%s" % publish_type_id)
                if publish_type.get("name") == 'vfx_exr':
                    f = publish.get("file_path", {}).get("path")
                    vfx_full_path = get_full_path(StrackGlobals.st, StrackGlobals.current_project, f)
                    if vfx_full_path:
                        vfx_full_path = vfx_full_path.replace("\\", "/")
                        if os.path.isdir(vfx_full_path):
                            NukeReadImport.search_run(vfx_full_path)
                        else:
                            vfx_full_path = os.path.dirname(vfx_full_path)
                            NukeReadImport.search_run(vfx_full_path)
                        NukefileImport.change_root()
                        vfx = True
                        break
    nuke.message("tracking_nuke_file:%s\nmp_img_file:%s\nroto_emattes:%s\npaint_IC:%s\nrender_exr:%s\nvfx_exr:%s" % (
    tracking, mp, roto, paint, render, vfx))

    return