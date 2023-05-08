import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

def on_canvas_click(event):
    x, y = event.x, event.y
    point = np.array([[x, y]], dtype=np.float32)
    mapped_point = cv2.perspectiveTransform(point[None, :, :], homography_matrix)
    mapped_x, mapped_y = int(mapped_point[0, 0, 0]), int(mapped_point[0, 0, 1])
    mapped_canvas.create_oval(mapped_x-2, mapped_y-2, mapped_x+2, mapped_y+2, fill='red', outline='red')

quad_vertices = np.array([[100, 100], [200, 50], [300, 200], [150, 250]], dtype=np.float32)
rect_width, rect_height = 300, 200
rect_vertices = np.array([[0, 0], [rect_width, 0], [rect_width, rect_height], [0, rect_height]], dtype=np.float32)

homography_matrix, _ = cv2.findHomography(quad_vertices, rect_vertices)

image = np.zeros((400, 400), dtype=np.uint8)
image.fill(255)
warped_image = cv2.warpPerspective(image, homography_matrix, (rect_width, rect_height))

window = Tk()
window.title("Image Mapping")

image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
image = Image.fromarray(image)
image = ImageTk.PhotoImage(image)

warped_image = cv2.cvtColor(warped_image, cv2.COLOR_GRAY2RGB)
warped_image = Image.fromarray(warped_image)
warped_image = ImageTk.PhotoImage(warped_image)

image_canvas = Canvas(window, width=400, height=400)
image_canvas.grid(row=0, column=0)
image_canvas.create_image(0, 0, anchor=NW, image=image)
image_canvas.bind('<Button-1>', on_canvas_click)

# Draw quad_vertices on image_canvas
for i in range(4):
    image_canvas.create_line(quad_vertices[i-1][0], quad_vertices[i-1][1], quad_vertices[i][0], quad_vertices[i][1], fill='blue')

mapped_canvas = Canvas(window, width=rect_width, height=rect_height)
mapped_canvas.grid(row=0, column=1)
mapped_canvas.create_image(0, 0, anchor=NW, image=warped_image)

# Draw rect_vertices on mapped_canvas
for i in range(4):
    mapped_canvas.create_line(rect_vertices[i-1][0], rect_vertices[i-1][1], rect_vertices[i][0], rect_vertices[i][1], fill='blue')

window.mainloop()
