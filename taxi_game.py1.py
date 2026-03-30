import tkinter as tk
from tkinter import messagebox
import random
import datetime

player_x = 0
player_y = 0
passenger_x = 2
passenger_y = 3
dest_x = 4
dest_y = 1
money = 0
has_passenger = False
steps = 0

def write_log(message):
    with open("taxi_log.txt", "a", encoding="utf-8") as f:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time}] {message}\n")

def move(direction):
    global player_x, player_y, passenger_x, passenger_y, dest_x, dest_y
    global money, has_passenger, steps
    
    old_x = player_x
    old_y = player_y
    
    if direction == "up" and player_y > 0:
        player_y -= 1
    elif direction == "down" and player_y < 4:
        player_y += 1
    elif direction == "left" and player_x > 0:
        player_x -= 1
    elif direction == "right" and player_x < 4:
        player_x += 1
    else:
        return
    
    steps += 1
    steps_label.config(text="Шагов: " + str(steps))
    
    write_log(f"Ход: ({old_x},{old_y}) → ({player_x},{player_y})")
    
    if not has_passenger and player_x == passenger_x and player_y == passenger_y:
        has_passenger = True
        write_log("Пассажир сел в такси")
        messagebox.showinfo("Информация", "Пассажир сел в такси!")
    
    if has_passenger and player_x == dest_x and player_y == dest_y:
        money += 50
        has_passenger = False
        write_log(f"Доставка! +50 денег. Всего: {money}")
        messagebox.showinfo("Информация", "Пассажир доставлен! +50 денег")
        
        passenger_x = random.randint(0, 4)
        passenger_y = random.randint(0, 4)
        dest_x = random.randint(0, 4)
        dest_y = random.randint(0, 4)
        
        while passenger_x == dest_x and passenger_y == dest_y:
            dest_x = random.randint(0, 4)
            dest_y = random.randint(0, 4)
        
        write_log(f"Новый пассажир на ({passenger_x},{passenger_y}), пункт назначения ({dest_x},{dest_y})")
    
    update_map()

def update_map():
    for y in range(5):
        for x in range(5):
            if x == player_x and y == player_y:
                if has_passenger:
                    map_labels[y][x].config(text="X")
                else:
                    map_labels[y][x].config(text="T")
            elif not has_passenger and x == passenger_x and y == passenger_y:
                map_labels[y][x].config(text="P")
            elif has_passenger and x == dest_x and y == dest_y:
                map_labels[y][x].config(text="D")
            else:
                map_labels[y][x].config(text=".")
    
    money_label.config(text="Деньги: " + str(money))
    if has_passenger:
        pass_label.config(text="Пассажир: есть")
    else:
        pass_label.config(text="Пассажир: нет")

def open_rules():
    rules_win = tk.Toplevel()
    rules_win.title("Правила игры")
    rules_win.geometry("300x250")
    rules_win.resizable(False, False)
    
    text = """ЦЕЛЬ ИГРЫ:
Заработать деньги, перевозя пассажиров

УПРАВЛЕНИЕ:
Кнопки со стрелками

ОБОЗНАЧЕНИЯ:
T - такси (пустое)
X - такси с пассажиром
P - пассажир
D - пункт назначения
. - пустая клетка

ПРАВИЛА:
1. Найди P
2. Вези к D
3. Получи +50 денег"""
    
    label = tk.Label(rules_win, text=text, font=("Arial", 9), justify="left")
    label.pack(pady=10, padx=10)
    
    btn = tk.Button(rules_win, text="Закрыть", command=rules_win.destroy)
    btn.pack(pady=5)

def open_stats():
    stats_win = tk.Toplevel()
    stats_win.title("Статистика")
    stats_win.geometry("450x350")
    stats_win.resizable(False, False)
    
    label_title = tk.Label(stats_win, text="ПОСЛЕДНИЕ ДЕЙСТВИЯ", font=("Arial", 12, "bold"))
    label_title.pack(pady=5)
    
    text_area = tk.Text(stats_win, wrap="word", font=("Courier", 10))
    text_area.pack(fill="both", expand=True, padx=10, pady=5)
    
    try:
        with open("taxi_log.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            start = max(0, len(lines) - 20)
            for i in range(start, len(lines)):
                text_area.insert("end", lines[i])
    except FileNotFoundError:
        text_area.insert("end", "Лог-файл ещё не создан.\nСыграйте несколько ходов.")
    
    text_area.config(state="disabled")
    
    btn_close = tk.Button(stats_win, text="Закрыть", command=stats_win.destroy)
    btn_close.pack(pady=5)

def start_game():
    global game_win, map_labels, money_label, pass_label, steps_label
    
    menu_win.destroy()
    
    global player_x, player_y, passenger_x, passenger_y, dest_x, dest_y, money, has_passenger, steps
    player_x, player_y = 0, 0
    passenger_x, passenger_y = 2, 3
    dest_x, dest_y = 4, 1
    money = 0
    has_passenger = False
    steps = 0
    
    write_log("Игра начата")
    
    game_win = tk.Tk()
    game_win.title("Игра Таксист")
    game_win.geometry("400x500")
    game_win.resizable(False, False)
    
    info_frame = tk.Frame(game_win)
    info_frame.pack(fill="x", padx=10, pady=5)
    
    money_label = tk.Label(info_frame, text="Деньги: 0", font=("Arial", 10))
    money_label.pack(side="left", padx=5)
    
    pass_label = tk.Label(info_frame, text="Пассажир: нет", font=("Arial", 10))
    pass_label.pack(side="left", padx=5)
    
    steps_label = tk.Label(info_frame, text="Шагов: 0", font=("Arial", 10))
    steps_label.pack(side="right", padx=5)
    
    map_frame = tk.Frame(game_win)
    map_frame.pack(pady=10)
    
    map_labels = []
    for i in range(5):
        row = []
        for j in range(5):
            label = tk.Label(map_frame, text=".", font=("Courier", 20), 
                           width=2, height=1, relief="solid", borderwidth=1)
            label.grid(row=i, column=j, padx=1, pady=1)
            row.append(label)
        map_labels.append(row)
    
    control_frame = tk.Frame(game_win)
    control_frame.pack(pady=10)
    
    btn_up = tk.Button(control_frame, text="Вверх", width=8, command=lambda: move("up"))
    btn_up.grid(row=0, column=1, padx=2, pady=2)
    
    btn_left = tk.Button(control_frame, text="Влево", width=8, command=lambda: move("left"))
    btn_left.grid(row=1, column=0, padx=2, pady=2)
    
    btn_down = tk.Button(control_frame, text="Вниз", width=8, command=lambda: move("down"))
    btn_down.grid(row=1, column=1, padx=2, pady=2)
    
    btn_right = tk.Button(control_frame, text="Вправо", width=8, command=lambda: move("right"))
    btn_right.grid(row=1, column=2, padx=2, pady=2)
    
    btn_menu = tk.Button(game_win, text="В главное меню", bg="lightgray", command=back_to_menu)
    btn_menu.pack(pady=5)
    
    update_map()
    game_win.mainloop()

def back_to_menu():
    write_log("Выход в главное меню")
    game_win.destroy()
    create_menu()

def create_menu():
    global menu_win
    
    menu_win = tk.Tk()
    menu_win.title("Таксист - Главное меню")
    menu_win.geometry("300x350")
    menu_win.resizable(False, False)
    
    label_title = tk.Label(menu_win, text="ИГРА ТАКСИСТ", font=("Arial", 16, "bold"))
    label_title.pack(pady=20)
    
    btn_start = tk.Button(menu_win, text="Новая игра", width=20, height=2,
                         bg="lightgreen", command=start_game)
    btn_start.pack(pady=5)
    
    btn_rules = tk.Button(menu_win, text="Правила", width=20, height=2,
                         bg="lightblue", command=open_rules)
    btn_rules.pack(pady=5)
    
    btn_stats = tk.Button(menu_win, text="Статистика", width=20, height=2,
                         bg="lightyellow", command=open_stats)
    btn_stats.pack(pady=5)
    
    btn_exit = tk.Button(menu_win, text="Выход", width=20, height=2,
                        bg="salmon", command=menu_win.quit)
    btn_exit.pack(pady=5)
    
    label_author = tk.Label(menu_win, text="Корнеев Д.В.", font=("Arial", 8))
    label_author.pack(side="bottom", pady=10)
    
    menu_win.mainloop()

create_menu()