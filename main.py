import tkinter as tk
from tkinter import ttk, messagebox, font
import os
import sys


# PyInstaller's temp folder
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def format_amount(event=None):
    value = amount_entry.get().replace(",", "").strip()
    if value.isdigit():
        formatted = "{:,}".format(int(value))
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, formatted)
    elif value == "":
        amount_entry.delete(0, tk.END)


def calculate():
    try:
        amount_str: str = amount_entry.get().replace(",", "")
        amount = float(amount_str)
        mode: str = mode_var.get()

        rates: dict[str, float] = {"Day - 50%": 0.50, "Night - 60%": 0.60, "Barbari - 75%": 0.75, "Barbari - 79%": 0.79}

        if mode not in rates:
            messagebox.showerror(title="Error", message="Please select an operation type.")
            return

        rate: float = rates[mode]
        received: float = amount * rate
        fee: float = amount - received

        received_label.config(text=f"✅ Received: ${int(received):,}", fg="green")
        fee_label.config(text=f"❌ Fee: ${int(fee):,}", fg="red")
    except ValueError:
        messagebox.showerror(title="Invalid Input", message="Please enter a valid number.")


def create_main_window():
    root = tk.Tk()
    root.title("WashMoney")
    root.iconbitmap(resource_path("icon.ico"))
    root.geometry("250x300")
    root.resizable(False, False)
    root.configure(bg="#f4f4f4")

    default_font = font.Font(family="Tahoma", size=10)
    root.option_add("*Font", default_font)

    tk.Label(root, text="Amount (USD)", bg="#f4f4f4").pack(pady=(15, 5))
    global amount_entry
    amount_entry = tk.Entry(root, justify="center", font=("Tahoma", 9))
    amount_entry.pack(ipady=5, padx=30)
    amount_entry.insert(0, "50,000")
    amount_entry.bind("<KeyRelease>", format_amount)

    tk.Label(root, text="Operation Type", bg="#f4f4f4").pack(pady=(15, 5))
    global mode_var
    mode_var = tk.StringVar()
    mode_dropdown = ttk.Combobox(root, textvariable=mode_var, state="readonly", justify="center", font=("Tahoma", 9))
    mode_dropdown["values"] = list(
        {"Day - 50%": 0.50, "Night - 60%": 0.60, "Barbari - 75%": 0.75, "Barbari - 79%": 0.79}.keys()
    )
    mode_dropdown.current(0)
    mode_dropdown.pack(ipady=3, padx=30)
    tk.Button(root, text="Calculate", command=calculate, bg="green", fg="white", font=("Tahoma", 9, "bold")).pack(
        pady=5, ipadx=1, ipady=1
    )
    global received_label, fee_label
    received_label = tk.Label(root, text="", font=("Tahoma", 9), bg="#f4f4f4", justify="center")
    received_label.pack(pady=(10, 2))

    fee_label = tk.Label(root, text="", font=("Tahoma", 9), bg="#f4f4f4", justify="center")
    fee_label.pack(pady=(0, 10))

    return root


if __name__ == "__main__":
    app = create_main_window()
    app.mainloop()
