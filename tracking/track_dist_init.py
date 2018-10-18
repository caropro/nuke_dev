#coding=utf-8
import os
import nuke
def main():
    current_path=nuke.root()["name"].getValue()
    nuke.root()["fps"].setValue(25)
    step_root=current_path.split("nuke")[0]

    camera_path=os.path.normpath(os.path.join(step_root,"fbx"))
    obj_path=os.path.normpath(os.path.join(step_root,"obj"))
    sourceimage=os.path.normpath(os.path.join(step_root,"sourceimages"))

    try:
        read_src_dir=max([x for x in os.listdir(sourceimage) if not "undist" in x ])
        read_src_path=os.path.join(sourceimage,read_src_dir)
    except:
        nuke.message(u"get the sourceimage first!!")
        read_src_path=''

    dist_count=0
    try:
        read_dist_dir=max([x for x in os.listdir(sourceimage) if "undist" in x ])
        read_dist_path=os.path.join(sourceimage,read_dist_dir)
        dist_count=len([x for x in os.listdir(sourceimage) if "undist" in x ])
    except:
        read_dist_path=''
        nuke.message(u"doesn't have the export of undistortion")

    #distortin node
    dist_dir=os.path.normpath(os.path.join(step_root,"nuke"))
    try:
        dist_file=max([x for x in os.listdir(dist_dir) if "tracking_dist" in x and "auto" not in x])
        dist_path=os.path.join(dist_dir,dist_file)
    except:
        nuke.message(u"get the sourceimage first!!")
    #camera_path
    try:
        camera_file=max([x for x in os.listdir(camera_path)])
        camera_filepath=os.path.join(camera_path,camera_file).replace("\\","/")
    except:
        camera_filepath=''
    #obj_path
    try:
        obj_file=max([x for x in os.listdir(obj_path)])
        obj_filepath=os.path.join(obj_path,obj_file).replace("\\","/")
    except:
        obj_filepath=''
    #first_block_______________________________________________________________________________________________

    read_jpg=nuke.createNode("Read")
    read_jpg['name'].setValue("source_jpg")
    if read_src_path:
        jpg_file=[x for x in nuke.getFileNameList(read_src_path) if "jpg" in x or "jpeg" in x][0]
        jpg_path=os.path.join(read_src_path,jpg_file)
    else:
        jpg_path=''
    read_jpg['file'].fromUserText(jpg_path)
    read_jpg["xpos"].setValue(-301.0)
    read_jpg["ypos"].setValue(-117.0)

    basic_format=read_jpg["format"].toScript()
    nuke.addFormat('%s %s'%(basic_format,"basic_res"))

    reformat_jpg=nuke.createNode("Reformat")
    reformat_jpg["resize"].setValue(0)
    reformat_jpg.setInput(0,read_jpg)
    reformat_jpg["black_outside"].setValue(1)
    reformat_jpg["xpos"].setValue(-301.0)
    reformat_jpg["ypos"].setValue(19.0)

    nuke.nodePaste(dist_path)
    dist_node = nuke.selectedNodes()[0]
    dist_node["dst_hide"].setValue(1)
    dist_node["reverse"].setValue(1)
    dist_node["background"].setValue(0)
    dist_node["xpos"].setValue(-301.0)
    dist_node["ypos"].setValue(76.0)

    res=dist_node["name"].getValue().split("_")[-1]
    resx=res.split("x")[0]
    resy=res.split("x")[1]

    nuke.addFormat('%s %s %s'%(resx,resy,"current_res"))


    reformat_jpg["format"].setValue("current_res")
    dist_node.setInput(0,reformat_jpg)

    write_first=nuke.createNode("Write")
    version_first=dist_count+1
    dist_folder=read_src_dir+"_undist_v%02d"%version_first
    dist_name="{}.%04d.jpg".format(dist_folder)
    first_write_path=os.path.join(sourceimage,dist_folder,dist_name).replace("\\","/")
    write_first['file'].setValue(first_write_path)
    write_first["file_type"].setValue("jpeg")
    write_first["_jpeg_quality"].setValue(1)
    write_first.setInput(0,dist_node)

    write_first["xpos"].setValue(-301.0)
    write_first["ypos"].setValue(184.0)



    bdn_1=nuke.createNode("BackdropNode")
    dir(bdn_1)

    bdn_1["xpos"].setValue(-355.0)
    bdn_1["ypos"].setValue(-202.0)

    bdn_1["bdheight"].setValue(461)
    bdn_1["bdwidth"].setValue(198)

    bdn_1["label"].setValue("Undistortion\n\xe5\x8e\xbb\xe9\x99\xa4\xe9\x95\x9c\xe5\xa4\xb4\xe7\x95\xb8\xe5\x8f\x98")

    #second_block_______________________________________________________________________________________________

    read_undist=nuke.createNode("Read")
    read_undist['name'].setValue("undist_file")
    undist_file=nuke.getFileNameList(read_dist_path)[0]
    undist_path=os.path.join(read_dist_path,undist_file)
    read_undist['file'].fromUserText(undist_path)
    read_undist["xpos"].setValue(0)
    read_undist["ypos"].setValue(-117.0)



    nuke.nodePaste(dist_path)
    dist_node2 = nuke.selectedNodes()[0]
    dist_node2["dst_hide"].setValue(1)
    dist_node2["reverse"].setValue(0)
    dist_node2["background"].setValue(0)

    dist_node2["xpos"].setValue(0)
    dist_node2["ypos"].setValue(19)
    dist_node2.setInput(0,read_undist)


    reformat_undist=nuke.createNode("Reformat")
    reformat_undist["resize"].setValue(0)
    reformat_undist.setInput(0,dist_node2)
    reformat_undist["xpos"].setValue(0)
    reformat_undist["ypos"].setValue(130)
    reformat_undist["clamp"].setValue(1)
    try:
        reformat_undist["format"].setValue("basic_res")
    except:
        reformat_undist["format"].setValue("%s basic_res" % basic_format.split(" ")[-1])


    bdn_2=nuke.createNode("BackdropNode")

    bdn_2["xpos"].setValue(-55.0)
    bdn_2["ypos"].setValue(-202.0)

    bdn_2["bdheight"].setValue(461)
    bdn_2["bdwidth"].setValue(198)

    bdn_2["label"].setValue("Redistortion\n\xe8\xbf\x98\xe5\x8e\x9f\xe9\x95\x9c\xe5\xa4\xb4\xe7\x95\xb8\xe5\x8f\x98")

    #thrid_block_______________________________________________________________________________________________
    checker=nuke.createNode("CheckerBoard2")
    checker["xpos"].setValue(444)
    checker["ypos"].setValue(-239)

    readgeo=nuke.createNode("ReadGeo2")
    readgeo["file"].fromUserText(obj_filepath)
    readgeo["xpos"].setValue(444)
    readgeo["ypos"].setValue(-150)
    readgeo.setInput(0,checker)

    scene=nuke.createNode("Scene")
    scene["display"].setValue(1)
    scene["xpos"].setValue(454)
    scene["ypos"].setValue(-80)
    scene.setInput(0,readgeo)

    cameranode = nuke.createNode("Camera2")
    cameranode["read_from_file"].setValue(1)
    cameranode["frame_rate"].setValue(25)
    cameranode["file"].fromUserText(camera_filepath)
    cameranode["xpos"].setValue(284)
    cameranode["ypos"].setValue(31)

    read_undist2=nuke.createNode("Read")
    read_undist2['name'].setValue("undist_file2")
    read_undist2['file'].fromUserText(undist_path)
    read_undist2["xpos"].setValue(599)
    read_undist2["ypos"].setValue(10.0)

    scanlinerender=nuke.createNode("ScanlineRender")
    scanlinerender["xpos"].setValue(444)
    scanlinerender["ypos"].setValue(51)
    scanlinerender.setInput(2,cameranode)
    scanlinerender.setInput(0,read_undist2)
    scanlinerender.setInput(1,scene)

    nuke.nodePaste(dist_path)
    dist_node3 = nuke.selectedNodes()[0]
    dist_node3["reverse"].setValue(0)
    dist_node3["background"].setValue(0)
    dist_node3["dst_hide"].setValue(1)
    dist_node3["xpos"].setValue(444)
    dist_node3["ypos"].setValue(129)
    dist_node3.setInput(0,scanlinerender)

    reformat_undist2=nuke.createNode("Reformat")
    reformat_undist2["resize"].setValue(0)
    reformat_undist2.setInput(0,dist_node3)
    reformat_undist2["xpos"].setValue(444)
    reformat_undist2["ypos"].setValue(230)
    reformat_undist2["clamp"].setValue(1)
    try:
        reformat_undist2["format"].setValue("basic_res")
    except:
        reformat_undist2["format"].setValue("%s basic_res" % basic_format.split(" ")[-1])

    bdn_3=nuke.createNode("BackdropNode")

    bdn_3["xpos"].setValue(271)
    bdn_3["ypos"].setValue(-267.0)

    bdn_3["bdheight"].setValue(600)
    bdn_3["bdwidth"].setValue(500)

