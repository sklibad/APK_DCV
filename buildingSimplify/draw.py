from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import shapefile


class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Building polygon
        self.polygons = []

        # Enclosing rectangle
        self.er = []

        # List of coordinate lists
        self.coordinates = []

        # Map extent
        self.extent = []

        # Widget extent
        self.canvas_extent = [770, 577 - 5]

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
        max_x = float("inf") * (-1)
        max_y = float("inf") * (-1)

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
        range_x = abs(self.extent[0] - self.extent[2])
        range_y = abs(self.extent[1] - self.extent[3])
        x_ratio = self.canvas_extent[0] / range_x
        y_ratio = self.canvas_extent[1] / range_y

        # Maintaining aspect ratio
        if x_ratio < y_ratio:
            self.canvas_extent[1] = x_ratio * range_y
        else:
            self.canvas_extent[0] = y_ratio * range_x

        # For each polygon
        for i in range(len(self.coordinates)):
            polygon = QPolygonF()
            # For each coordinate tuple
            for j in range(len(self.coordinates[i])):
                # Change coordinates to positive values
                new_x = self.coordinates[i][j][0] - self.extent[0]
                new_y = self.coordinates[i][j][1] - self.extent[1]

                # Resize coordinates to pixels fitting into widget extent
                x = new_x / (self.extent[2] - self.extent[0]) * self.canvas_extent[0] // 1
                y = self.canvas_extent[1] - new_y / (self.extent[3] - self.extent[1]) * self.canvas_extent[1] // 1 + 5

                p = QPointF(x, y)
                polygon.append(p)
            self.polygons.append(polygon)

    def getPolygons(self):
        return self.polygons

    def delPolygons(self):
        self.polygons = []

    def setEnclosingRectangles(self, er: list):
        self.er = er

    def delEnclosingRectangles(self):
        self.er = []

    """
    def mousePressEvent(self, e:QMouseEvent):
        # Get cursor position
        x = int(e.position().x())
        y = int(e.position().y())

        # Create new point
        p = QPoint(x, y)
        # Add to polygon
        self.pol.append(p)
        # Repaint screen
        self.repaint()
    """

    def paintEvent(self, e: QPaintEvent):
        # Create new object
        qp = QPainter(self)

        # Start draw
        qp.begin(self)

        # Set pen and brush - polygon
        qp.setPen(Qt.GlobalColor.black)

        # Draw polygons
        for pol in self.polygons:
            qp.drawPolygon(pol)

        # Set pen and brush - enclosing rectangle
        qp.setPen(Qt.GlobalColor.magenta)

        # Draw building
        for er in self.er:
            qp.drawPolygon(er)

        # End draw
        qp.end()