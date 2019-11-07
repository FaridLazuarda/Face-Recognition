# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog,QPixmap
from extractormatcher import *
from pathlib import Path
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(420, 439)
        
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.Cosine_Similarity = QtGui.QRadioButton(self.groupBox)
        self.Cosine_Similarity.setObjectName(_fromUtf8("Cosine_Similarity"))
        self.gridLayout_2.addWidget(self.Cosine_Similarity, 4, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.valueT = QtGui.QLineEdit(self.groupBox)
        self.valueT.setObjectName(_fromUtf8("valueT"))
        self.horizontalLayout.addWidget(self.valueT)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(self.groupBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 374, 203))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        self.photo = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.photo.setObjectName(_fromUtf8("photo_2"))
        self.verticalLayout.addWidget(self.photo)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 6, 0, 1, 1)
        
        self.Euclid_distance = QtGui.QRadioButton(self.groupBox)
        self.Euclid_distance.setObjectName(_fromUtf8("Euclid_distance"))
        self.gridLayout_2.addWidget(self.Euclid_distance, 3, 0, 1, 1)
        self.show = QtGui.QPushButton(self.groupBox)
        self.show.setObjectName(_fromUtf8("show"))
        self.show.clicked.connect(lambda : self.btn_click(self.Euclid_distance.isChecked(),self.valueT.text()))
        self.gridLayout_2.addWidget(self.show, 5, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form) 


    def btn_click(self, check, le):
        filename = QFileDialog.getOpenFileName()
        self.label_2.setPixmap(QPixmap(filename))
        filename=str(filename)
        filename=filename.split('/')[-1]
        if check :
            name, match = ma.matchEcl(os.path.join(image_test,filename),int(le))
        else:
            name, match = ma.matchCos(os.path.join(image_test,filename),int(le))
        for i in range(int(le)):
            self.photo = QtGui.QLabel(self.scrollAreaWidgetContents)
            self.photo.setObjectName(_fromUtf8("photo"))
            self.photo.setAlignment(QtCore.Qt.AlignCenter)
            self.photo.setPixmap(QPixmap(os.path.join(image_ref,name[i])))
            self.verticalLayout.addWidget(self.photo)
            self.label = QtGui.QLabel(self.scrollAreaWidgetContents)
            self.label.setScaledContents(True)
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.setObjectName(_fromUtf8("label_2"))
            self.verticalLayout.addWidget(self.label)
            self.label.setText(_translate("Form",str(i+1),None))

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Face Recognition", None))
        self.groupBox.setTitle(_translate("Form","Main Window",None))
        self.Cosine_Similarity.setText(_translate("Form", "Cosine Similarity", None))
        self.label_2.setText(_translate("Form", " ", None))
        self.label.setText(_translate("Form", "Banyak foto yang ingin ditampilkan", None))
        
        self.photo.setText(_translate("Form", " ", None))
        self.Euclid_distance.setText(_translate("Form", "Euclidean Distance", None))
        self.show.setText(_translate("Form", "Pilih foto yang ingin dicocokkan dan Tampilkan", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ma=Matcher()
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

