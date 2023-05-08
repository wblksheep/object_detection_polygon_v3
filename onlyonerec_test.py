import tkinter as tk

class RectangleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Single Rectangle")

        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack()

        self.rectangle = None
        self.canvas.bind("<Button-1>", self.draw_rectangle)

    def draw_rectangle(self, event):
        if self.rectangle is not None:
            self.canvas.delete(self.rectangle)

        x1, y1 = event.x - 50, event.y - 50
        x2, y2 = event.x + 50, event.y + 50
        self.rectangle = self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")

if __name__ == "__main__":
    app = RectangleApp()
    app.mainloop()
