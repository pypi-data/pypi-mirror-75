from PyQt5.QtWidgets import *
import sys
import os
import mne

class OpenFileOrDirDialog(QFileDialog):
    def __init__(self,*args):
        QFileDialog.__init__(self,*args)
        self.setOptions(QFileDialog.DontUseNativeDialog)
        self.setFileMode(QFileDialog.ExistingFile) # use QFileDialog.ExstingFiles if wanting to open multiple files/dirs
        buttons = self.findChildren(QPushButton)
        for button in buttons:
            if 'open' in str(button.text()).lower():
                self.openFileButton=button
        self.openFileButton.clicked.disconnect()
        self.openFileButton.clicked.connect(self.openClicked)
        self.tree= self.findChild(QTreeView)

    def openClicked(self):
        inds = self.tree.selectionModel().selectedIndexes()
        files = []
        for i in inds:
            if i.column()==0:
                files.append(os.path.join(str(self.directory().absolutePath()),str(i.data())))
        self.selectedFiles = files
        self.hide()

    def filesSelected(self):
        return self.selectedFiles[0]


# ---- test ----------------------------------------------------
# app = QApplication(sys.argv)
# main_window = QWidget()
# main_window.show()
# dialog = OpenFileOrDirDialog(main_window)
# dialog.exec_()
# fpath=dialog.filesSelected() #selectedFiles()
# raw = mne.io.read_raw_ctf(fpath, preload=True)
# print(fpath)
# sys.exit(app.exec_())


