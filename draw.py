from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import shapefile


class Draw(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Spatial data data structures
        self.q = QPoint()
        self.polygons = []

        # List of polygons to highlight
        self.res_pol = []

        # List of coordinate lists
        self.coordinates = []

        # Map extent
        self.extent = []

        # Widget extent
        self.canvas_extent = [916, 547]

    def insertFile(self):
        # Shapefile path
        path = QFileDialog.getOpenFileName(self)[0]

        # Read shapefile
        shapef = shapefile.Reader(path)

        # Get polygons from shapefile
        features = shapef.shapes()

        # Inicialize extreme values
        min_x = float("inf")
        min_y = float("inf")
        max_x = float("inf")*(-1)
        max_y = float("inf")*(-1)

        # For each polygon
        for f in features:

            # List of polygon coordinates
            feature_coordinates = []

            # Get polygon coordinates
            coords = f.points

            # For each coordinate tuple
            for c in coords:

                # Update extreme values
                if c[0] < min_x:
                    min_x = c[0]
                elif c[0] > max_x:
                    max_x = c[0]
                if c[1] < min_y:
                    min_y = c[1]
                elif c[1] > max_y:
                    max_y = c[1]

                # Add coordinate tuple to list
                feature_coordinates.append([c[0], c[1]])
            self.coordinates.append(feature_coordinates)

        # Update map extent
        self.extent = [min_x, min_y, max_x, max_y]

    def rescaleData(self):
        # For each polygon
        for i in range(len(self.coordinates)):
            polygon = QPolygon()
            # For each coordinate tuple
            for j in range(len(self.coordinates[i])):

                # Change coordinates to positive values
                new_x = self.coordinates[i][j][0] - self.extent[0]
                new_y = self.coordinates[i][j][1] - self.extent[1]

                # Resize coordinates to pixels fitting into widget extent
                x = round(new_x/(self.extent[2] - self.extent[0])*self.canvas_extent[0] // 1, 0)
                y = round(self.canvas_extent[1] - new_y/(self.extent[3] - self.extent[1])*self.canvas_extent[1] // 1, 0)

                p = QPoint(int(x), int(y))
                polygon.append(p)
            self.polygons.append(polygon)

    def mousePressEvent(self, e:QMouseEvent):
        # Get cursor position
        x = int(e.position().x())
        y = int(e.position().y())
        self.q.setX(x)
        self.q.setY(y)
        self.repaint()

    def paintEvent(self, e: QPaintEvent):
        # Create new object
        qp = QPainter(self)

        # Start draw
        qp.begin(self)

        # Set pen and brush - polygon
        qp.setPen(Qt.GlobalColor.blue)
        qp.setBrush(Qt.GlobalColor.gray)

        for pol in self.polygons:
            qp.drawPolygon(pol)

        for pol in self.res_pol:
            qp.setPen(Qt.GlobalColor.darkMagenta)
            qp.setBrush(Qt.GlobalColor.magenta)
            qp.drawPolygon(pol)

        qp.setPen(Qt.GlobalColor.darkRed)
        qp.setBrush(Qt.GlobalColor.red)
        r = 5
        qp.drawEllipse(self.q.x() - r, self.q.y() - r, 2 * r, 2 * r)

        qp.end()

    def getPoint(self):
        # Get q
        return self.q

    def getPolygons(self):
        # Get list of polygons
        return self.polygons

    def setResPol(self, pol: QPolygon):
        # Add polygon to list
        self.res_pol.append(pol)

    def clearResPol(self):
        # Set result polygon
        self.res_pol = []

    def delPolygons(self):
        self.polygons = [QPolygon()]

    def delPoint(self):
        self.q = QPoint()

    def delResPol(self):
        self.res_pol = [QPolygon()]