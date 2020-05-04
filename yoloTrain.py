import os, signal
import subprocess
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class_main = uic.loadUiType('yoloTrain.ui')[0]
form_class_editor = uic.loadUiType('textEditor.ui')[0]

class WindowClass(QMainWindow, form_class_main):
    filepath = ''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fname1, self.fname2, self.fname3, self.fname4 = None, None, None, None
        self.size = ''
        self.path = ''  #edit here
        self.toolButton.clicked.connect(lambda: self.ToolButtonClick(1))
        self.toolButton_2.clicked.connect(lambda: self.ToolButtonClick(2))
        self.toolButton_3.clicked.connect(lambda: self.ToolButtonClick(3))
        self.toolButton_4.clicked.connect(lambda: self.ToolButtonClick(4))
        self.pushButton.clicked.connect(lambda: self.pushButtonClick(1))
        self.pushButton_2.clicked.connect(lambda: self.pushButtonClick(2))
        self.pushButton_3.clicked.connect(lambda: self.pushButtonClick(3))
        self.pushButton_4.clicked.connect(lambda: self.pushButtonClick(4))
        self.editButton.clicked.connect(lambda: self.editButtonClick(1))
        self.editButton_2.clicked.connect(lambda: self.editButtonClick(2))
        self.lineEdit.textChanged.connect(self.lineEdited)

    def ToolButtonClick(self, sel):
        fname = QFileDialog.getOpenFileName(self)
        if sel == 1:
            self.fname1 = fname[0]
            self.textBrowser.setPlainText(self.fname1)    
        elif sel == 2:
            self.fname2 = fname[0]
            self.textBrowser_2.setPlainText(self.fname2)    
        elif sel == 3:
            self.fname3 = fname[0]
            self.textBrowser_3.setPlainText(self.fname3)
        elif sel == 4:
            self.fname4 = fname[0]
            self.textBrowser_4.setPlainText(self.fname4)

    def pushButtonClick(self, sel):
        if sel == 1:
            if None in (self.fname1, self.fname2, self.fname3):
                self.showDialog('missing path')
                return
            else:
                cmd = f'cd {self.path}; ./darknet detector train {self.fname1} {self.fname2} {self.fname3}'
        elif sel == 2:
            if None in (self.fname1, self.fname2, self.fname3):
                self.showDialog('missing path')
                return
            else:
                cmd = f'cd {self.path}; ./darknet detector train {self.fname1} {self.fname2} {self.fname3} -map'
        elif sel == 3:
            if None in (self.fname1, self.fname2, self.fname3, self.fname4):
                self.showDialog('missing path')
                return
            else:
                cmd = f'cd {self.path}; ./darknet detector demo {self.fname1} {self.fname2} {self.fname3} -ext_output {self.fname4}'
        elif sel == 4:
            if self.fname1 is None:
                self.showDialog('missing path')
            elif self.size == '':
                self.showDialog('size')
            else:
                cmd = f'cd {self.path}; echo | ./darknet detector calc_anchors {self.fname1} -num_of_clusters 9 -width {self.size} -height {self.size}'
            return
        
        try:
            res = subprocess.check_output(cmd, shell=True)
            if sel == 4:
                self.anchors = res.decode('utf-8').split('\n')[-2]
                self.showDialog(self.anchors)
        except subprocess.CalledProcessError:
            self.showDialog('error')

    def editButtonClick(self, sel):
        if sel == 1:
            WindowClass.filepath = self.textBrowser.toPlainText()
        else:
            WindowClass.filepath = self.textBrowser_2.toPlainText()
        
        if WindowClass.filepath != '':
            self.editor = TextEditor()
            self.editor.show()


    def showDialog(self, sel):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        if sel == 'missing path':
            msgBox.setText('파일 경로를 지정하세요.')
        elif sel == 'size':
            msgBox.setText('사이즈 값을 입력하세요.')
        elif sel == 'error':
            msgBox.setText('실행 오류. 경로를 확인하세요.')
        else:
            msgBox.setText(sel)
        msgBox.setWindowTitle('Warning')
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def lineEdited(self):
        self.size = self.lineEdit.text()


class TextEditor(QMainWindow, form_class_editor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.content = self.file_open()
        self.plainTextEdit.setPlainText(self.content)
        self.pushButton.clicked.connect(self.pushButtonClick)

    def file_open(self):
        file = open(WindowClass.filepath, 'r')
        text = file.read()
        file.close()
        return text

    def pushButtonClick(self):
        file = open(WindowClass.filepath, 'w')
        file.write(self.plainTextEdit.toPlainText())
        file.close()
        self.close()




def main():
    app = QApplication(sys.argv)
    form = WindowClass()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
