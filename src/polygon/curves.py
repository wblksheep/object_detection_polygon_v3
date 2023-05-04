import numpy as np
from scipy.interpolate import splprep, splev
import cv2


class BSpline:
    def __init__(self, point1, point2, smoothness=0.5, num_points=100):
        self.point1 = point1
        self.point2 = point2
        self.smoothness = smoothness
        self.num_points = num_points
        self.curve_points = self.fit_bspline()

    def fit_bspline(self):
        # 计算中间控制点
        middle_point = [(self.point1[0] + self.point2[0]) / 2, (self.point1[1] + self.point2[1]) / 2]
        points = np.array(
            [self.point1, middle_point, self.point2])
        points = np.array([self.point1, middle_point, self.point2])
        tck, u = splprep(points.T, u=None, s=self.smoothness, k=2, per=0)
        u_new = np.linspace(u.min(), u.max(), self.num_points)
        x_new, y_new = splev(u_new, tck, der=0)
        return np.column_stack((x_new, y_new))

    def get_curve_points(self):
        return self.curve_points

    def draw_curve(self, image, color=(0, 255, 0), thickness=2):
        curve = self.curve_points.astype(np.int32)
        for i in range(len(curve) - 1):
            x1, y1 = curve[i]
            x2, y2 = curve[i + 1]
            cv2.line(image, (x1, y1), (x2, y2), color, thickness)
        return image
