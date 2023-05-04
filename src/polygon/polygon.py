import os

import numpy as np
import cv2
from polygon.curves import BSpline
class Polygon:
    def __init__(self, points=None):
        self.points = points if points else []
        self.curves = []

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
        return self.curves
    def to_list(self):
        return self.points
def create_polygon(points):
    """
    根据给定的点生成一个多边形。
    :param points: 一个四元组，包含四个点的坐标。
    :return: 一个包含多边形顶点坐标的numpy数组。
    """
    polygon = np.array(points, dtype=np.int32)
    return polygon

def is_point_inside_polygon(point, polygon):
    """
    检查给定点是否在多边形内。
    :param point: 需要检查的点的坐标，形式为(x, y)。
    :param polygon: 一个包含多边形顶点坐标的numpy数组。
    :return: 布尔值，如果点在多边形内则为True，否则为False。
    """
    return cv2.pointPolygonTest(polygon, point, False) >= 0

def draw_polygon(image, polygon, color=(0, 0, 255), thickness=2):
    """
    在给定图像上绘制多边形。
    :param image: 需要绘制多边形的图像。
    :param polygon: 一个包含多边形顶点坐标的numpy数组。
    :param color: 用于绘制多边形的颜色，形式为(B, G, R)。
    :param thickness: 绘制多边形的线条粗细。
    :return: 绘制了多边形的图像。
    """
    cv2.polylines(image, [polygon], isClosed=True, color=color, thickness=thickness)
    return image
