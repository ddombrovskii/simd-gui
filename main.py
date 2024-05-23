import tkinter as tk
from tkinter import ttk
import subprocess

LARGEFONT = ("Verdana", 28)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, NewFlightPage, FlightsListPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Настройка симуляции", font=LARGEFONT)

        label.grid(row=0, column=1, padx=10, pady=10)

        button1 = ttk.Button(self, text="Новый полет", command=lambda: controller.show_frame(NewFlightPage))
        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Все полеты", command=lambda: controller.show_frame(FlightsListPage))
        button2.grid(row=2, column=1, padx=10, pady=10)

        button_start = ttk.Button(self, text="start sim", command=self.start_simulator)
        button_start.grid(row=3, column=1, padx=10, pady=10)

    @staticmethod
    def start_simulator():
        subprocess.call('make px4_sitl gazebo-classic', shell=True, cwd='/home/ddombrovskii/PX4-Autopilot')


class NewFlightPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Настройка полета", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        label_home = ttk.Label(self, text="Домашняя точка: ")
        label_home.grid(row=1, column=1, padx=10, pady=10)

        entry_home = ttk.Entry(self)
        entry_home.grid(row=1, column=2, padx=10, pady=10)

        button_save = ttk.Button(self, text="Сохранить", command=lambda: controller.show_frame(FlightsListPage))
        button_save.grid(row=2, column=1, padx=10, pady=10)


class FlightsListPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 2", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Page 1", command=lambda: controller.show_frame(NewFlightPage))
        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Startpage", command=lambda: controller.show_frame(StartPage))
        button2.grid(row=2, column=1, padx=10, pady=10)


if __name__ == '__main__':
    app = Application()
    app.mainloop()
