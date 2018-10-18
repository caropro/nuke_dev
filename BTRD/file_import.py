
import BTRD
import candw
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
        self.path=""
        self.mpath=""
        path=QPushButton("file_browser")
        self.line=QLineEdit()
        self.ensure=QPushButton("Enter the mid path")
        self.linepath=QLineEdit()
        self.inputtype=QComboBox()
        self.inputtype.addItems(['jpeg','mov','exr','dpx'])
        importf=QPushButton("import")
        write=QPushButton("write")
        cancel=QPushButton("cancel")
        self.check=QCheckBox("Path_Filter")     

        layouta=QHBoxLayout()
        layouta.addWidget(path)
        layouta.addWidget(self.line)
        
        layoutb=QHBoxLayout()
        layoutb.addWidget(self.inputtype)
        layoutb.addWidget(importf)
        layoutb.addWidget(write)
        layoutb.addWidget(cancel)

        layoutc=QHBoxLayout()
        layoutc.addWidget(self.linepath)
        layoutc.addWidget(self.ensure)
        layoutc.addWidget(self.check)
        
        layoutd=QVBoxLayout()
        layoutd.addLayout(layouta)
        layoutd.addLayout(layoutc)
        layoutd.addLayout(layoutb)
        
        
        self.setLayout(layoutd)
 
        path.clicked.connect(self.find_path)
        importf.clicked.connect(self.search)
        write.clicked.connect(BTRD.main)
        cancel.clicked.connect(self.close)
        cancel.clicked.connect(self.reboot)
        self.ensure.clicked.connect(self.update)

        self.setWindowTitle("Standard Dialog")
    def update(self):
        text=self.linepath.text()
        if text:
            if nuke.ask('Input path is '+text+'?'):   
                nuke.message('the'+text+"will be the path factor")
                self.mpath=text
                self.ensure.setText("Change another path")
        else:
            nuke.message('empty input midname')
            self.mpath=text
                   
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
                    if not self.mpath:
                        self.mpath=readnode['name'].value()
                    self.finalpath=sum_name+r"/"+self.mpath+r"/"+real_name
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

form=file_import()

def run(func=form):
    func.show()

