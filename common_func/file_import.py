# coding=utf8
import batch_render_front
import nuke
import sys
import re
import os
try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
from nukescripts import panels
import multiprocessing


class file_import(QDialog):
    def __init__(self,parent=None):
        super(file_import,self).__init__(parent)
        self.setWindowTitle(u"导入路境内所有可导入的文件")
        self.path=""
        self.search_path_dir=""
        self.ui_setup()
        self.connection_setup()
        
        
    def ui_setup(self):
        self.path_finder_btn=QPushButton("file_browser")
        self.line=QLineEdit()
        #路径中含有此段内容才会通过查询
        self.ensure=QPushButton("Enter the mid path")
        self.linepath=QLineEdit()
        self.inputtype=QComboBox()
        #默认的几类输出格式
        self.inputtype.addItems(['jpeg','mov','exr','dpx'])
        self.import_btn=QPushButton("import")
        self.write_btn=QPushButton("write")
        self.cancel_btn=QPushButton("cancel")
        #点击确认之后才会使用上边的mid path去查询
        self.check=QCheckBox("Path_Filter")     

        layouta=QHBoxLayout()
        layouta.addWidget(self.path_finder_btn)
        layouta.addWidget(self.line)
        
        layoutb=QHBoxLayout()
        layoutb.addWidget(self.inputtype)
        layoutb.addWidget(self.import_btn)
        layoutb.addWidget(self.write_btn)
        layoutb.addWidget(self.cancel_btn)

        layoutc=QHBoxLayout()
        layoutc.addWidget(self.linepath)
        layoutc.addWidget(self.ensure)
        layoutc.addWidget(self.check)
        
        layoutd=QVBoxLayout()
        layoutd.addLayout(layouta)
        layoutd.addLayout(layoutc)
        layoutd.addLayout(layoutb)

        self.setLayout(layoutd)
 
    def connection_setup(self):
        self.path_finder_btn.clicked.connect(self.find_path)
        self.import_btn.clicked.connect(self.search)
        self.write_btn.clicked.connect(batch_render_front.main)
        self.cancel_btn.clicked.connect(self.close)
        self.ensure.clicked.connect(self.update)

        self.setWindowTitle("Standard Dialog")
    def update(self):
        current_path_text=self.linepath.text()
        if current_path_text:
            if nuke.ask('Input path is %s?'%current_path_text):   
                nuke.message("The %s will be the path factor" % current_path_text)
                self.search_path_dir=current_path_text
                self.ensure.setText("Change another path")
        else:
            nuke.message('empty input midname')
            self.search_path_dir=current_path_text
                   
    def find_path(self):
        s=QFileDialog.getExistingDirectory(self,"Open Directory","/")
        self.line.setText(str(s))
        self.path=s
        print(self.path)         
    def reboot(self):
        self.line.setText('')
        self.path='' 
        self.linepath.setText('')
        print("reset success")    
    def search(self): 
        def search_run(path):
            self.type=self.inputtype.currentText()
            sum_name=None
            n=None
            final=[]
            n=nuke.getFileNameList(path)
            for i in n:
                m = os.path.join(path,i)
                if os.path.isdir(m):
                     search_run(m)
                else:
                    pathfile=m
                    tmp=m.split(" ")[-1]
                    m=m.replace(tmp,'')
                    m=m.strip()
                    #print m
                    readnode=nuke.createNode("Read")
                    readnode['file'].fromUserText(pathfile)

                    name=m.split(".")[0]
                    #print(name)
                    real_name=name.split("/")[-1]
                    real_name=re.split("([#]+?)$",real_name)[0]
                    #print(real_name)
                    new=name.split("/")[:-1]
                    sum_name=''
                    #print(new)
                    if self.check.isChecked():
                        for i in new:
                            c=re.search(r'(\w+\d+)$', i)
                            if c:
                                first=(new.index(i))
                                break
                            else:
                                first=len(new)
                        final=new[:first+1]
                    else:
                        final=new
                    #print(self.check.isChecked())
                    #print(final)
                    for sec in final:
                        if sum_name:
                            sum_name=sum_name+'/'+sec+'/'
                        else:
                            sum_name=sec
                    sum_name=sum_name.replace("//",'/')
                    print(sum_name)                      
                    writenode=nuke.createNode("Write")
                    writenode.setInput(0,readnode)
                    if not self.search_path_dir:
                        self.search_path_dir=readnode['name'].value()
                    self.finalpath=sum_name+r"/"+self.search_path_dir+r"/"+real_name
                    self.finalpath=self.finalpath.replace("//",'/')
                    #print(real_name) 
                    if self.inputtype.currentText()=="mov":
                        writenode["file"].setValue(self.finalpath+"."+self.type)
                        writenode["file_type"].setValue(str(self.type))
                    else:
                        writenode["file"].setValue(self.finalpath+"_%04d."+self.type)
                        writenode["file_type"].setValue(str(self.type))
                        try:
                            writenode["_jpeg_quality"].setValue(1)
                        except:
                            continue   
        if not self.path:
            nuke.message('NO Path here')
        elif self.path=='/':
            if nuke.ask('Input path is rootpath,going to die?'):
                nuke.message('DieDieDieDieDieDieDieDie')
        else:
            search_run(self.path) 


def run():
    func = file_import()
    func.show()

