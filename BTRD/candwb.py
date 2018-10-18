import nuke

def candw():
	a=None
	b=None
	s=None
	#filePath = nuke.getFilename('Get File Contents', '*.*')
	seqPath = nuke.getClipname('Get Sequence')
	#n=filePath
	n=seqPath
	judge=n.split(" ")
	a=nuke.createNode('Read')
	a['file'].fromUserText(n)
	# if len(judge)==1:
	# 	a=nuke.createNode('Read')
	# 	a['file'].fromUserText(n)
	# else:
	# 	rangframe=n.split(' ')[-1]
	# 	firstframe=int(rangframe.split("-")[0])
	# 	lastframe=int(rangframe.split('-')[1])
	# 	n=n.split(" ")[0]
	# 	a=nuke.nodes.Read(file=n)

	# 	a["first"].setValue(firstframe)
	# 	a["last"].setValue(lastframe)

	name=n.split(".")[0]
	nm=name.split("/")[-1]
	n=name.split("/")[:-1]
	s=''
	for i in n:
		s=s+"/"+i
	print(name)
	b=nuke.createNode("Write")
	b["file"].setValue(s+r"/"+a['name'].value()+"/"+nm+"_%04d.jpg")
	b.setInput(0,a)

# import os
# import nuke

# def candw():
#     path=nuke.getClipname('Get Sequence')
#     def search(path):
#         sum_name=None
#         n=None
#         n=nuke.getFileNameList(path)
#         for i in n:
#             m = os.path.join(path,i)
#             if os.path.isdir(m):
#                  search(m)
#             else:
#                 tmp=m.split(" ")[-1]
#                 m=m.replace(tmp,'')
#                 m=m.strip()
#                 print m
#                 readnode=nuke.nodes.Read(file=m)
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
