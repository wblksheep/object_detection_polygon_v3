import os
import sys
from PIL import Image, ImageTk
import math
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
from src.polygon.PolygonController import PolygonController


class TargetDetectionGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.yolo = YOLOv5()  # Initialize YOLOv5 object
        self.curve_selected = False  # Add a boolean attribute to represent if a curve is selected
        self.selected_curve = None
        self.create_widgets()
        self.polygon_init = False
        self.polygon_controller = None

    def create_widgets(self):
        self.canvas = DetectionCanvas(self.master)
        self.canvas.grid(row=0, column=0, rowspan=4)
        self.canvas.bind("<Button-1>", self.click_on_canvas)
        self.canvas.bind("<B1-Motion>", self.on_move_press)  # Bind mouse move event
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.capture_button = ttk.Button(self.master, text="Capture", command=self.display_image_on_canvas)
        self.capture_button.grid(row=0, column=1)
        self.polygon = Polygon(self.canvas)  # Initialize Polygon object
        self.create_sliders()

        self.mode_combobox = ttk.Combobox(self.master, values=["High Performance", "Balanced", "Energy Saving"])
        self.mode_combobox.grid(row=2, column=1)

        self.save_button = ttk.Button(self.master, text="Save Results", command=self.save_detection_results)
        self.save_button.grid(row=3, column=1)

        self.load_button = ttk.Button(self.master, text="Load Polygon", command=self.load_preset_polygon)
        self.load_button.grid(row=4, column=1)

    def create_sliders(self):
        self.slider = tk.Scale(self.master, from_=0, to=1, orient=tk.HORIZONTAL, command=self.on_slider_change)
        self.slider.grid(row=1, column=1)

    def on_slider_change(self, value):
        # Update curves based on slider value
        self.polygon.update_curves(float(value))
        self.canvas.update_curves(self.polygon.curves)

    def click_on_canvas(self, event):
        if not self.polygon_init:
            point = (event.x, event.y)
            self.polygon.add_point(point)
            point_id = self.canvas.draw_point(point)
            self.polygon.add_control_point(point_id)
            if len(self.polygon.points) == 5:
                self.polygon.register_observer(self.canvas)  # Register canvas as observer of polygon
                self.polygon_controller = PolygonController(self.polygon,
                                                            self.canvas)  # Initialize PolygonController object                   self.polygon.curves[i])  # Initialize CanvasObserver object
                self.polygon_init = True
                self.polygon_controller.on_button_press(event.x, event.y)
        else:
            self.polygon_controller.on_button_press(event.x, event.y)

    def on_move_press(self, event):
        self.polygon_controller.on_move_press(event.x, event.y)

    def on_button_release(self, event):
        if hasattr(self, 'polygon_controller'):
            self.polygon_controller.on_button_release()

    def display_image_on_canvas(self):
        self.canvas.clear_detections()
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
        detections = self.yolo.detect(image_path)

        # Show the image on the canvas
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.canvas_image = ImageTk.PhotoImage(Image.fromarray(frame))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)
        # Draw detections on the canvas
        for detection in detections:
            self.canvas.draw_detections(detection, self.polygon)
        self.canvas.update_pre_detections()

        self.polygon.update_polygon()

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
