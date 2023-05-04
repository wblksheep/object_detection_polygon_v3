import os
import sys
from PIL import Image, ImageTk

import json
import cv2
import torch
from pathlib import Path

# Import YOLOv5
from src.detection.yolo_v5 import YOLOv5
from src.polygon.polygon import Polygon
sys.path.append(os.path.dirname(__file__))
import tkinter as tk
from tkinter import ttk, filedialog
from canvas import DetectionCanvas

class TargetDetectionGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.yolo=YOLOv5() #Initialize YOLOv5 object
        self.polygon = Polygon() #Initialize Polygon object
        self.create_widgets()

    def create_widgets(self):
        self.canvas = DetectionCanvas(self.master)
        self.canvas.grid(row=0, column=0, rowspan=4)
        self.canvas.bind("<Button-1>", self.click_on_canvas)

        self.capture_button = ttk.Button(self.master, text="Capture", command=self.display_image_on_canvas)
        self.capture_button.grid(row=0, column=1)

        self.slider = tk.Scale(self.master, from_=0, to=1, orient=tk.HORIZONTAL)
        self.slider.grid(row=1, column=1)

        self.mode_combobox = ttk.Combobox(self.master, values=["High Performance", "Balanced", "Energy Saving"])
        self.mode_combobox.grid(row=2, column=1)

        self.save_button = ttk.Button(self.master, text="Save Results", command=self.save_detection_results)
        self.save_button.grid(row=3, column=1)

        self.load_button = ttk.Button(self.master, text="Load Polygon", command=self.load_preset_polygon)
        self.load_button.grid(row=4, column=1)

    def click_on_canvas(self, event):
        point = (event.x, event.y)
        self.polygon.add_point(point)
        self.canvas.draw_point(point)

        if len(self.polygon.points) == 4:
            curves = self.polygon.add_curves()
            for curve in curves:
                self.canvas.draw_curve(curve)

    def display_image_on_canvas(self):
        # Capture image from the camera and display it on the canvas
        import cv2
        from src.config import load_config
        _, RESOURCES_PATH = load_config()
        # 构建图像文件的绝对路径
        image_path = os.path.join(RESOURCES_PATH, "img.png")
        frame = self.yolo.capture_image() if self.yolo.capture_image() is not None else cv2.imread(image_path)
        self.canvas_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)
        self.update_detection_results()

    def update_detection_results(self):
        # Update detection results on the canvas
        import cv2
        from src.config import load_config
        _, RESOURCES_PATH = load_config()
        # 构建图像文件的绝对路径
        image_path = os.path.join(RESOURCES_PATH, "img.png")
        frame = self.yolo.capture_image() if self.yolo.capture_image() is not None else cv2.imread(image_path)
        # Perform object detection using provided detect function
        detections=self.yolo.detect(image_path)

        # Show the image on the canvas
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.canvas_image = ImageTk.PhotoImage(Image.fromarray(frame))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)
        # Draw detections on the canvas
        for detection in detections:
            self.canvas.draw_detections(detection, self.polygon)
        # Redraw the polygon
        self.canvas.draw_polygon(self.polygon)


    def save_detection_results(self):
        # Save current detection results and polygon settings
        save_path = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json")], defaultextension="*.json")
        if save_path:
            results = {
                "detections": self.yolo.detections,
                "polygon": self.polygon.to_list()
            }
            with open(save_path, "w") as f:
                json.dump(results, f)
        pass

    def load_preset_polygon(self):
        # Load preset polygon settings
        load_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")], defaultextension="*.json")
        if load_path:
            with open(load_path, "r") as f:
                loaded_data = json.load(f)
            self.polygon = Polygon(points=loaded_data["polygon"])
            self.canvas.draw_polygon(self.polygon)
        pass
