import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

MAX_W, MAX_H = 150, 600   # made wider
IMG_PATH = "images"

BMI_CLASSES = [
    ("underweight", 18.5, "Underweight", "#7db3ff"),
    ("normal", 25.0, "Normal", "#65c18c"),
    ("overweight", 30.0, "Overweight", "#f7c04a"),
    ("obese", 35.0, "Obese", "#f57c3a"),
    ("extreme", float("inf"), "Extremely Obese", "#e74c3c"),
]

def load_png_clamped(path: str, max_w=MAX_W, max_h=MAX_H) -> ImageTk.PhotoImage:
    try:
        im = Image.open(path).convert("RGBA")
        im.thumbnail((max_w, max_h), Image.LANCZOS)
        canvas = Image.new("RGBA", (max_w, max_h), (255, 255, 255, 0))
        ox = (max_w - im.width) // 2
        oy = (max_h - im.height) // 2
        canvas.paste(im, (ox, oy))
        return ImageTk.PhotoImage(canvas)
    except:
        ph = Image.new("RGBA", (max_w, max_h), (180, 180, 180, 255))
        return ImageTk.PhotoImage(ph)

class BMIWidget(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BMI Widget")
        self.configure(bg="#0f172a")
        self.option_add("*TCombobox*Listbox.font", ("Segoe UI", 12))

        style = ttk.Style(self)
        style.configure("TLabel", background="#0f172a", foreground="white", font=("Segoe UI", 14))
        style.configure("TButton", font=("Segoe UI", 14, "bold"), padding=8)
        style.configure("TEntry", font=("Segoe UI", 14), padding=6)

        # Gender dropdown
        ttk.Label(self, text="Gender:").grid(row=0, column=0, sticky="w", padx=10, pady=6)
        self.gender = ttk.Combobox(self, values=["men", "women"], font=("Segoe UI", 14), width=12)
        self.gender.current(0)
        self.gender.grid(row=0, column=1, pady=6, padx=10)

        # Height input
        ttk.Label(self, text="Height (cm):").grid(row=1, column=0, sticky="w", padx=10, pady=6)
        self.height = ttk.Entry(self, width=10)
        self.height.grid(row=1, column=1, pady=6, padx=10)

        # Weight input
        ttk.Label(self, text="Weight (kg):").grid(row=2, column=0, sticky="w", padx=10, pady=6)
        self.weight = ttk.Entry(self, width=10)
        self.weight.grid(row=2, column=1, pady=6, padx=10)

        # Calculate button
        self.calc_btn = ttk.Button(self, text="Calculate BMI", command=self.calc)
        self.calc_btn.grid(row=3, column=0, columnspan=2, pady=15)

        # Result BMI
        self.bmi_val = tk.Label(self, text="–", font=("Segoe UI", 36, "bold"), bg="#0f172a", fg="white")
        self.bmi_val.grid(row=4, column=0, columnspan=2, pady=10)

        self.chip = tk.Label(self, text="—", bg="#65c18c", fg="white", font=("Segoe UI", 18, "bold"), padx=16, pady=6)
        self.chip.grid(row=5, column=0, columnspan=2, pady=8)

        # Image display
        self.figure_label = tk.Label(self, bg="#0f172a")
        self.figure_label.grid(row=6, column=0, columnspan=2, pady=15)

        # preload placeholders
        self.images = {}
        for g in ["men", "women"]:
            self.images[g] = {}
            for key, _, _, _ in BMI_CLASSES:
                path = os.path.join(IMG_PATH, g, f"{key}.png")
                self.images[g][key] = load_png_clamped(path)

    def calc(self):
        try:
            h = float(self.height.get())
            w = float(self.weight.get())
            bmi = w / ((h / 100) ** 2)
        except:
            self.bmi_val.config(text="Err")
            self.chip.config(text="Invalid", bg="gray")
            return

        for key, maxv, label, color in BMI_CLASSES:
            if bmi < maxv:
                chosen = (key, label, color)
                break

        self.bmi_val.config(text=f"{bmi:.1f}")
        self.chip.config(text=chosen[1], bg=chosen[2])

        g = self.gender.get()
        self.figure_label.config(image=self.images[g][chosen[0]])
        self.figure_label.image = self.images[g][chosen[0]]

if __name__ == "__main__":
    app = BMIWidget()
    app.mainloop()
