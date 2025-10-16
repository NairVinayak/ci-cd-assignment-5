import tkinter as tk
from tkinter import messagebox

# Create main window
root = tk.Tk()
root.title("Sports Merchandise Store")
root.geometry("350x400")

# Title Label
tk.Label(root, text="🏀 Sports Merchandise Store 🏏", font=("Arial", 14, "bold")).pack(pady=10)

# Items and Prices
items = {
    "Football": 500,
    "Cricket Bat": 1200,
    "Tennis Racket": 800,
    "Basketball": 600,
    "Jersey": 400
}

# Variables for checkboxes
vars = {}
for item, price in items.items():
    var = tk.IntVar()
    chk = tk.Checkbutton(root, text=f"{item} - ₹{price}", variable=var, font=("Arial", 10))
    chk.pack(anchor="w", padx=30)
    vars[item] = var

# Function to calculate total
def calculate_total():
    total = 0
    for item, var in vars.items():
        if var.get() == 1:
            total += items[item]
    messagebox.showinfo("Total Bill", f"Your total amount is ₹{total}")

# Button
tk.Button(root, text="Calculate Bill", command=calculate_total, bg="green", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

root.mainloop()
