import numpy as np
import cv2
from polygon.curves import BSpline

class Polygon:
    def __init__(self, points=None, img_shape=(1080,1920)):
        self.points = points if points else []
        self.curves = []
        self.img_shape = img_shape
        self.mask = np.zeros(img_shape, dtype=np.uint8)

    def add_point(self, point):
        self.points.append(point)

    def add_curves(self):
        if len(self.points) != 4:
            return None
        self.curves = [
            BSpline(self.points[0], self.points[1]),
            BSpline(self.points[1], self.points[2]),
            BSpline(self.points[2], self.points[3]),
            BSpline(self.points[3], self.points[0])
        ]
        self.generate_mask()
        return self.curves

    def generate_mask(self):
        points = np.vstack([curve.get_curve_points() for curve in self.curves])
        hull = cv2.convexHull(points.astype(np.float32))
        cv2.fillConvexPoly(self.mask, hull.astype(np.int32), 255)

    def is_point_inside(self, point):
        return self.mask[point[1], point[0]] == 255

    def to_list(self):
        return self.points