import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import subprocess
import requests
import json
import os
import re

BACKEND_URL = 'http://localhost:8080/api/users/1/flights'


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Настройка симуляции")
        self.geometry("400x300")

        self.label_title = ttk.Label(self, text="Настройка симуляции", font=("Arial", 28))
        self.label_title.pack()

        self.button_flights_list = ttk.Button(self, text="Все полеты", command=self.open_flights_list)
        self.button_flights_list.pack(padx=5, pady=5, anchor=tk.CENTER)

        self.button_new_flight = ttk.Button(self, text="Новый полет", command=self.open_new_flight)
        self.button_new_flight.pack(padx=5, pady=5, anchor=tk.CENTER)

    def open_flights_list(self):
        flights_list = FlightsList(self)
        self.withdraw()

    def open_new_flight(self):
        new_flight = NewFlight(self)
        self.withdraw()


class FlightsList(tk.Tk):
    def __init__(self, parent):
        super().__init__()
        self.parent: tk.Tk = parent
        self.title("Все полеты")
        self.geometry("400x400")

        self.label_title = ttk.Label(self, text="Список полетов", font=("Arial", 28))
        self.label_title.grid()

        request = requests.get(BACKEND_URL)
        if request.status_code == 200:
            flights = request.json()

            for i, flight in enumerate(flights):
                for c in range(2):
                    frame = self.flight_frame(i + 1)
                    frame.grid(row=(i + 1) // 2 + 1, column=c, padx=10, pady=10)
        else:
            self.label_error = ttk.Label(self, text="Ошибка загрузки")
            self.label_error.pack()

        self.button_back = ttk.Button(self, text="Назад", command=self.back)
        self.button_back.grid()

    def flight_frame(self, number):
        frame = ttk.Frame(self, borderwidth=1, relief=tk.SOLID, padding=5)

        flight_name = ttk.Label(frame, text=f"Полет {number + 1}")
        flight_name.grid()

        button_log = ttk.Button(frame, text="Лог полета")
        button_log.grid()

        button_delete = ttk.Button(frame, text="Удалить полет")
        button_delete.grid()

        return frame

    def back(self):
        self.parent.deiconify()
        self.destroy()


class NewFlight(tk.Tk):
    def __init__(self, parent):
        super().__init__()
        self.parent: tk.Tk = parent
        self.title("Все полеты")
        self.geometry("400x300")

        self.label_title = ttk.Label(self, text="Новый полет", font=("Arial", 28))
        self.label_title.pack()

        self.label_home = ttk.Label(self, text="Введите координаты")
        self.label_title.pack()
        self.home_entry = ttk.Entry(self)
        self.home_entry.pack()

        self.button_save = ttk.Button(self, text="Сохранить", command=self.save)
        self.button_save.pack(padx=5, pady=5)

        self.button_back = ttk.Button(self, text="Назад", command=self.back)
        self.button_back.pack(padx=5, pady=5)

    def save(self):
        home = self.home_entry.get()

        if self.check_coords(home):
            home_lat, home_lon = [x.strip() for x in home.split(',')]
            data = {"home": home, "plan": "none"}
            request = requests.post(BACKEND_URL, json=data)
        else:
            messagebox.showerror(title="Error", message="Введите координаты")
            return

        if request.status_code == 201:
            messagebox.showinfo(title="Информация о создании полета", message="Полет успешно создан")

            subprocess.Popen('make px4_sitl gazebo-classic', shell=True, cwd='/home/ddombrovskii/PX4-Autopilot',
                             env=dict(PX4_HOME_LAT=home_lat, PX4_HOME_LON=home_lon, **os.environ))
        else:
            messagebox.showerror(title="Информация о создании полета", message="Ошибка создания полета")

    @staticmethod
    def check_coords(line):
        try:
            re.match(r'^([-+]?\d{1,2}[.]\d+),\s*([-+]?\d{1,3}[.]\d+)$', line).group()
            return True
        except AttributeError:
            return False

    def back(self):
        self.parent.deiconify()
        self.destroy()


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
