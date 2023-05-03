import tkinter as tk
from gui.gui_main import TargetDetectionGUI

def main():
    root = tk.Tk()
    root.title("Target Detection")
    root.geometry("800x600")
    root.resizable(False, False)

    app = TargetDetectionGUI(root)
    app.grid(row=0, column=0, sticky="nsew")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()
