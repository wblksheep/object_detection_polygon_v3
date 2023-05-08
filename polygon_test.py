import numpy as np
from scipy.interpolate import splprep, splev
from tkinter import *
from PIL import Image, ImageTk
import cv2

# 定义四边形顶点
points = np.array([[0, 0], [2, 4], [6, 4], [4, 1], [0, 0]])
num_points = len(points)

# 计算周期性B-spline曲线，将k设置为1
tck, u = splprep(points.T, u=None, s=0, k=1, per=True)

# 生成新的曲线点
u_new = np.linspace(u.min(), u.max(), num_points)
x_new, y_new = splev(u_new, tck, der=0)

# 创建画布
width, height = 800, 600
canvas = np.zeros((height, width, 3), dtype=np.uint8)
canvas.fill(255)

# 画出四边形和B-spline曲线
for i in range(num_points - 1):
    canvas = cv2.line(canvas, (int(points[i, 0] * 100), int(points[i, 1] * 100)), (int(points[i+1, 0] * 100), int(points[i+1, 1] * 100)), (255, 0, 0), 2)
    canvas = cv2.line(canvas, (int(x_new[i] * 100), int(y_new[i] * 100)), (int(x_new[i+1] * 100), int(y_new[i+1] * 100)), (0, 0, 255), 2)

# 使用tkinter展示图像
window = Tk()
window.title("B-spline")

canvas_image = Image.fromarray(canvas)
canvas_image = ImageTk.PhotoImage(canvas_image)

image_canvas = Canvas(window, width=width, height=height)
image_canvas.pack()
image_canvas.create_image(0, 0, anchor=NW, image=canvas_image)

window.mainloop()
