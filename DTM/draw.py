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

        # Triangles for slope
        self.triangles_slope: List[QPolygonF] = []

        # Shades of grey
        self.shades: List[int] = []

        # Triangles for aspect
        self.triangles_aspect: List[QPolygonF] = []

        # Aspect colors
        self.colors: List[QColor] = []

        # Map extent
        self.extent = []

        # Widget extent
        self.canvas_extent = [1493, 701]

    def insertFile(self):
        # Shapefile path
        path = QFileDialog.getOpenFileName(self)[0]

        # Inicialize extreme values
        min_x = float("inf")
        min_y = float("inf")
        max_x = float("inf") * (-1)
        max_y = float("inf") * (-1)

        # Read textfile
        with open(path) as f:
            lines = f.readlines()
            # For each line (point) in text file
            for l in lines:
                p = l.split(" ")
                p[0] = float(p[0])
                p[1] = float(p[1])
                p[2] = float(p[2])
                q = QPoint3D(p[0], p[1], p[2])
                self.points.append(q)

                # Update extreme values
                if p[0] < min_x:
                    min_x = p[0]
                elif p[0] > max_x:
                    max_x = p[0]
                if p[1] < min_y:
                    min_y = p[1]
                elif p[1] > max_y:
                    max_y = p[1]

        # Update map extent
        self.extent = [min_x, min_y, max_x, max_y]

    def rescaleData(self):
        range_x = abs(self.extent[0] - self.extent[2])
        range_y = abs(self.extent[1] - self.extent[3])
        x_ratio = self.canvas_extent[0] / range_x
        y_ratio = self.canvas_extent[1] / range_y

        # Maintaining aspect ratio
        if x_ratio < y_ratio:
            self.canvas_extent[1] = x_ratio * range_y
        else:
            self.canvas_extent[0] = y_ratio * range_x

        # For each point
        for i in range(len(self.points)):
            # Narrow coordinate range
            new_x = self.points[i].x() - self.extent[0]
            new_y = self.points[i].y() - self.extent[1]

            # Resize coordinates to pixels fitting into widget extent
            x = (new_x / range_x * self.canvas_extent[0]) // 1
            y = (self.canvas_extent[1] - new_y / range_y * self.canvas_extent[1]) // 1
            #p = QPoint3D(x, y, self.points[i].getZ())

            # Extend range of elevation values for better results
            p = QPoint3D(x, y, self.points[i].getZ()/355*100000)
            self.points[i] = p

    def getPoints(self):
        return self.points

    def getDT(self):
        return self.dt

    def setDT(self, dt):
        self.dt = dt

    def setCL(self, cont_lines):
        self.cont_lines = cont_lines

    def setTrianglesSlope(self, t):
        self.triangles_slope = t

    def setTrianglesAspect(self, t):
        self.triangles_aspect = t

    def setShades(self, s):
        self.shades = s

    def setColors(self, c):
        self.colors = c

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

        # Draw slope
        qp.setPen(Qt.GlobalColor.gray)
        for i in range(len(self.triangles_slope)):
            qp.setBrush(QColor(self.shades[i], self.shades[i], self.shades[i]))
            qp.drawPolygon(self.triangles_slope[i])

        # Draw aspect
        qp.setPen(Qt.GlobalColor.gray)
        for i in range(len(self.triangles_aspect)):
            qp.setBrush(self.colors[i])
            qp.drawPolygon(self.triangles_aspect[i])

        # Draw contour lines
        qp.setPen(Qt.GlobalColor.black)
        for e in self.cont_lines:
            qp.drawLine(int(e.getStart().x()), int(e.getStart().y()), int(e.getEnd().x()), int(e.getEnd().y()))

        # End draw
        qp.end()
