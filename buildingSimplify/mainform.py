from PyQt6 import QtCore, QtGui, QtWidgets
from draw import Draw
from algorithms import Algorithms
from math import *
import sys


class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(895, 600)
        self.horizontalLayout = QtWidgets.QHBoxLayout(MainForm)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Canvas = Draw(MainForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Canvas.sizePolicy().hasHeightForWidth())
        self.Canvas.setSizePolicy(sizePolicy)
        self.Canvas.setObjectName("Canvas")
        self.horizontalLayout.addWidget(self.Canvas)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(MainForm)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(MainForm)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(MainForm)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(MainForm)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.pushButton_2 = QtWidgets.QPushButton(MainForm)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(MainForm)
        self.pushButton_3.clicked.connect(self.insertFile)  # type: ignore
        self.pushButton.clicked.connect(self.simplifyClick) # type: ignore
        self.pushButton_2.clicked.connect(self.clearClick) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def insertFile(self):
        self.Canvas.insertFile()
        self.Canvas.rescaleData()
        pass

    def simplifyClick(self):
        # Get polygon
        polygons = self.Canvas.getPolygons()
        a = Algorithms()
        er_list = []
        for pol in polygons:
            if self.comboBox.currentIndex() == 0:
                try:
                    er = a.minAreaEnclosingRectangle(pol)
                except:
                    continue
            elif self.comboBox.currentIndex() == 1:
                try:
                    main_dir = a.reduceGains(pol)
                    er = a.wallAverage(pol, main_dir)
                except:
                    continue
            else:
                try:
                    er = a.longestEdge(pol)
                except:
                    continue
            er_list.append(er)

        # Set MAER
        self.Canvas.setEnclosingRectangles(er_list)

        # Repaint
        self.Canvas.repaint()

    def clearClick(self):
        self.Canvas.delPolygons()
        self.Canvas.delEnclosingRectangles()
        self.Canvas.repaint()
        pass

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "BuildingSimplify"))
        self.label.setText(_translate("MainForm", "Select method"))
        self.comboBox.setItemText(0, _translate("MainForm", "Minimum BR"))
        self.comboBox.setItemText(1, _translate("MainForm", "Wall Average"))
        self.comboBox.setItemText(2, _translate("MainForm", "Longest edge"))
        self.pushButton_3.setText(_translate("MainForm", "Insert file"))
        self.pushButton.setText(_translate("MainForm", "Simplify"))
        self.pushButton_2.setText(_translate("MainForm", "Clear"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QWidget()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())
