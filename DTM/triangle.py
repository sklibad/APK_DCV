from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from math import *
from qpoint3D import *
from edge import *
from typing import List
from numpy import *
from edge import *

class Triangle:
    def __init__(self, p1: Edge, p2: Edge, p3: Edge):
        self.p1 = p1.getStart()
        self.p2 = p2.getStart()
        self.p3 = p3.getStart()
        self.qPolygon = QPolygonF()
        self.col = None

    def getNormalVector(self):
        # Calculates normal vector of triangle and creates QPolygonF object

        # Triangle coordinates
        x1 = self.p1.x()
        y1 = self.p1.y()
        z1 = self.p1.getZ()
        self.qPolygon.append(QPointF(x1, y1))

        x2 = self.p2.x()
        y2 = self.p2.y()
        z2 = self.p2.getZ()
        self.qPolygon.append(QPointF(x2, y2))

        x3 = self.p3.x()
        y3 = self.p3.y()
        z3 = self.p3.getZ()
        self.qPolygon.append(QPointF(x3, y3))

        # Plane vectors
        u = [x2 - x1, y2 - y1, z2 - z1]
        v = [x3 - x1, y3 - y1, z3 - z1]

        # Cross product
        n = cross(u, v)

        return n

    def setColor(self, col):
        self.col = col

    def getColor(self):
        return self.col

    def getQPolygon(self):
        return self.qPolygon
