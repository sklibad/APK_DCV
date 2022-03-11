from PyQt6 import QtCore, QtGui, QtWidgets
from draw import Draw
from algorithms import Algorithms


class Ui_MainForm(object):
    algorithms = Algorithms()
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(1068, 569)
        self.horizontalLayout = QtWidgets.QHBoxLayout(MainForm)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.canvas = Draw(MainForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(sizePolicy)
        self.canvas.setMaximumSize(QtCore.QSize(931, 561))
        self.canvas.setToolTipDuration(-2)
        self.canvas.setObjectName("canvas")
        self.horizontalLayout.addWidget(self.canvas)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(MainForm)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(MainForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(MainForm)
        self.label.setToolTipDuration(-3)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.pushButton_2 = QtWidgets.QPushButton(MainForm)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(MainForm)
        self.pushButton_3.clicked.connect(self.insertFile) # type: ignore
        self.pushButton.clicked.connect(self.switchAlgorithm) # type: ignore
        self.pushButton_2.clicked.connect(self.analyze) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Widget"))
        self.pushButton_3.setText(_translate("MainForm", "Insert file"))
        self.pushButton.setText(_translate("MainForm", "Switch algorithm"))
        self.label.setText(_translate("MainForm", "Winding number"))
        self.pushButton_2.setText(_translate("MainForm", "Analyze"))

    def insertFile(self):
        self.canvas.insertFile()
        self.canvas.rescaleData()

    def switchAlgorithm(self):
        self.algorithms.setSource()

        if self.algorithms.isWindingNumber():
            # Ray crossing algorithm active
            self.label.setText("Ray crossing")
        else:
            # Winding number algorithm active
            self.label.setText("Winding number")

    def analyze(self):
        q = self.canvas.getPoint()
        pols = self.canvas.getPolygons()
        self.canvas.clearResPol()
        for pol in pols:
            # For each polygon
            if self.algorithms.isWindingNumber():
                res = self.algorithms.rayCasting(q, pol)
            else:
                res = self.algorithms.getPositionPointAndPolygon(q, pol)
            if res == 1:
                print("inside")
                # If point is inside polygon
                self.canvas.setResPol(pol)
                break
            elif res == -1:
                print("colinear")
                # If point is colinear
                self.canvas.setResPol(pol)

        self.canvas.update()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QWidget()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())