from PyQt6.QtCore import *
from PyQt6.QtGui import *
from math import *

class Algorithms:
    def __init__(self):
        self.winding_num = False

    def getPointAndLinePosition(self, a: QPoint, p1: QPoint, p2: QPoint):
        # Analyze position point and line
        eps = 1.0e-10

        # Coordinate differences
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = a.x() - p1.x()
        vy = a.y() - p1.y()

        # Calculating determinant
        t = ux * vy - vx * uy

        # Point in left halfplane
        if t > eps:
            return 1

        # Point in right halfplane
        if t < -eps:
            return 0

        # Colinear point
        return -1

    def get2LinesAngle(self, p1: QPoint, p2: QPoint, p3: QPoint, p4: QPoint):
        # Get angle between 2 vectors
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()

        # Dot product
        uv = ux*vx + uy*vy

        # Norms
        nu = (ux**2 + uy**2)**0.5
        nv = (vx**2 + vy**2)**0.5

        # Angle
        if nu == 0 or nv == 0:
            cos_a = 1
        else:
            cos_a = uv/(nu*nv)
        if cos_a > 1:
            cos_a = 1
        elif cos_a < -1:
            cos_a = -1

        return abs(acos(cos_a))

    def getPositionPointAndPolygon(self, q: QPoint, pol: QPolygon) -> int:
        # Analyzes position of the point and polygon
        n = len(pol)
        omega_sum = 0

        # Loop through polygon nodes
        for i in range(n):

            # Analyze position of q and pi, pi+1
            pos = self.getPointAndLinePosition(q, pol[i], pol[(i + 1) % n])

            # Angle between q and pi, pi+1
            omega = self.get2LinesAngle(q, pol[i], q, pol[(i + 1) % n])

            # Computing winding number
            if pos == 1:
                # Point in the left halfplane
                omega_sum += omega
            else:
                # Try if point is colinear
                if pos == -1:
                    p_x = q.x()
                    p_y = q.y()
                    l1_x = pol[i].x()
                    l1_y = pol[i].y()
                    l2_x = pol[(i + 1) % n].x()
                    l2_y = pol[(i + 1) % n].y()
                    if (l1_x - p_x)*(l2_x - p_x) <= 0 and (l1_y - p_y)*(l2_y - p_y) <= 0:
                        # Point lies on polygon' edge
                        return -1
                # Point in the right halfplane
                omega_sum -= omega

        # Point q inside polygon
        epsilon = 1.0e-10
        if abs(abs(omega_sum)-2*pi) < epsilon:
            return 1

        # Point q outside polygon
        return 0

    def detectIntersection(self, q: QPoint, p1: QPoint, p2: QPoint):
        eps = 1.0e-4
        q_x = q.x()
        q_y = q.y()
        p1_x = p1.x()
        p1_y = p1.y()
        p2_x = p2.x()
        p2_y = p2.y()
        if p1_y < p2_y:
            min_y = p1_y
            min_x = p1_x
            max_y = p2_y
            max_x = p2_x
        else:
            min_y = p2_y
            min_x = p2_x
            max_y = p1_y
            max_x = p1_x

        if (q_y > max_y or q_y < min_y) or q_x > max(p1_x, p2_x):
            # Point Y coordinates within edge or point from edge to the right
            return 0

        if q_x < min(p1_x, p2_x):
            # Point from edge to the left
            return 1
        else:
            if abs(p1_x - p2_x) > eps:
                # Edge not parallel with y axis

                # Compute edge gain
                p_gain = (max_y - min_y)/(max_x - min_x)
            else:
                p_gain = float("inf")
            if abs(min_x - q_x) > eps:
                # Point x coordinate not identical with edge point
                q_gain = (q_y - min_y)/(q_x - min_x)
            else:
                q_gain = float("inf")

        if abs(q_gain - p_gain) < eps:
            # If point is colinear
            return -1
        elif q_gain > p_gain:
            # If point is to the left from the egde
            return 1
        return 0

    def rayCasting(self, q: QPoint, pol: QPolygon) -> int:
        n = len(pol)
        crossings = 0
        for i in range(n):
            value = self.detectIntersection(q, pol[i], pol[(i + 1) % n])
            if value == -1:
                return -1
            crossings += value
        return crossings % 2

    def isWindingNumber(self):
        # Get winding number algorithm state
        return self.winding_num

    def setSource(self):
        # Change winding number state
        self.winding_num = not(self.winding_num)
