import tkinter as tk
from PIL import ImageTk, Image
from tkinter import Canvas
from matplotlib.path import Path
# 在DetectionCanvas类中，我们定义了画布，能够绘制多边形、更新多边形、绘制检测结果和清除检测结果，以及在画布上显示图像。
class DetectionCanvas(Canvas):
    def __init__(self, master, width=1920, height=1080, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.pack()

    def draw_polygon(self, polygon_points, fill_color='blue', outline_color='red'):
        self.polygon = self.canvas.create_polygon(polygon_points, fill=fill_color, outline=outline_color)

    def update_polygon(self, polygon_points):
        self.canvas.coords(self.polygon, *polygon_points)

    def draw_detection_results(self, detection_boxes, detection_classes, detection_colors):
        self.detection_rectangles = []
        for box, class_name, color in zip(detection_boxes, detection_classes, detection_colors):
            x1, y1, x2, y2 = box
            rectangle = self.canvas.create_rectangle(x1, y1, x2, y2, outline=color)
            self.detection_rectangles.append(rectangle)
            self.canvas.create_text(x1, y1, text=class_name, anchor='nw', fill=color)

    def clear_detection_results(self):
        for rect in self.detection_rectangles:
            self.canvas.delete(rect)
        self.detection_rectangles = []

    def display_image_on_canvas(self, image_path):
        image = Image.open(image_path)
        image = image.resize((640, 480), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

    def draw_detections(self, detection, polygon):
        x1, y1, x2, y2, conf, cls = detection

        # Check if the detection's center is inside the polygon
        detection_center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
        if 0 <= detection_center[0] < 1920 and 0 <= detection_center[1] < 1080:
            if polygon.is_point_inside(detection_center):
                self.create_rectangle(int(x1), int(y1), int(x2), int(y2), outline="red")
                self.create_text(int(x1), int(y1), text=f"{cls}: {conf:.2f}", anchor=tk.NW, fill="red")
        self.draw_polygon(polygon)

    def draw_polygon(self, polygon):
        if len(polygon.points) >= 2:
            for i in range(len(polygon.points) - 1):
                self.create_line(polygon.points[i], polygon.points[i + 1], fill="blue")
            if len(polygon.points) == 4:
                self.create_line(polygon.points[-1], polygon.points[0], fill="blue")

    def draw_point(self, point, color="red", radius=3):
        x, y = point
        self.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

    def draw_curve(self, curve, color="blue"):
        points = curve.get_curve_points()
        for i in range(len(points) - 1):
            self.create_line(points[i][0], points[i][1],points[i+1][0],points[i+1][1], fill=color)