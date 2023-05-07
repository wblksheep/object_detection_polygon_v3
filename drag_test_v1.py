import tkinter as tk
from scipy.interpolate import BSpline, interp1d
import numpy as np


class ExampleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.curve = None
        self.points = [(100, 100), (200, 300), (300, 100)]
        self.control_points = []

        for x, y in self.points:
            point = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='white', outline='black')
            self.control_points.append(point)

        self.update_curve()

    def on_button_press(self, event):
        for i, point in enumerate(self.control_points):
            x1, y1, x2, y2 = self.canvas.coords(point)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.dragging_point = i
                return

    def on_move_press(self, event):
        if hasattr(self, 'dragging_point'):
            x, y = event.x, event.y
            self.canvas.coords(self.control_points[self.dragging_point], x-5, y-5, x+5, y+5)
            self.points[self.dragging_point] = (x, y)
            self.update_curve()

    def on_button_release(self, event):
        self.dragging_point = None

    def update_curve(self):
        if self.curve:
            self.canvas.delete(self.curve)

        x = [p[0] for p in self.points]
        y = [p[1] for p in self.points]

        # 计算B样条曲线上的点
        tck = interpolate.splrep(x, y, k=3)
        x_bspline = np.linspace(x[0], x[-1], 1000)
        y_bspline = interpolate.splev(x_bspline, tck)

        # 用计算得到的点绘制曲线
        interp_func = interp1d(x_bspline, y_bspline)
        points = [(x_bspline[i], interp_func(x_bspline[i])) for i in range(len(x_bspline))]
        coords = [p for point in points for p in point]
        self.curve = self.canvas.create_line(*coords, fill='blue', smooth=True)


if __name__ == '__main__':
    app = ExampleApp()
    app.mainloop()