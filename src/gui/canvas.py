import tkinter as tk
from PIL import ImageTk, Image
from tkinter import Canvas
# 在DetectionCanvas类中，我们定义了画布，能够绘制多边形、更新多边形、绘制检测结果和清除检测结果，以及在画布上显示图像。
class DetectionCanvas(Canvas):
    def __init__(self, master, width=800, height=600, **kwargs):
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

    def draw_detections(self, detections, polygon):
        self.delete("all")
        for det in detections:
            x1, y1, x2, y2, conf, cls = det
            self.create_rectangle(x1, y1, x2, y2, outline="red")
            self.create_text(x1, y1, text=f"{cls}: {conf:.2f}", anchor=tk.NW, fill="red")
        self.draw_polygon(polygon)

    def draw_polygon(self, polygon):
        if len(polygon.points) >= 2:
            for i in range(len(polygon.points) - 1):
                self.create_line(polygon.points[i], polygon.points[i + 1], fill="blue")
            if len(polygon.points) == 4:
                self.create_line(polygon.points[-1], polygon.points[0], fill="blue")