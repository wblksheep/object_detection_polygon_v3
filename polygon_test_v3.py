import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

# 定义四边形顶点
points = np.array([[0, 0], [200, 400], [600, 400], [400, 100]], dtype=np.int32)

# 创建一个空白图像
height, width = 1000, 1000
image = np.zeros((height, width), dtype=np.uint8)

# 将四边形顶点转换为适合OpenCV的格式
pts = points.reshape((-1, 1, 2))


# 使用fillPoly绘制多边形并生成掩模
cv2.fillPoly(image, [pts], 255)

# 创建Tkinter窗口
window = Tk()
window.title("Polygon Mask")

# 将OpenCV图像转换为PIL图像，然后转换为Tkinter PhotoImage
image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
image = Image.fromarray(image)
image = ImageTk.PhotoImage(image)

# 在Tkinter Canvas上显示图像
canvas = Canvas(window, width=width, height=height)
canvas.pack()
canvas.create_image(0, 0, anchor=NW, image=image)

window.mainloop()
