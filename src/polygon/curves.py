import numpy as np
from scipy.interpolate import splprep, splev
import cv2

def fit_bspline(points, smoothness=0.5, num_points=100):
    """
    使用B-spline曲线拟合给定的点。
    :param points: 一个包含点坐标的numpy数组，形式为(x, y)。
    :param smoothness: 平滑度参数，越大的值会产生越平滑的曲线。
    :param num_points: 生成曲线上的点的数量。
    :return: 一个包含生成的B-spline曲线上点的坐标的numpy数组。
    """
    points = np.array(points)
    tck, u = splprep(points.T, u=None, s=smoothness, per=1)
    u_new = np.linspace(u.min(), u.max(), num_points)
    x_new, y_new = splev(u_new, tck, der=0)
    return np.column_stack((x_new, y_new))

def draw_curve(image, curve, color=(0, 255, 0), thickness=2):
    """
    在给定图像上绘制曲线。
    :param image: 需要绘制曲线的图像。
    :param curve: 一个包含曲线上点的坐标的numpy数组。
    :param color: 用于绘制曲线的颜色，形式为(B, G, R)。
    :param thickness: 绘制曲线的线条粗细。
    :return: 绘制了曲线的图像。
    """
    curve = curve.astype(np.int32)
    for i in range(len(curve) - 1):
        x1, y1 = curve[i]
        x2, y2 = curve[i + 1]
        cv2.line(image, (x1, y1), (x2, y2), color, thickness)
    return image

def draw_curved_polygon(image, polygon, smoothness=0.5, num_points=100, color=(0, 0, 255), thickness=2):
    """
    在给定图像上绘制一个由B-spline曲线表示的多边形。
    :param image: 需要绘制多边形的图像。
    :param polygon: 一个包含多边形顶点坐标的numpy数组。
    :param smoothness: 平滑度参数，越大的值会产生越平滑的曲线。
    :param num_points: 生成曲线上的点的数量。
    :param color: 用于绘制曲线的颜色，形式为(B, G, R)。
    :param thickness: 绘制曲线的线条粗细。
    :return: 绘制了曲线多边形的图像。
    """
    curve = fit_bspline(polygon, smoothness, num_points)
    return draw_curve(image, curve, color, thickness)
