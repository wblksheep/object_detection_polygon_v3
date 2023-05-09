import numpy as np
from tkinter import *

# 定义四边形顶点
points = np.array([[0, 0], [200, 400], [600, 400], [400, 100]], dtype=np.int32)

# 创建Tkinter窗口
window = Tk()
window.title("Polygon Mask")

# 设置画布大小
width, height = 1000, 1000

# 在Tkinter Canvas上显示图像
canvas = Canvas(window, width=width, height=height)
canvas.pack()

# 使用create_polygon绘制多边形
canvas.create_polygon(*points.flatten(), fill='gray')

window.mainloop()
