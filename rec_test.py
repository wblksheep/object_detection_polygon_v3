import tkinter as tk


class ExampleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.rect = None
        self.start_x = None
        self.start_y = None
        self.transparent_line = None

    def on_button_press(self, event):
        # 创建矩形
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x + 1, event.y + 1, outline='red')

        # 创建透明线
        self.transparent_line = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, width=2,
                                                        dash=(2, 2), fill='', capstyle='round')

    def on_move_press(self, event):
        # 更新矩形位置
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
            # 更新透明线终点坐标
            self.canvas.coords(self.transparent_line, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        # 删除透明线
        self.canvas.delete(self.transparent_line)


app = ExampleApp()
app.mainloop()
