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


def check_winner():
    for i in range(3):
        if buttons[i][0].cget("text") == buttons[i][1].cget("text") == buttons[i][2].cget("text") != "":
            return True
        if buttons[0][i].cget("text") == buttons[1][i].cget("text") == buttons[2][i].cget("text") != "":
            return True

    if buttons[0][0].cget("text") == buttons[1][1].cget("text") == buttons[2][2].cget("text") != "":
        return True
    if buttons[0][2].cget("text") == buttons[1][1].cget("text") == buttons[2][0].cget("text") != "":
        return True

    return False


def on_clic(row, col):
    global current_player

    if buttons[row][col].cget("text") != "":
        return

    buttons[row][col].config(text = current_player)

    if check_winner():
        messagebox.showinfo("Игра завершена", f"Игрок {current_player} победил!")

    current_player = "0" if current_player == "X" else "X"


for row_index in range(3):
    button_row = []
    for col_index in range(3):
        btn = tk.Button(frame, text="", font=("Arial", 20), width=5, height=3,
                        command=lambda r=row_index, c=col_index: on_clic(r, c))
        btn.grid(row=row_index, column=col_index)
        button_row.append(btn)
    buttons.append(button_row)

window.mainloop()
