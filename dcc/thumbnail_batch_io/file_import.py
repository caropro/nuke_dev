import batch_single_out_put
import nuke
import sys
import re
import os
import time
reload(sys)
sys.setdefaultencoding("utf-8")
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
        self.out_put_path=""
        path=QPushButton("file_browser")
        self.line=QLineEdit()
        self.ensure=QPushButton("output path")
        self.linepath=QLineEdit()
        self.time_date=QDateTimeEdit()
        self.time_date.setCalendarPopup(True)
        self.time_btn=QPushButton("time_confirm")
        self.inputtype=QComboBox()
        self.inputtype.addItems(['jpeg','mov','exr','dpx'])
        importf=QPushButton("import")
        write=QPushButton("write")
        cancel=QPushButton("cancel")

        layout_time=QHBoxLayout()
        layout_time.addWidget(self.time_date)
        layout_time.addWidget(self.time_btn)

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
        
        layoutd=QVBoxLayout()
        layoutd.addLayout(layout_time)
        layoutd.addLayout(layouta)
        layoutd.addLayout(layoutc)
        layoutd.addLayout(layoutb)
        
        
        self.setLayout(layoutd)
 
        path.clicked.connect(self.find_path)
        importf.clicked.connect(self.search)
        write.clicked.connect(batch_single_out_put.main)
        cancel.clicked.connect(self.close)
        cancel.clicked.connect(self.reboot)
        self.time_btn.clicked.connect(self.time_confirm)
        self.ensure.clicked.connect(self.update)

        self.setWindowTitle("thumbnail import Dialog")
        self.setModal(True)

    def time_confirm(self):
        self.time_code=self.time_date.dateTime().toTime_t()
        nuke.message("get the time data %s" % self.time_date.dateTime())


    def update(self):
        path=QFileDialog.getExistingDirectory(self,"Open Directory","\\")
        self.linepath.setText(path)
        if os.path.isdir(path):
            try:
                os.makedirs(path)
            except:
                pass
            self.out_put_path=path
        else:
            nuke.message("something wrong with the outputpath")

    def find_path(self):
        select_path=QFileDialog.getExistingDirectory(self,"Open Directory","\\")
        self.line.setText(str(select_path))
        self.path=select_path
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
                file_path = os.path.join(path,i)
                if os.path.isdir(file_path):
                     search_run(file_path)
                else:
                    if not "iplate" in file_path:
                        continue
                    pathfile=file_path
                    final_ctime = os.stat(path)
                    if not (final_ctime.st_ctime)>self.time_code:
                        print("break time {}".format(time.ctime(final_ctime.st_ctime)))
                        continue
                    tail_info=file_path.split(" ")[-1]
                    #the information about the sequence
                    #possible someone path_without_ext the folder with the space
                    file_path=file_path.replace(tail_info,'')
                    file_path=file_path.strip()

                    readnode=nuke.createNode("Read")
                    readnode['file'].fromUserText(pathfile)

                    path_without_ext=file_path.split(".")[0]
                    print("the path_without_ext is %s" % path_without_ext)
                    file_name=path_without_ext.split("\\")[-1]
                    #with the frame number
                    file_name=re.split("([#]+?)$",file_name)[0]
                    real_name=file_name
                    file_name=file_name.split("dp_")[-1].split("_bg")[0]
                    if file_name.startswith("I_"):
                        file_name.replace("I_","")
                    new_path=path_without_ext.split("\\")[:-1]

                    writenode=nuke.createNode("Write")
                    reformat = nuke.createNode("Reformat")
                    reformat["type"].setValue("scale")
                    reformat["scale"].setValue(0.5)
                    reformat.setInput(0,readnode)
                    writenode.setInput(0,reformat)
                    self.finalpath=os.path.normpath(os.path.join(self.out_put_path,file_name))
                    if self.inputtype.currentText()=="mov":
                        writenode["file"].fromUserText((self.finalpath+"."+self.type).replace("\\",'/'))
                        writenode["file_type"].setValue(str(self.type))
                    else:
                        writenode["file"].fromUserText((self.finalpath+"."+self.type).replace("\\",'/'))
                        writenode["file_type"].setValue(str(self.type))
                        try:
                            writenode["_jpeg_quality"].setValue(0.5)
                        except:
                            continue
                    # writenode["name"].setValue(real_name)
        if not self.path:
            nuke.message('NO Path here')
        elif self.path=='\\':
            if nuke.ask('Input path is rootpath,going to die?'):
                nuke.message('DieDieDieDieDieDieDieDie')
        else:
            search_run(self.path)

form=file_import()

def run(func=form):
    func.show()

