# import nuke

# def candw():
# 	a=None
# 	b=None
# 	s=None
# 	#filePath = nuke.getFilename('Get File Contents', '*.*')
# 	seqPath = nuke.getClipname('Get Sequence')

# 	n=seqPath
# 	n=n.split(" ")[0]
# 	a=nuke.nodes.Read(file=n)
# 	name=n.split(".")[0]
# 	nm=name.split("/")[-1]
# 	n=name.split("/")[:-1]
# 	s=''
# 	for i in n:
# 		s=s+"/"+i
# 	print(name)
# 	nuke.knobDefault("Write.file", s+r"/"+a['name'].value()+"/"+nm+"_%04d.jpg")
# 	b=nuke.createNode("Write")
# 	b.setInput(0,a)

import os
import nuke

def candw():
    path=nuke.getClipname('Get Sequence',multiple=True)[0]
    def search(path):
        sum_name=None
        n=None
        n=nuke.getFileNameList(path)
        for i in n:
            m = os.path.join(path,i)
            if os.path.isdir(m):
                 search(m)
            else:
                pathfile=m
                tmp=m.split(" ")[-1]
                m=m.replace(tmp,'')
                m=m.strip()
                print m
                readnode=nuke.createNode("Read")
                readnode['file'].fromUserText(pathfile)
                
                name=m.split(".")[0]
                real_name=name.split("/")[-1]
                new=name.split("/")[:-1]
                sum_name=''
                for i in new:
                    sum_name=sum_name+"/"+i
                print(sum_name)
                writenode=nuke.createNode("Write")
                writenode.setInput(0,readnode)
                writenode["file"].setValue(sum_name+r"/"+readnode['name'].value()+r"/"+real_name+"_%04d.jpg")
    search(path)


# def candw():
#     path=nuke.getClipname('Get Sequence',multiple=True)[0]
#     def search(path):
#         sum_name=None
#         n=None
#         n=nuke.getFileNameList(path)
#         for i in n:
#             m = os.path.join(path,i)
#             if os.path.isdir(m):
#                  search(m)
#             else:

#                 rangframe=m.split(' ')[-1]
#                 firstframe=int(rangframe.split("-")[0])
#                 lastframe=int(rangframe.split('-')[1]) 

#                 tmp=m.split(" ")[-1]
#                 m=m.replace(tmp,'')
#                 m=m.strip()
#                 print m
#                 readnode=nuke.nodes.Read(file=m)
#                 readnode["first"].setValue(firstframe)
#                 readnode["last"].setValue(lastframe)
#                 name=m.split(".")[0]
#                 real_name=name.split("/")[-1]
#                 new=name.split("/")[:-1]
#                 sum_name=''
#                 for i in new:
#                     sum_name=sum_name+"/"+i
#                 print(sum_name)
#                 writenode=nuke.createNode("Write")
#                 writenode.setInput(0,readnode)
#                 writenode["file"].setValue(sum_name+r"/"+readnode['name'].value()+r"/"+real_name+"_%04d.jpg")
#     search(path)
