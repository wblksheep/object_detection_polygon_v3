import cv2
import numpy as np

# 定义四边形顶点
points = np.array([[0, 0], [200, 400], [600, 400], [400, 100]], dtype=np.int32)

# 创建一个空白图像
height, width = 1000, 1000
image = np.zeros((height, width), dtype=np.uint8)

# 将四边形顶点转换为适合OpenCV的格式
pts = points.reshape((-1, 1, 2))

# 使用fillPoly绘制多边形并生成掩模
cv2.fillPoly(image, [pts], 255)

# 展示掩模图像
cv2.imshow('Mask', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
