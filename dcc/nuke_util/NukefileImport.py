# coding=utf8
# Copyright (c) 2017 CineUse
import os
import clique

from Qt import QtCore
from Qt import QtWidgets
from Qt import QtGui

import nuke
from std_pipeline.AssetHandler import AssetHandler
from strack_globals import StrackGlobals
from std_strack.get_full_path import get_full_path

import platform

#coding=utf-8
import nuke
import platform

def change_root():
    linux_root_dict = {"P:": "/projects/", "Q:": "/projects01/", "R:": "/projects02/", "T:": "/projects03/",
                       "U:": "/projects04/", "W:": "/projects05/","m:":"/projects06/"}
    win_root_dict = {"/projects/": "P:", "/projects01/": "Q:", "/projects02/": "R:", "/projects03/": "T:",
                     "/projects04/": "U:", "/projects05/": "W:","/projects06/":"m:"}
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
                if len(geo_head)==2:
                    try:
                        geo_path=geo_path.replace(geo_head,linux_root_dict[geo_head])
                        geo_node["file"].setValue(geo_path)
                    except:
                        continue
    else:
        if write_nodes:
            for write_node in write_nodes:
                write_path = write_node["file"].getValue()
                try:
                    write_head = "/"+write_path.split("/")[1] + "/"
                    if write_head.startswith("/project"):
                        write_path = write_path.replace(write_head, win_root_dict[write_head])
                        write_node["file"].setValue(write_path)
                except:
                    continue

        if read_nodes:
            for read_node in read_nodes:
                read_path = read_node["file"].getValue()
                try:
                    read_head = "/"+read_path.split("/")[1] + "/"
                    if read_head.startswith("/project"):
                        read_path = read_path.replace(read_head, win_root_dict[read_head])
                        read_node["file"].setValue(read_path)
                except:
                    continue
        if camera_nodes:
            for camera_node in camera_nodes:
                camera_path = camera_node["file"].getValue()
                try:
                    camera_head = "/"+camera_path.split("/")[1] + "/"
                    if camera_head.startswith("/project"):
                        camera_path = camera_path.replace(camera_head, win_root_dict[camera_head])
                        camera_node["file"].setValue(camera_path)
                except:
                    continue
        if geo_nodes:
            for geo_node in geo_nodes:
                geo_path = geo_node["file"].getValue()
                try:
                    geo_head = "/"+geo_path.split("/")[1] + "/"
                    if geo_head.startswith("/project"):
                        geo_path = geo_path.replace(geo_head, win_root_dict[geo_head])
                        geo_node["file"].setValue(geo_path)
                except:
                    continue


def create(self):
    print "create <<", self.item
    # 1. get data from item
    data = self.item.data(QtCore.Qt.UserRole)
    # 2. get version and publish info
    version_num, publish_info = data.get('current_version_publish')
    # 3. get publish path
    for pub in publish_info:
        publish_path = pub.get('file_path', {}).get('path')
        publish_path = get_full_path(StrackGlobals.st, StrackGlobals.current_project, publish_path)
        if not publish_path:
            raise ValueError('current publish path is none.')
        # 3.1 parse publish path
        format_publish_path = publish_path.replace("%04d", "####").replace("[", "").replace("]", "")
        format_publish_path=format_publish_path.replace("\\","/")
        # 4. do reference
        try:
            # change this line for every hook
            nuke.nodePaste(format_publish_path)
            print "xxxx"
            change_root()
            print "yyy"
            readNode = nuke.selectedNodes()
            self._file_read_nodes.append(readNode)
        except:
            print "%s reference failed." % publish_path
