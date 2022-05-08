from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from math import *
from qpoint3D import *
from edge import *
from typing import List
from numpy import *
from triangle import *


class Algorithms:
    def __init__(self):
        pass

    def getPointAndLinePosition(self, a:QPoint3D, p1:QPoint3D, p2:QPoint3D):
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

    def get2LinesAngle(self, p1: QPoint3D, p2: QPoint3D, p3: QPoint3D, p4: QPoint3D):
        # Get angle between 2 vectors
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()

        # Dot product
        uv = ux * vx + uy * vy

        # Norms
        nu = (ux ** 2 + uy ** 2) ** 0.5
        nv = (vx ** 2 + vy ** 2) ** 0.5

        # Angle
        try:
            return abs(acos(uv / (nu * nv)))
        except:
            return 0

    def getCircleCenterAndRadius(self, p1: QPoint3D, p2: QPoint3D, p3: QPoint3D):
        # Calculate center and radius of circle defined by three points

        #Coefficients k1-k12
        k1 = p1.x()**2 + p1.y()**2
        k2 = p2.x()**2 + p2.y()**2
        k3 = p3.x() ** 2 + p3.y() ** 2
        k4 = p1.y() - p2.y()
        k5 = p1.y() - p3.y()
        k6 = p2.y() - p3.y()
        k7 = p1.x() - p2.x()
        k8 = p1.x() - p3.x()
        k9 = p2.x() - p3.x()
        k10 = p1.x()**2
        k11 = p2.x()**2
        k12 = p3.x()**2

        # Compute m
        m_nom = k12*(-k4) + k11*k5 - (k10 + k4*k5)*k6
        m_den = p3.x()*(-k4) + p2.x()*k5 + p1.x()*(-k6)
        m = 0.5*(m_nom/m_den)

        # Compute n
        n_nom = k1*(-k9) + k2*k8 + k3*(-k7)
        n_den = p1.y()*(-k9) + p2.y()*k8 + p3.y()*(-k7)
        n = 0.5*(n_nom/n_den)

        #Create inscribed circle center
        c = QPoint3D(m, n)

        # Compute radius
        r = ((p1.x() - m)**2 + (p1.y() - n)**2)**0.5

        return c, r

    def getNearestPointIdx(self, p: QPoint3D, points: List[QPoint3D]):
        # Get index of nearest point
        idx_min = -1
        d_min = inf

        #Browse all points
        for i in range(len(points)):
            #Skip identical point
            if p == points[i]:
                continue

            # Distance between p and points
            dx = p.x() - points[i].x()
            dy = p.y() - points[i].y()
            d = (dx*dx+dy*dy)**0.5

            # Update d_min
            if d < d_min:
                d_min = d
                idx_min = i

        return idx_min

    def getDelaunayPointIdx(self, e: Edge, points: List[QPoint3D]):
        # Finding optimal Delaunay point to the edge
        idx_min = -1
        r_min = inf

        # Get edge end points
        p1 = e.getStart()
        p2 = e.getEnd()

        # Browse all points
        for i in range(len(points)):
            #Skip identical point
            if p1 == points[i] or p2 == points[i]:
                continue

            # Point in left halfplane
            if self.getPointAndLinePosition(points[i], p1, p2) == 1:

                #Center and radius of the inscribed circle
                c, r = self.getCircleCenterAndRadius(points[i], p1, p2)

                #Center in right halfplane
                if self.getPointAndLinePosition(c, p1, p2) == 0:
                    r = -r

                # Update minimum
                if r < r_min:
                    r_min = r
                    idx_min = i

        return idx_min


    def DT(self, points : List[QPoint3D]):
        # Create Delaunay triangulation using incremental method
        dt: List[Edge] = []
        ael: List[Edge] = []

        # Find pivot (minimum x)
        q = min(points, key=lambda k: k.x())

        # Point nearest to pivot q
        i_nearest = self.getNearestPointIdx(q, points);
        qn = points[i_nearest];

        # Create new edge
        e1 = Edge(q, qn);

        # Find optimal Delaunay point
        i_point = self.getDelaunayPointIdx(e1, points);

        #Point has not been found, change orientation, search again
        if i_point == -1:
            e1 = e1.switch()
            i_point = self.getDelaunayPointIdx(e1, points)

        #Delaunay point + 3 rd vertex
        v3 = points[i_point]

        # Create remaining edges of the first triangle
        e2 = Edge(e1.getEnd(), v3)
        e3 = Edge(v3, e1.getStart())

        # Add 3 edges to DT
        dt.append(e1);
        dt.append(e2);
        dt.append(e3);

        # Add 3 edges to AEL
        ael.append(e1);
        ael.append(e2);
        ael.append(e3);

        # Proces edges until AEL is empty
        while ael:
            #Get last edge
            e1 = ael.pop();

            #Change orientation
            e1 = e1.switch();

            #Find optimal Delaunay point
            i_point = self.getDelaunayPointIdx(e1, points);

            # Point has been found
            if i_point != -1:
                v3 = points[i_point]

                # Create remaining edges of the second triangle
                e2 = Edge(e1.getEnd(), v3)
                e3 = Edge(v3, e1.getStart())

                # Add 3 edges to DT
                dt.append(e1);
                dt.append(e2);
                dt.append(e3);

                # Update AEL
                self.updateAEL(e2, ael)
                self.updateAEL(e3, ael)

        return dt

    def updateAEL(self, e: Edge, ael: List[Edge]):
        # Update AEL
        e = e.switch()

        #Look for e in AEL
        if e in ael:
            #Edge e has been found, remove from the list
            ael.remove(e)

        else:
            #Edge e has not been found, add to the list
            e = e.switch()
            ael.append(e)

    def getCLpoint(self, p1: QPoint3D, p2: QPoint3D, z: float):
        # Returns point on contour line

        # Get B coordinates
        x_b = (p2.x()-p1.x())/(p2.getZ() - p1.getZ())*(z - p1.getZ()) + p1.x()
        y_b = (p2.y() - p1.y()) / (p2.getZ() - p1.getZ()) * (z - p1.getZ()) + p1.y()

        return QPoint3D(x_b, y_b, z)


    def createCL(self, dt: List[Edge], zmin: float, zmax: float, dz: float) -> List[Edge]:
        # Generate contour lines in interval zmin - zmax
        cl: List[Edge] = []

        # Browse list of edge by triangles
        for i in range(0, len(dt), 3):
            # Triangle vertices
            p1 = dt[i].getStart()
            p2 = dt[i+1].getStart()
            p3 = dt[i+2].getStart()

            # Get point heights
            z1 = p1.getZ()
            z2 = p2.getZ()
            z3 = p3.getZ()

            # Create horizontal planes inside intervals
            for z in arange(zmin, zmax, dz):
                # Height differencies
                dz1 = z1 - z
                dz2 = z2 - z
                dz3 = z3 - z

                # Intersected edges
                t12 = dz1*dz2
                t23 = dz2*dz3
                t31 = dz3*dz1

                # Triangle is planar
                if dz1 == 0 and dz2 == 0 and dz3 == 0:
                    continue

                # Edge p1, p2 is collinear
                elif dz1 == 0 and dz2 == 0:
                    cl.append(dt[i])

                # Edge p2, p3 is collinear
                elif dz2 == 0 and dz3 == 0:
                    cl.append(dt[i+1])

                # Edge p3, p2 is collinear
                elif dz3 == 0 and dz1 == 0:
                    cl.append(dt[i+2])

                # Intersected edges 1, 2 and 2, 3
                elif (t12 <= 0 and t23 < 0) or (t12 < 0 and t23 <= 0):
                    A = self.getCLpoint(p1, p2, z)
                    B = self.getCLpoint(p2, p3, z)

                    # Create edge
                    e = Edge(A, B)

                    # Add edge to list
                    cl.append(e)

                # Intersected edges 2, 3 and 3, 1
                elif (t23 <= 0 and t31 < 0) or (t23 < 0 and t31 <= 0):
                    B = self.getCLpoint(p2, p3, z)
                    C = self.getCLpoint(p3, p1, z)

                    # Create edge
                    e = Edge(B, C)

                    # Add edge to list
                    cl.append(e)

                # Intersected edges 3, 1 and 1, 2
                elif (t12 <= 0 and t31 < 0) or (t12 < 0 and t31 <= 0):
                    C = self.getCLpoint(p3, p1, z)
                    A = self.getCLpoint(p1, p2, z)

                    # Create edge
                    e = Edge(C, A)

                    # Add edge to list
                    cl.append(e)

        return cl

    def computeSlope(self, dt: List[Edge]):
        # Calculates slope of each triangle of delaunay triangulation

        triangles: List[Triangle] = []
        shades: List[int] = []

        # Browse list of edge by triangles
        for i in range(0, len(dt), 3):
            t = Triangle(dt[i], dt[i + 1], dt[i + 2])
            n = t.getNormalVector()

            # Angle in degrees between plane of triangle and horizontal plane
            slope = acos(n[2] / sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2))*180/pi
            slope = 255 - slope/90*255
            shades.append(slope)

            # Get triangle as QPolygonF object
            t_2D = t.getQPolygonF()
            triangles.append(t_2D)

        return triangles, shades

    def computeAscpect(self, dt: List[Edge]):
        # Calculates aspect of each triangle of delaunay triangulation

        triangles: List[Triangle] = []
        colors: List[QColor] = []

        # Browse list of edge by triangles
        for i in range(0, len(dt), 3):
            t = Triangle(dt[i], dt[i + 1], dt[i + 2])
            n = t.getNormalVector()

            # Partial derivatives
            fx = n[0]
            fy = n[1]

            # Get triangle as QPolygonF object
            t_2D = t.getQPolygonF()
            triangles.append(t_2D)

            # Azimuth in degrees
            try:
                A = atan(fy/fx)*180/pi
            # If surface is flat
            except:
                colors.append(QColor(128, 128, 128))
                continue

            # Quadrant correction
            if fx > 0:
                A = 90 - A
            elif fx < 0:
                A = 270 - A

            # Aspect visualization by cardinal direction
            if 25 < A <= 65:
                colors.append(QColor(255, 165, 0))
            elif 65 < A <= 105:
                colors.append(QColor(255, 255, 0))
            elif 105 < A <= 145:
                colors.append(QColor(0, 128, 0))
            elif 145 < A <= 185:
                colors.append(QColor(0, 191, 255))
            elif 185 < A <= 225:
                colors.append(QColor(0, 0, 255))
            elif 225 < A <= 265:
                colors.append(QColor(0, 0, 139))
            elif 265 < A <= 305:
                colors.append(QColor(128, 0, 128))
            elif 305 < A <= 345:
                colors.append(QColor(138, 43, 226))
            else:
                colors.append(QColor(255, 0, 0))

        return triangles, colors


