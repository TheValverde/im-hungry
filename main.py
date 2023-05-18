import customtkinter as ctk
import tkinter as tk
import json
import random
from datetime import datetime

# Load data from json file if it exists, otherwise use an empty list
try:
    with open('data.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    data = []

class AddMealDialog(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Add Meal")
        self.restaurant_name = tk.StringVar()
        self.meal_name = tk.StringVar()
        self.meal_price = tk.StringVar()
        self.start_hour = tk.StringVar()
        self.end_hour = tk.StringVar()

        ctk.CTkLabel(self, text="Add Meal").grid(row=0, column=0, columnspan=2)

        ctk.CTkLabel(self, text="Restaurant Name:").grid(row=1, column=0)
        ctk.CTkEntry(self, textvariable=self.restaurant_name).grid(row=1, column=1)

        tk.Label(self, text="Meal Name:").grid(row=2, column=0)
        tk.Entry(self, textvariable=self.meal_name).grid(row=2, column=1)

        tk.Label(self, text="Meal Price:").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.meal_price).grid(row=3, column=1)

        tk.Label(self, text="Start Hour (24h):").grid(row=4, column=0)
        tk.Entry(self, textvariable=self.start_hour).grid(row=4, column=1)

        tk.Label(self, text="End Hour (24h):").grid(row=5, column=0)
        tk.Entry(self, textvariable=self.end_hour).grid(row=5, column=1)

        tk.Button(self, text="Save", command=self.save_meal).grid(row=6, column=0, columnspan=2)

    def save_meal(self):
        self.result = [self.restaurant_name.get(), self.meal_name.get(), float(self.meal_price.get()), self.start_hour.get(), self.end_hour.get()]
        self.destroy()

class MealInfoPanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure((0, 1), weight=1)

        self.restuarant_name = tk.Label(self, text="Restaurant Name: ")
        self.restuarant_name.grid(row=0, column=0, sticky="w")

        self.meal_name = tk.Label(self, text="Meal Name: ")
        self.meal_name.grid(row=1, column=0, sticky="w")

        self.meal_price = tk.Label(self, text="Meal Price: ")
        self.meal_price.grid(row=2, column=0, sticky="w")

        self.meal_hours = tk.Label(self, text="Available Hours: ")
        self.meal_hours.grid(row=3, column=0, sticky="w")

    def update_info(self, meal):
        self.restuarant_name.configure(text=f"Restaurant Name: {meal[0]}")
        self.meal_name.configure(text=f"Meal Name: {meal[1]}")
        self.meal_price.configure(text=f"Meal Price: {meal[2]}")
        self.meal_hours.configure(text=f"Available Hours: {meal[3]}-{meal[4]}")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.meals = data if data else [] # Load meals from JSON data

        self.title("I'm Hungry")
        self.geometry("400x400")
        self.grid_columnconfigure((0, 1), weight=1)

        self.button = ctk.CTkButton(self, text="I'm Hungry", command=self.hungry_callback)
        self.button.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.add_meal_button = ctk.CTkButton(self, text="Add Meal", command=self.add_meal)
        self.add_meal_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew", columnspan=2)

        self.meal_info_panel = MealInfoPanel(self)
        self.meal_info_panel.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=2)


    def hungry_callback(self):
        available_meals = [meal for meal in self.meals if self.is_within_hours(meal[3], meal[4])]
        if available_meals:
            meal = random.choice(available_meals)
            self.meal_info_panel.update_info(meal)
        else:
            self.button.configure(text="No meals available.")

    def is_within_hours(self, start, end):
        current_time = datetime.now().time()
        start_time = datetime.strptime(start, "%H:%M").time()
        end_time = datetime.strptime(end, "%H:%M").time()
        if start_time < end_time:
            return start_time <= current_time <= end_time
        else:  # crosses midnight
            return start_time <= current_time or current_time <= end_time

    def add_meal(self):
        dialog = AddMealDialog(self)
        self.wait_window(dialog)
        self.meals.append(dialog.result)

        # Save meals to json file every time a new one is added
        with open('data.json', 'w') as f:
            json.dump(self.meals, f)

app = App()
app.mainloop()
