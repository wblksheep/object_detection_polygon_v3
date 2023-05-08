import tkinter as tk
from PIL import ImageTk, Image
from tkinter import Canvas
from matplotlib.path import Path
from scipy import interpolate
import numpy as np


# 在DetectionCanvas类中，我们定义了画布，能够绘制多边形、更新多边形、绘制检测结果和清除检测结果，以及在画布上显示图像。
class DetectionCanvas(Canvas):
    def __init__(self, master, width=1920, height=1080, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.curve = None
        self.pack()
        self.cur_detection_rectangles=[]
        self.cur_detection_text=[]
        self.pre_detection_rectangles=[]
        self.pre_detection_text=[]

    def draw_polygon(self, polygon):
        if len(polygon.points) == 4:
            for curve in polygon.curves:
                self.draw_curve(curve)

    def update_polygon(self, polygon):
        if self.curve:
            self.delete(self.curve)
        polygon_points = polygon.points
        control_points = polygon.control_points
        x = [p[0] for p in polygon_points]
        y = [p[1] for p in polygon_points]

        tck, u = interpolate.splprep([x, y], per=True)
        u_new = np.linspace(u.min(), u.max(), 1000)
        x_new, y_new = interpolate.splev(u_new, tck)
        for i, point in enumerate(polygon.control_points):
            x1, y1, x2, y2 = self.coords(point)
            self.delete(point)
            point = self.create_oval(x1, y1, x2, y2, fill='white', outline='black')
            polygon.control_points[i] = point
        coords = [coord for point in zip(x_new, y_new) for coord in point]
        self.curve = self.create_polygon(*coords, outline='blue', fill='', width=2)

    # def draw_detection_results(self, detection_boxes, detection_classes, detection_colors):
    #     self.detection_rectangles = []
    #     for box, class_name, color in zip(detection_boxes, detection_classes, detection_colors):
    #         x1, y1, x2, y2 = box
    #         rectangle = self.canvas.create_rectangle(x1, y1, x2, y2, outline=color)
    #         self.detection_rectangles.append(rectangle)
    #         self.canvas.create_text(x1, y1, text=class_name, anchor='nw', fill=color)
    #
    # def clear_detection_results(self):
    #     for rect in self.detection_rectangles:
    #         self.delete(rect)
    #     self.detection_rectangles = []

    def clear_detections(self):
        for rect in self.pre_detection_rectangles:
            self.delete(rect)
        for text in self.pre_detection_text:
            self.delete(text)
    def update_pre_detections(self):
        self.pre_detection_rectangles=self.cur_detection_rectangles
        self.pre_detection_text=self.cur_detection_text
        self.cur_detection_rectangles=[]
        self.cur_detection_text=[]

    def display_image_on_canvas(self, image_path):
        image = Image.open(image_path)
        image = image.resize((640, 480), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(image)
        self.create_image(0, 0, image=self.photo, anchor='nw')

    def draw_detections(self, detection, polygon):
        x1, y1, x2, y2, conf, cls = detection

        # Check if the detection's center is inside the polygon

        detection_center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
        if 0 <= detection_center[0] < 1920 and 0 <= detection_center[1] < 1080:
            if polygon.is_point_inside(detection_center):
                rectangle = self.create_rectangle(int(x1), int(y1), int(x2), int(y2), outline="red")
                self.cur_detection_rectangles.append(rectangle)
                text = self.create_text(int(x1), int(y1), text=f"{cls}: {conf:.2f}", anchor=tk.NW, fill="red")
                self.cur_detection_text.append(text)


    def draw_polygon(self, polygon):
        if len(polygon.points) >= 2:
            for i in range(len(polygon.points) - 1):
                self.create_line(polygon.points[i], polygon.points[i + 1], fill="blue")
            if len(polygon.points) == 4:
                self.create_line(polygon.points[-1], polygon.points[0], fill="blue")

    def draw_point(self, point, color="red", radius=3):
        x, y = point
        point_id = self.create_oval(x - 5, y - 5, x + 5, y + 5, fill='white', outline='black')
        return point_id

    def draw_curve(self, curve, color="blue"):
        points = curve.get_curve_points()
        for i in range(len(points) - 1):
            self.create_line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], fill=color)

    # 补充draw_selected_curve方法，用于绘制选中的曲线
    def draw_selected_curve(self, curve, color="red"):
        points = curve.get_curve_points()
        for i in range(len(points) - 1):
            self.create_line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], fill=color)

    def update_curves(self, curves):
        for curve in curves:
            self.delete(curve)
            self.draw_curve(curve)
