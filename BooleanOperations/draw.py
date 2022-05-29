from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from edge import *
from typing import List
from qpointfb import *
import os

class Draw(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.polA: List[QPointFB] = []
        self.polB: List[QPointFB] = []
        self.res: List[Edge] = []

    def insertFile(self, load_polA = True):
        # Shapefile path
        path = QFileDialog.getOpenFileName(self)[0]
        # Read textfile
        with open(path) as f:
            lines = f.readlines()
            # For each line (point) in text file
            for l in lines:
                p = l.split(" ")
                p[0] = float(p[0])
                p[1] = float(p[1])
                q = QPointFB(p[0], p[1])

                if load_polA:
                    self.polA.append(q)
                else:
                    self.polB.append(q)
        return os.path.basename(path)

    def paintEvent(self, e: QPaintEvent):
        # Create graphic object
        qp = QPainter(self)

        # Start draw
        qp.begin(self)

        # Set pen
        qp.setPen(Qt.GlobalColor.black)

        #Draw polygon A
        qp.setPen(Qt.GlobalColor.blue)
        q_polA = QPolygonF()
        for p in self.polA:
            q_polA.append(p)
        qp.drawPolygon(q_polA)

        #Draw polygon B
        qp.setPen(Qt.GlobalColor.green)
        q_polB = QPolygonF()
        for p in self.polB:
            q_polB.append(p)
        qp.drawPolygon(q_polB)

        # Draw results
        qp.setPen(Qt.GlobalColor.red)
        for e in self.res:
            qp.drawLine(e.getStart(), e.getEnd())

        # End draw
        qp.end()

    def getPolygons(self):
        return self.polA, self.polB

    def setResults(self, edges):
        self.res = edges

    def clearResults(self):
        self.res.clear()

    def clearCanvas(self):
        self.polA.clear()
        self.polB.clear()
        self.res.clear()
