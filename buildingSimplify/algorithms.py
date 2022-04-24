from PyQt6.QtCore import *
from PyQt6.QtGui import *
from math import *

class Algorithms:
    def __init__(self):
        pass

    def get2LinesAngle(self, p1: QPoint, p2: QPoint, p3: QPoint, p4: QPoint):
        # Get angle between 2 vectors
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()

        # Cross product
        uv = ux * vx + uy * vy

        # Norms
        nu = (ux ** 2 + uy ** 2) ** 0.5
        nv = (vx ** 2 + vy ** 2) ** 0.5

        # Angle
        try:
            return abs(acos(uv / (nu * nv)))
        except:
            return 0

    def calculateGain(self, p1: QPoint, p2: QPoint):
        x_diff = p1.x() - p2.x()
        y_diff = p1.y() - p2.y()
        gain = atan2(y_diff, x_diff)

        return gain

    def createCH(self, pol:QPolygon):
        ch = QPolygonF()

        #Find pivot
        q = min(pol, key=lambda k: k.y())

        # Initialise Pj, Pj1
        pj = q
        pj1 = QPointF(q.x() - 10, q.y())

        # Appending pivot to convex hull
        ch.append(q)

        # Jarvis scan
        first_pass = True

        while pj != q or first_pass:
            first_pass = False

            # Find point maximizing omega
            omega_max = 0
            index_max = -1

            for index in range(len(pol)):
                # Compute omega angle
                omega = self.get2LinesAngle(pj, pj1, pj, pol[index])

                # Updating maximum
                if omega > omega_max:
                    omega_max = omega
                    index_max = index

            # Add vertex to convex hull
            ch.append(pol[index_max])

            # Update last two points of ch
            pj1 = pj
            pj = pol[index_max]

        return ch

    def rotate(self, pol: QPolygon, angle: float):
        # Rotate polygon vertices by angle
        pol_rot = QPolygon()

        # Browse points one by one
        for i in range(len(pol)):
            # Apply rotation matrix
            xr = pol[i].x() * cos(angle) - sin(angle) * pol[i].y()
            yr = pol[i].x() * sin(angle) + cos(angle) * pol[i].y()

            # Add point to rotated polygon
            point = QPoint(int(xr), int(yr))
            pol_rot.append(point)

        return pol_rot

    def minMaxBox(self, pol: QPolygon):
        # Creating minmax box and calculating area
        # Finding extreme coordinates
        x_min = min(pol, key=lambda k: k.x()).x()
        x_max = max(pol, key=lambda k: k.x()).x()
        y_min = min(pol, key=lambda k: k.y()).y()
        y_max = max(pol, key=lambda k: k.y()).y()

        # Create vertices of bounding box
        v1 = QPointF(x_min, y_min)
        v2 = QPointF(x_max, y_min)
        v3 = QPointF(x_max, y_max)
        v4 = QPointF(x_min, y_max)

        # Area of rectangle
        a = x_max - x_min
        b = y_max - y_min
        S = a * b

        # Create QPolygon
        minmax_box = QPolygonF([v1, v2, v3, v4])

        return S, minmax_box

    def minAreaEnclosingRectangle(self, pol: QPolygon):
        # Create approximation of building using minimum area enclosing rectangle
        ch = self.createCH(pol)
        n_ch = len(ch)

        # Create initial approximation
        sigma_min = 0
        S_min, mmb_min = self.minMaxBox(ch)

        # Process all segment of convex hull
        for i in range(n_ch):

            # Direction of segment
            sigma_i = self.get2LinesAngle(ch[i], ch[(i+1) % n_ch], QPoint(0, 0), QPoint(1, 0))

            # Rotate by -sigma_i
            ch_rot = self.rotate(ch, -sigma_i)

            # Create MMB
            S_i, mmb_i = self.minMaxBox(ch_rot)

            # Updating minimum
            if S_i < S_min:
                S_min = S_i
                sigma_min = sigma_i
                mmb_min = mmb_i

        # Rotate mmb_min back by sigma_min
        er = self.rotate(mmb_min, sigma_min)

        # Resize mmb_res, S_mmb = s_building
        er_new = self.resizeRectangle(er, pol)

        return er_new

    def getArea(self, pol:QPolygon):
        # Compute area of nonconvex polygon using LH formula
        n = len(pol)
        S = 0

        for i in range(n):
            dS = pol[i].x()*(pol[(i+1) % n].y() - pol[(i-1+n) % n].y())
            S += dS

        return abs(S)/2

    def resizeRectangle(self, er: QPolygon, pol: QPolygon):
        # Modify enclosing rectangle to shape of the same area as building

        # Calculate area of both polygons
        er_S = self.getArea(er)
        pol_S = self.getArea(pol)

        # Calculate fraction of areas
        k = pol_S/er_S

        # Calculate center of gravity
        xc = (er[0].x() + er[1].x() + er[2].x() + er[3].x())/4
        yc = (er[0].y() + er[1].y() + er[2].y() + er[3].y())/4

        # Calculate directions
        u1x = er[0].x() - xc
        u1y = er[0].y() - yc

        u2x = er[1].x() - xc
        u2y = er[1].y() - yc

        u3x = er[2].x() - xc
        u3y = er[2].y() - yc

        u4x = er[3].x() - xc
        u4y = er[3].y() - yc

        # Modify points of enclosing rectangle
        v1x = xc + sqrt(k)*u1x
        v1y = yc + sqrt(k)*u1y

        v2x = xc + sqrt(k)*u2x
        v2y = yc + sqrt(k)*u2y

        v3x = xc + sqrt(k)*u3x
        v3y = yc + sqrt(k)*u3y

        v4x = xc + sqrt(k)*u4x
        v4y = yc + sqrt(k)*u4y

        # Create QPoint objects
        v1 = QPoint(int(v1x), int(v1y))
        v2 = QPoint(int(v2x), int(v2y))
        v3 = QPoint(int(v3x), int(v3y))
        v4 = QPoint(int(v4x), int(v4y))

        # Create QPolygon object
        er_new = QPolygon([v1, v2, v3, v4])

        return er_new

    def reduceGains(self, pol: QPolygon):
        # Returns list of edge gains reduced by value of gain of first edge
        nom_sum = 0
        den_sum = 0
        sigma_dif = self.calculateGain(pol[0], pol[1])
        for i in range(len(pol)):
            if pol[i].x() == pol[(i+1) % len(pol)].x() and pol[i].y() == pol[(i+1) % len(pol)].y():
                continue

            # Calculate edge length
            s_i = sqrt((pol[i].x() - (pol[(i+1) % len(pol)]).x())**2 + (pol[i].y() - (pol[(i+1) % len(pol)]).y())**2)

            # Direction of segment
            sigma_i = self.calculateGain(pol[i], pol[(i+1) % len(pol)])

            # Sigma value reduced by gain of first edge
            sigma_reduced = sigma_i - sigma_dif

            # Divide sigma_reduced by pi/2
            k_i = round(2*sigma_reduced/pi, 0)

            # Do sigma_reduced modulo by pi/2
            r_i = sigma_reduced - k_i*pi/2

            # Calculate main building direction
            nom_sum += r_i*s_i
            den_sum += s_i
            main_dir = sigma_dif + nom_sum/den_sum

        return main_dir


    def wallAverage(self, pol: QPolygon, main_dir: float):
        # Simplifies polygon using method Wall average
        pol_rot = self.rotate(pol, -main_dir)
        mmb = self.minMaxBox(pol_rot)[1]
        mmb_rot = self.rotate(mmb, main_dir)
        mmb_res = self.resizeRectangle(mmb_rot, pol)

        return mmb_res

    def longestEdge(self, pol: QPolygon):
        # Simplifies polygon using method Longest edge

        # Inicialize maximum length of polygon edge and its gain
        length_max = 0
        angle = 0

        for i in range(len(pol)):
            x1 = pol[i].x()
            y1 = pol[i].y()
            x2 = pol[(i + 1) % len(pol)].x()
            y2 = pol[(i + 1) % len(pol)].y()

            # Calculate edge length
            length = sqrt((x1 - x2)**2 + (y1 - y2)**2)

            # If length higher than current max length
            if length > length_max:
                length_max = length
                angle = self.calculateGain(pol[i], pol[(i + 1) % len(pol)])

        pol_rot = self.rotate(pol, -angle)
        mmb = self.minMaxBox(pol_rot)[1]
        mmb_rot = self.rotate(mmb, angle)
        mmb_res = self.resizeRectangle(mmb_rot, pol)

        return mmb_res





