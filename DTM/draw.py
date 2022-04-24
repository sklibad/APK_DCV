from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from random import *
from typing import List
from qpoint3D import *
from edge import *

class Draw (QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Input points
        self.points: List[QPoint3D] = []

        # Delaunay edges
        self.dt: List[Edge] = []

        # Contour lines
        self.cont_lines: List[Edge] = []

        # Shades of grey
        self.shades: List[int] = []

        # Triangles by slope
        self.triangles: List[QPolygonF] = []

    def getPoints(self):
        return self.points

    def getDT(self):
        return self.dt

    def setDT(self, dt):
        self.dt = dt

    def setCL(self, cont_lines):
        self.cont_lines = cont_lines

    def setTriangles(self, t):
        self.triangles = t

    def setShades(self, s):
        self.shades = s

    def mousePressEvent(self, e: QMouseEvent):
        # Get cursor position
        x = e.position().x()
        y = e.position().y()

        # Create new point
        p = QPoint3D(x, y, 500*random())

        # Add to polygon
        self.points.append(p)

        # Repaint screen
        self.repaint()

    def paintEvent(self, e: QPaintEvent):
        # Create new object
        qp = QPainter(self)

        # Start draw
        qp.begin(self)

        # Set pen and brush - building
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.white)

        # Draw points
        radius = 5
        for p in self.points:
            qp.drawEllipse(int(p.x()- radius), int(p.y()) - radius, 2 * radius, 2 * radius)

        #Draw Delaunay edges
        qp.setPen(Qt.GlobalColor.green)
        for e in self.dt:
            qp.drawLine(int(e.getStart().x()), int(e.getStart().y()), int(e.getEnd().x()), int(e.getEnd().y()))
            #qp.drawLine(QPointF(e.getStart()), QPointF(e.getEnd()))

        # Draw
        qp.setPen(Qt.GlobalColor.gray)
        for i in range(len(self.triangles)):
            qp.setBrush(QColor(self.shades[i], self.shades[i], self.shades[i]))
            qp.drawPolygon(self.triangles[i])

        # Draw contour lines
        qp.setPen(Qt.GlobalColor.black)
        for e in self.cont_lines:
            qp.drawLine(int(e.getStart().x()), int(e.getStart().y()), int(e.getEnd().x()), int(e.getEnd().y()))

        # End draw
        qp.end()