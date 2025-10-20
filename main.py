# main.py
import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Игра крестики-нолики")
window.geometry("500x500")

current_player = "X"
buttons = []

# Создаём вложенный фрейм
frame = tk.Frame(window)
frame.place(relx=0.5, rely=0.5, anchor="center")  # Центрируем фрейм

def on_clic(row, col):
    pass

for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(frame, text="", font=("Arial", 20), width=5, height=3,
                        command=lambda r=i, c=j: on_clic(r, c))
        btn.grid(row=i, column=j)
        row.append(btn)
    buttons.append(row)

window.mainloop()
