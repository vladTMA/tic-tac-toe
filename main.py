# main.py
"""
# Игра "Крестики-нолики" настраиваемым количеством раундов и игр в раунде.
Поддерживает игру на поле 10x10 - выигрышная комбинация 4 символа подряд.
"""

import tkinter as tk
from tkinter import messagebox

# Настройки игры
GRID_SIZE = 10  # Размер игрового поля
WIN_LENGTH = 4  # Количество символов для победы

# Создание главного окна
window = tk.Tk()
window.title("Игра крестики-нолики")
window.geometry("600x960")

# Глобальные переменные игры
current_player = "X"  # Текущий игрок
buttons = []  # Массив кнопок игрового поля

# Переменные для счета
player_score = 0  # Счет игрока
opponent_score = 0  # Счет противника

# Переменные для раундов и партий
total_rounds = 3  # Общее количество раундов
games_per_round = 5  # Количество игр в раунде
current_round = 1  # Текущий раунд
games_played = 0  # Количество сыгранных игр в текущем раунде

# Виджеты для настройки игры
rounds_var = tk.IntVar(value=3)  # Переменная для количества раундов
games_var = tk.IntVar(value=5)  # Переменная для количества игр в раунде

# Переменные для выбора символов
player_symbol = tk.StringVar(value="X")  # Символ игрока
opponent_symbol = "O"  # Символ противника


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tip or not self.text:
            return
        # Используем координаты события для позиционирования тултипа
        x = event.x_root + 10
        y = event.y_root + 10
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1, font=("Arial", 10))
        label.pack()

    def hide(self, event=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None



# Создание интерфейса
def create_interface():
    """Создает элементы интерфейса игры"""
    local_top_frame = tk.Frame(window, bg="#f9f9f9")  # светлый фон
    local_top_frame.pack(side="top", fill="x", pady=10)

    # Все элементы пакуем в local_top_frame
    tk.Label(local_top_frame, text="Выберите символ:", font=("Arial", 12), bg="#f9f9f9").pack()
    tk.OptionMenu(local_top_frame, player_symbol, "X", "O").pack(pady=5)

    # Настройка количества раундов
    tk.Label(local_top_frame, text="Число раундов", font=("Arial", 12), bg="#f9f9f9").pack()
    tk.Spinbox(local_top_frame, from_=1, to=20, textvariable=rounds_var, width=5).pack(pady=2)

    # Настройка количества игр в раунде
    tk.Label(local_top_frame, text="Партий в раунде", font=("Arial", 12), bg="#f9f9f9").pack()
    tk.Spinbox(local_top_frame, from_=1, to=20, textvariable=games_var, width=5).pack(pady=2)

    button_frame = tk.Frame(local_top_frame)
    button_frame.pack(pady=10)

    # Кнопка Старт для применения настроек
    start_btn = tk.Button(local_top_frame, text="Старт", command=reset_game,  bg="#d0f0c0", width=10)
    start_btn.pack(side="left", padx=5)

    # Создание кнопки сброса в верхней части
    reset_btn = tk.Button(button_frame, text="Сброс", command=reset_game, bg="#f0d0d0", width=10)
    reset_btn.pack(side="left", padx=5)

    # Создание фрейма для счёта
    local_score_label = tk.Label(
        local_top_frame,
        text=f"Счёт — {player_symbol.get()}: {player_score} | {opponent_symbol}: {opponent_score}   Раунд: {current_round}/{total_rounds}   Игр: {games_played}/{games_per_round}",
        font=("Arial", 12, "bold")
    )
    local_score_label.pack()

    # Создание фрейма для игрового поля
    game_frame = tk.Frame(window, bg="#e6f2ff")  # светло-голубой фон
    game_frame.pack(side="top", fill='both', expand=True)

    local_board_frame = tk.Frame(game_frame, bg="#e6f2ff")
    local_board_frame.pack(expand=True)

    return local_top_frame, local_board_frame, local_score_label


# Универсальный алгоритм проверки выигрыша
def check_winner():
    def check_line(start_row, start_col, delta_row, delta_col):
        """Проверяет линию на наличие выигрышной комбинации"""
        symbol = buttons[start_row][start_col].cget("text")
        if symbol == "":
            return None

        # Проверяем в положительном направлении
        count_forward = 1
        for step in range(1, WIN_LENGTH):
            r = start_row + delta_row * step
            c = start_col + delta_col * step
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                if buttons[r][c].cget("text") == symbol:
                    count_forward += 1
                else:
                    break
            else:
                break

        # Проверяем в отрицательном направлении
        count_backward = 1
        for step in range(1, WIN_LENGTH):
            r = start_row - delta_row * step
            c = start_col - delta_col * step
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                if buttons[r][c].cget("text") == symbol:
                    count_backward += 1
                else:
                    break
            else:
                break

        total_count = count_forward + count_backward - 1  # -1 чтобы не считать стартовую клетку дважды
        if total_count >= WIN_LENGTH:
            return symbol
        return None

    # Проверяем все возможные начальные позиции и направления
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                winner = check_line(row, col, dr, dc)
                if winner:
                    return winner
    return None


def update_score_label(score_display):
    """Обновляет отображение счета и информации о раундах"""
    global player_score, opponent_score, current_round, total_rounds, games_played, games_per_round
    score_display.config(
        text=f"Счёт — {player_symbol.get()}: {player_score} | {opponent_symbol}: {opponent_score} | Раунд: {current_round}/{total_rounds} | Партий: {games_played}/{games_per_round}"
    )


def is_draw():
    """Проверяет, является ли игра ничьей (все клетки заполнены)"""
    return all(buttons[r][c].cget("text") != "" for r in range(GRID_SIZE) for c in range(GRID_SIZE))


def reset_board(score_lbl):
    """Очищает игровое поле и сбрасывает текущего игрока"""
    global current_player, opponent_symbol
    current_player = player_symbol.get()
    opponent_symbol = "O" if current_player == "X" else "X"
    for row in buttons:
        for btn in row:
            btn.config(text="", bg="#f0f0f0", state="normal")  # очищаем текст и возвращаем исходный цвет
    update_score_label(score_lbl)  # Передаём лейбл


def handle_round_end(score_lbl):
    """Обрабатывает завершение раунда и матча"""
    global current_round, games_played, player_score, opponent_score, total_rounds

    if games_played >= games_per_round:
        messagebox.showinfo("Раунд завершён", f"Раунд {current_round} завершён!")
        # Сброс счёта для нового раунда
        player_score = 0
        opponent_score = 0
        current_round += 1
        games_played = 0
        update_score_label(score_lbl)

        if current_round > total_rounds:
            messagebox.showinfo("Матч завершён", f"Все {total_rounds} раунды сыграны!")
            current_round = 1
            games_played = 0
            # Полный сброс счёта в конце матча уже сделан выше


def reset_game():
    """Полный сброс игры с обновлением настроек"""
    global current_player, opponent_symbol, player_score, opponent_score, games_played, current_round, total_rounds, games_per_round
    current_player = player_symbol.get()
    opponent_symbol = "O" if current_player == "X" else "X"
    player_score = 0
    opponent_score = 0
    games_played = 0
    current_round = 1
    total_rounds = rounds_var.get()
    games_per_round = games_var.get()
    reset_board(score_label)
    update_score_label(score_label)


def on_clic(row, col):
    """Обрабатывает клик по клетке игрового поля"""
    global current_player, games_played, current_round, player_score, opponent_score

    # Проверяем, что клетка пуста
    if buttons[row][col].cget("text") != "":
        return

    # Ставим символ текущего игрока
    buttons[row][col].config(
        text=current_player,
        fg="blue" if current_player == "X" else "red"
    )

    # Проверяем на выигрыш
    winner = check_winner()
    if winner:
        # Обновляем счет
        if winner == player_symbol.get():
            player_score += 1
        else:
            opponent_score += 1
        update_score_label(score_label)

        messagebox.showinfo("Игра завершена", f"Игрок {winner} победил!")
        games_played += 1
        handle_round_end(score_label)
        reset_board(score_label)
        return

    # Проверяем на ничью
    if is_draw():
        messagebox.showinfo("Игра завершена", "Ничья!")
        games_played += 1
        handle_round_end(score_label)
        reset_board(score_label)
        return

    # Переключаем игрока
    current_player = opponent_symbol if current_player == player_symbol.get() else player_symbol.get()

    status_label.config(text=f"Ход игрока: {current_player}")


def create_game_board(local_board_frame):
    """Создает игровое поле из кнопок"""
    for row_index in range(GRID_SIZE):
        button_row = []
        for col_index in range(GRID_SIZE):
            btn = tk.Button(
                local_board_frame,
                text="",
                font=("Arial", 16),
                width=3,
                height=2,
                bg="#f0f0f0",  # фон клетки
                activebackground="#d0e0ff",  # фон при нажатии
                relief="ridge",  # объёмная рамка
                bd=2,  # толщина рамки
                command=lambda r=row_index, c=col_index: on_clic(r, c)
            )
            btn.grid(row=row_index, column=col_index)
            Tooltip(btn, f"Клетка [{row_index + 1}, {col_index + 1}]")  # всплывающая подсказка
            button_row.append(btn)
        buttons.append(button_row)


# Создание интерфейса и игрового поля
top_frame, board_frame, score_label = create_interface()
create_game_board(board_frame)

status_label = tk.Label(top_frame, text=f"Ход игрока: {current_player}", font=("Arial", 12), bg="#f9f9f9")
status_label.pack(pady=5)


# Запуск главного цикла
window.mainloop()