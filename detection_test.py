import tkinter as tk
import cv2
import os
from PIL import Image, ImageTk


class CustomCanvas(tk.Canvas):
    def __init__(self, yolo, polygon, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.yolo = yolo
        self.polygon = polygon
        self.capture_image_id = None
        self.canvas_image = None

        self.capture_button = tk.Button(self, text="Capture", command=self.toggle_capture)
        self.capture_button.pack(side=tk.BOTTOM)

        self.capturing = False

    def toggle_capture(self):
        self.capturing = not self.capturing
        if self.capturing:
            self.capture_button.config(text="Stop")
            self.after(1, self.display_image_on_canvas)
        else:
            self.capture_button.config(text="Capture")

    def display_image_on_canvas(self):
        if not self.capturing:
            return

        frame = self.yolo.capture_image()
        self.canvas_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))

        if self.capture_image_id is None:
            self.capture_image_id = self.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)
        else:
            self.itemconfig(self.capture_image_id, image=self.canvas_image)

        self.update_detection_results(frame)
        self.after(1, self.display_image_on_canvas)

    def update_detection_results(self, frame):

        detections = self.yolo.detect(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.canvas_image = ImageTk.PhotoImage(Image.fromarray(frame))
        self.itemconfig(self.capture_image_id, image=self.canvas_image)

        for detection in detections:
            self.canvas.draw_detections(detection, self.polygon)

        self.canvas.update_pre_detections()
        self.polygon.update_polygon()
