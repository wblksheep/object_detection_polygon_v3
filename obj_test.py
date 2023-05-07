import tkinter as tk


class RectangleModel:
    def __init__(self):
        self.observers = []
        self.rectangles = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.rectangles)

    def add_rectangle(self, rectangle):
        self.rectangles.append(rectangle)
        self.notify_observers()


class RectangleView(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

    def update(self, rectangles):
        self.delete("all")
        for rectangle in rectangles:
            self.create_rectangle(*rectangle, outline="black", width=2)


class RectangleController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.register_observer(self.view)

    def add_rectangle(self, rectangle):
        self.model.add_rectangle(rectangle)


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("矩形绘制")

        self.model = RectangleModel()
        self.view = RectangleView(self, width=600, height=400, bg="white")
        self.view.pack(padx=10, pady=10)

        self.controller = RectangleController(self.model, self.view)

        self.view.bind("<Button-1>", self.on_button_press)
        self.view.bind("<B1-Motion>", self.on_move_press)
        self.view.bind("<ButtonRelease-1>", self.on_button_release)

        self.start_point = None
        self.current_rectangle = None

    def on_button_press(self, event):
        self.start_point = (event.x, event.y)

    def on_move_press(self, event):
        if self.start_point:
            if self.current_rectangle:
                self.view.delete(self.current_rectangle)
            self.current_rectangle = self.view.create_rectangle(self.start_point[0], self.start_point[1], event.x, event.y, outline="black", width=2)

    def on_button_release(self, event):
        if self.start_point:
            rectangle = (self.start_point[0], self.start_point[1], event.x, event.y)
            self.controller.add_rectangle(rectangle)
            self.start_point = None
            self.current_rectangle = None


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
