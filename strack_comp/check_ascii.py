#coding=utf-8
#author:Jonathon Woo
#version:1.0.0
import nuke

def check_node_ascii():
    nodes = nuke.allNodes()
    error_list=[]
    for node in nodes:
    #check the node name
        context_name=node.name()
        print isinstance(context_name, str)
        org_name_length=len(context_name)
        utf_name_length=len(context_name.decode('utf-8'))
        if org_name_length!=utf_name_length:
            print "!!!!!"
            nuke.message("中文警告:%s"%node.name())
            node.setSelected(True)
            error_list.append("node")
            continue
    #check the node label
        context=node["label"].getValue()
        print isinstance(context, str)
        org_length=len(context)
        utf_length=len(context.decode('utf-8'))
        if org_length!=utf_length:
            print "!!!!!"
            nuke.message("中文警告:%s"%node.name())
            node.setSelected(True)
            error_list.append("node")
            continue
    #check io node's file path
        file_path_type_list=["Read","Write","Camera2","ReadGeoi2"]
        if node.Class() in file_path_type_list:
            context_file=node["file"].getValue()
            print isinstance(context_file, str)
            org_file_length=len(context_file)
            utf_file_length=len(context_file.decode('utf-8'))
            if org_file_length!=utf_file_length:
                print "!!!!!"
                nuke.message("中文警告:%s"%node.name())
                node.setSelected(True)
                error_list.append("node")
                continue
                    # check roto node's layer
    #check roto node
        if node.Class() == "Roto":
            c_knob = node.knob("curves")
            context_file = c_knob.rootLayer.serialise()
            print
            isinstance(context_file, str)
            org_file_length = len(context_file)
            utf_file_length = len(context_file.decode('utf-8'))
            if org_file_length != utf_file_length:
                print
                "!!!!!"
                nuke.message("中文警告:%s" % node.name())
                node.setSelected(True)
                error_list.append("node")
                continue
    return nuke.message("Done.\nerror nodes count:%s"%len(error_list))