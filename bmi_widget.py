import tkinter as tk
from tkinter import messagebox

def calculate_bmi():
    try:
        height = float(height_entry.get()) / 100  # convert cm → meters
        weight = float(weight_entry.get())
        bmi = weight / (height ** 2)

        # Show BMI
        bmi_value.set(f"{bmi:.2f}")

        # Categorize BMI
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obesity"

        messagebox.showinfo("BMI Result", f"Your BMI is {bmi:.2f} ({category})")
    except:
        messagebox.showerror("Error", "Please enter valid numbers")

# Tkinter Window
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("300x300")

# Labels & Entries
tk.Label(root, text="Height (cm)").pack(pady=5)
height_entry = tk.Entry(root)
height_entry.pack()

tk.Label(root, text="Weight (kg)").pack(pady=5)
weight_entry = tk.Entry(root)
weight_entry.pack()

# BMI Scale
tk.Label(root, text="BMI Value").pack(pady=5)
bmi_value = tk.StringVar()
bmi_scale = tk.Scale(root, variable=bmi_value, from_=10, to=40, orient="horizontal", length=200)
bmi_scale.pack()

# Button
tk.Button(root, text="Calculate BMI", command=calculate_bmi).pack(pady=10)

root.mainloop()
