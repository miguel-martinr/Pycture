# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'template.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(963, 595)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(0, 0, 75, 24))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(70, 0, 75, 24))
        self.pushButton_4.setObjectName("pushButton_4")
        self.App = QtWidgets.QFrame(Form)
        self.App.setGeometry(QtCore.QRect(-1, -1, 961, 591))
        self.App.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.App.setFrameShadow(QtWidgets.QFrame.Raised)
        self.App.setObjectName("App")
        self.tabWidget = QtWidgets.QTabWidget(self.App)
        self.tabWidget.setGeometry(QtCore.QRect(0, 20, 521, 551))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.graphicsView = QtWidgets.QGraphicsView(self.tab)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 521, 521))
        self.graphicsView.setObjectName("graphicsView")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.tab_2)
        self.graphicsView_2.setGeometry(QtCore.QRect(0, 0, 321, 451))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.tab_2)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(0, 430, 321, 20))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.tabWidget.addTab(self.tab_2, "")
        self.label = QtWidgets.QLabel(self.App)
        self.label.setGeometry(QtCore.QRect(10, 570, 91, 21))
        self.label.setObjectName("label")
        self.App.raise_()
        self.pushButton.raise_()
        self.pushButton_4.raise_()

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "File"))
        self.pushButton_4.setText(_translate("Form", "Edit"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Tab 2"))
        self.label.setText(_translate("Form", "TextLabel"))
