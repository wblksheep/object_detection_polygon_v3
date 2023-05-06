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

        def create_four_equidistant_points(p1, p2):
            t_values = np.linspace(0, 1, 4)
            #将p1和p2按[0]位置坐标升序排列
            if p1[0] > p2[0]:
                p1, p2 = p2, p1
            return [(p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])) for t in t_values]

        self.curves = [
            BSpline(create_four_equidistant_points(self.points[0], self.points[1])),
            BSpline(create_four_equidistant_points(self.points[1], self.points[2])),
            BSpline(create_four_equidistant_points(self.points[2], self.points[3])),
            BSpline(create_four_equidistant_points(self.points[3], self.points[0]))
        ]
        self.generate_mask()
        return self.curves

    def generate_mask(self):
        points = np.vstack([curve.get_curve_points() for curve in self.curves])
        hull = cv2.convexHull(points.astype(np.float32))
        cv2.fillConvexPoly(self.mask, hull.astype(np.int32), 255)

    def is_point_inside(self, point):
        return self.mask[point[1], point[0]] == 255

    def update_polygon(self, new_points):
        for i, new_point in enumerate(new_points):
            self.points[i] = new_point
        self.add_curves()

    def to_list(self):
        return self.points