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

    if read_src_path:
        jpg_file=[x for x in nuke.getFileNameList(read_src_path) if "jpg" in x or "jpeg" in x][0]
        jpg_path=os.path.join(read_src_path,jpg_file)
    else:
        jpg_path=''
    read_undist2=nuke.createNode("Read")
    read_undist2['name'].setValue("src_file2")
    read_undist2['file'].fromUserText(jpg_path)
    read_undist2["xpos"].setValue(599)
    read_undist2["ypos"].setValue(10.0)
    basic_format=read_undist2["format"].toScript()
    nuke.addFormat('%s %s'%(basic_format,"basic_res"))

    scanlinerender=nuke.createNode("ScanlineRender")
    scanlinerender["xpos"].setValue(444)
    scanlinerender["ypos"].setValue(51)
    scanlinerender.setInput(2,cameranode)
    scanlinerender.setInput(0,read_undist2)
    scanlinerender.setInput(1,scene)


    reformat_undist2=nuke.createNode("Reformat")
    reformat_undist2["resize"].setValue(0)
    reformat_undist2.setInput(0,scanlinerender)
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
