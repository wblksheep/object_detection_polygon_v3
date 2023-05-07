import tkinter as tk
from scipy.interpolate import BSpline
from scipy import interpolate
import numpy as np


class PolygonObserver:
    def update(self, points):
        pass


class PolygonSubject:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer: PolygonObserver):
        self.observers.append(observer)

    def notify_observers(self, points):
        for observer in self.observers:
            observer.update(points)


class PolygonCanvas(tk.Canvas, PolygonObserver):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.curve = None

    def update(self, points):
        if self.curve:
            self.delete(self.curve)

        x = [p[0] for p in points]
        y = [p[1] for p in points]

        tck, u = interpolate.splprep([x, y], s=0, per=True)
        u_new = np.linspace(u.min(), u.max(), 1000)
        x_new, y_new = interpolate.splev(u_new, tck)

        coords = [coord for point in zip(x_new, y_new) for coord in point]
        self.curve = self.create_polygon(*coords, outline='blue', fill='', width=2)


class ResizablePolygon(PolygonSubject):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.points = [(100, 100), (200, 300), (300, 100), (250, 200)]

        tck, u = interpolate.splprep([[p[0] for p in self.points], [p[1] for p in self.points]], s=0, per=True)
        u_new = np.linspace(u.min(), u.max(), len(self.points))
        self.points = list(zip(*interpolate.splev(u_new, tck)))

        self.control_points = []

        for x, y in self.points:
            point = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='white', outline='black')
            self.control_points.append(point)

        self.dragging_point = None
        self.update_polygon()

    def update_polygon(self):
        self.notify_observers(self.points)


class ExampleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x1000")

        self.polygon_canvas = PolygonCanvas(self, width=400, height=400)
        self.polygon_canvas.pack()

        self.resizable_polygon = ResizablePolygon(self.polygon_canvas)
        self.resizable_polygon.register_observer(self.polygon_canvas)

        self.polygon_canvas.bind("<Button-1>", self.on_button_press)
        self.polygon_canvas.bind("<B1-Motion>", self.on_move_press)
        self.polygon_canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        for i, point in enumerate(self.resizable_polygon.control_points):
            x1, y1, x2, y2 = self.resizable_polygon.canvas.coords(point)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.resizable_polygon.dragging_point = i
                return

    def on_move_press(self, event):
        if self.resizable_polygon.dragging_point is not None:
            x, y = event.x, event.y
            self.resizable_polygon.canvas.coords(
                self.resizable_polygon.control_points[self.resizable_polygon.dragging_point],
                x - 5, y - 5, x + 5, y + 5)
            self.resizable_polygon.points[self.resizable_polygon.dragging_point] = (x, y)
            self.resizable_polygon.update_polygon()

    def on_button_release(self, event):
        self.resizable_polygon.dragging_point = None


if __name__ == '__main__':
    app = ExampleApp()
    app.mainloop()
