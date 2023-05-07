import tkinter as tk


class TemperatureModel:
    def __init__(self):
        self.observers = []
        self._temperature = 0

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.temperature)

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value
        self.notify_observers()


class TemperatureView(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.temperature_var = tk.StringVar()

    def update(self, temperature):
        self.temperature_var.set(f"华氏温度: {temperature * 9 / 5 + 32:.2f}°F")


class TemperatureController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.register_observer(self.view)

    def update_temperature(self, temperature):
        self.model.temperature = temperature


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("温度转换器")

        self.model = TemperatureModel()
        self.view = TemperatureView(self)
        self.view.pack(pady=10)

        self.controller = TemperatureController(self.model, self.view)

        self.celsius_label = tk.Label(self, text="摄氏温度:")
        self.celsius_label.pack()
        self.celsius_entry = tk.Entry(self)
        self.celsius_entry.pack(pady=10)

        self.convert_button = tk.Button(self, text="转换", command=self.on_convert)
        self.convert_button.pack()

        self.result_label = tk.Label(self, textvariable=self.view.temperature_var)
        self.result_label.pack(pady=10)

    def on_convert(self):
        try:
            celsius_temperature = float(self.celsius_entry.get())
            self.controller.update_temperature(celsius_temperature)
        except ValueError:
            self.view.temperature_var.set("输入无效，请输入一个数字。")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
