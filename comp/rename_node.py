#coding=utf-8
import nuke
import platform

def run():
    linux_root_dict = {"P:": "/projects/", "Q:": "/projects01/", "R:": "/projects02/", "T:": "/projects03/",
                       "U:": "/projects04/", "W:": "/projects05/"}
    win_root_dict = {"/projects/": "P:", "/projects01/": "Q:", "/projects02/": "R:", "/projects03/": "T:",
                     "/projects04/": "U:", "/projects05/": "W:"}
    write_nodes = nuke.allNodes("Write")
    read_nodes = nuke.allNodes("Read")
    camera_nodes = nuke.allNodes("Camera2")
    geo_nodes = nuke.allNodes("ReadGeo2")

    if platform.system()=="Linux":
        print("linux")
        if write_nodes:
            for write_node in write_nodes:
                write_path=write_node["file"].getValue()
                write_head=write_path.split(":")[0]+":"
                print write_head
                if len(write_head)==2:
                    try:
                        write_path=write_path.replace(write_head,linux_root_dict[write_head])
                        write_node["file"].setValue(write_path)
                    except:
                        continue
        if read_nodes:
            for read_node in read_nodes:
                read_path=read_node["file"].getValue()
                read_head=read_path.split(":")[0]+":"
                if len(read_head)==2:
                    try:
                        read_path=read_path.replace(read_head,linux_root_dict[read_head])
                        read_node["file"].setValue(read_path)
                    except:
                        continue
        if camera_nodes:
            for camera_node in camera_nodes:
                camera_path=camera_node["file"].getValue()
                camera_head=camera_path.split(":")[0]+":"
                if len(camera_head)==2:
                    try:
                        camera_path=camera_path.replace(camera_head,linux_root_dict[camera_head])
                        camera_node["file"].setValue(camera_path)
                    except:
                        continue
        if geo_nodes:
            for geo_node in geo_nodes:
                geo_path=geo_node["file"].getValue()
                geo_head=geo_path.split(":")[0]+":"
                if len(geo_head)!=2:
                    geo_path=geo_path.replace(geo_head,linux_root_dict[geo_head])
                    geo_node["file"].setValue(geo_path)
    else:
        if write_nodes:
            for write_node in write_nodes:
                write_path = write_node["file"].getValue()
                write_head = "/"+write_path.split("/")[1] + "/"
                if write_head.startswith("/project"):
                    write_path = write_path.replace(write_head, win_root_dict[write_head])
                    write_node["file"].setValue(write_path)

        if read_nodes:
            for read_node in read_nodes:
                read_path = read_node["file"].getValue()
                read_head = "/"+read_path.split("/")[1] + "/"
                if read_head.startswith("/project"):
                    read_path = read_path.replace(read_head, win_root_dict[read_head])
                    read_node["file"].setValue(read_path)

        if camera_nodes:
            for camera_node in camera_nodes:
                camera_path = camera_node["file"].getValue()
                camera_head = "/"+camera_path.split("/")[1] + "/"
                if camera_head.startswith("/project"):
                    camera_path = camera_path.replace(camera_head, win_root_dict[camera_head])
                    camera_node["file"].setValue(camera_path)

        if geo_nodes:
            for geo_node in geo_nodes:
                geo_path = geo_node["file"].getValue()
                geo_head = "/"+geo_path.split("/")[1] + "/"
                if geo_head.startswith("/project"):
                    geo_path = geo_path.replace(geo_head, win_root_dict[geo_head])
                    geo_node["file"].setValue(geo_path)

def change_root():
    run()