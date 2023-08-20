import tkinter
import math
from tkinter import ttk
from jproperties import Properties
import time

window = tkinter.Tk()
style = ttk.Style()
title_text = tkinter.StringVar(value="Paused")
window_width = 800
window_height = 600
font_size = 50

player_label_values = []
time_label_values = []
player_times = []
up_down_buttons = []
players_done = []
done_buttons = []
old_seconds = time.time()
state = 0 # 0 = paused, 1 = running
current_row = 0
num_players = 0


FONT = "Calibri "
PROPERTIES_FILE_NAME = "grimdark-clock.properties"
PROP_PLAYERS = "players"
PROP_MINUTES = "minutes"
PROP_FONT_SIZE = "fontsize"


def play_event():
    global state
    title_text.set("Playing: " + player_label_values[current_row].get())
    state = 1
    enable_up_down(False)


def pause_event():
    global state
    title_text.set("Paused: " + player_label_values[current_row].get())
    for row in range(num_players):
        players_done[row] = 0
        done_buttons[row]["state"] = "normal"
    state = 0
    enable_up_down(True)


def done_event(row):
    players_done[row] = 1
    done_buttons[row]["state"] = "disabled"

    if row == current_row:
        next_event()


def next_event():
    original_row = current_row
    next_row()
    while players_done[current_row] == 1 and current_row != original_row:
        next_row()
    if current_row == original_row and players_done[current_row] == 1:
        pause_event()
    if state == 0:
        title_text.set("Paused: " + player_label_values[current_row].get())
    else:
        title_text.set("Playing: " + player_label_values[current_row].get())


def next_row():
    global current_row
    current_row += 1
    if current_row >= num_players:
        current_row = 0


def tick():
    global old_seconds

    seconds = time.time()
    elapsed = seconds - old_seconds
    old_seconds = seconds

    if state == 1:
        player_times[current_row] -= elapsed
        time_left = player_times[current_row]
        time_label_values[current_row].set(format_time(time_left))

    window.after(100, tick)


def enable_up_down(enable):
    if enable:
        for button in up_down_buttons:
            button["state"] = "normal"
    else:
        for button in up_down_buttons:
            button["state"] = "disabled"


def format_time(time_left):
    minutes = math.floor(time_left / 60)
    time_left = time_left - minutes * 60
    seconds = math.floor(time_left)
    minutes_text = str(minutes).zfill(2)
    seconds_text = str(seconds).zfill(2)
    return f'{minutes_text}:{seconds_text}'


def up_event(row):
    other = row - 1
    swap(row, other)


def down_event(row):
    other = row + 1
    swap(row, other)


def swap(row, other):
    name = player_label_values[row].get()
    player_label_values[row].set(player_label_values[other].get())
    player_label_values[other].set(name)

    player_time = player_times[row]
    player_times[row] = player_times[other]
    player_times[other] = player_time

    time_label_values[row].set(format_time(player_times[row]))
    time_label_values[other].set(format_time(player_times[other]))


def input_with_default(question, default):
    if default is None:
        answer = input(question + ": ")
    else:
        answer = input(question + " (" + default.data + "): ")
    if answer == "":
        return default.data
    return answer


def read_parameters():
    configs = Properties()
    try:
        with open(PROPERTIES_FILE_NAME, 'rb') as config_file:
            configs.load(config_file)
    except FileNotFoundError as f:
        print("No properties found, creating it.")

    names = input_with_default("Name of players, separate with space", configs.get(PROP_PLAYERS))
    player_names = names.split()
    if len(player_names) < 2 or len(player_names) > 7:
        print("Invalid number of players, try between 2 and 7")
        exit(1)
    configs[PROP_PLAYERS] = names
    with open(PROPERTIES_FILE_NAME, "wb") as f:
        configs.store(f, encoding="utf-8")

    initial_minutes = int(input_with_default("How many minutes do each player start with", configs.get(PROP_MINUTES)))
    if initial_minutes < 5 or initial_minutes > 120:
        print("Invalid starting time, try something 5 and 120")
        exit(1)
    configs[PROP_MINUTES] = str(initial_minutes)
    with open(PROPERTIES_FILE_NAME, "wb") as f:
        configs.store(f, encoding="utf-8")

    return player_names, initial_minutes


def create_player_row(player_names, row, initial_minutes):
    name_value = tkinter.StringVar(value=player_names[row])
    player_label_values.append(name_value)
    name_label = ttk.Label(master=window, textvariable=name_value, style="label.TLabel")
    name_label.grid(row = row + 1, column = 0, padx=5, pady=5, sticky="news")

    time_value = tkinter.StringVar(value=str(initial_minutes) + ":00")
    time_label = ttk.Label(master=window, textvariable=time_value, style="label.TLabel")
    time_label_values.append(time_value)
    time_label.grid(row = row + 1, column = 1, padx=5, pady=5, sticky="news")

    if row > 0:
        up_button = ttk.Button(master=window, text="Up", command=lambda: up_event(row), style="small.TButton")
        up_button.grid(row = row + 1, column = 2, padx=5, pady=5, sticky="news")
        up_down_buttons.append(up_button)

    if row < num_players - 1:
        down_button = ttk.Button(master=window, text="Down", command = lambda: down_event(row), style="small.TButton")
        down_button.grid(row = row + 1, column = 3, padx=5, pady=5, sticky="news")
        up_down_buttons.append(down_button)

    done_button = ttk.Button(master=window, text="Done", command = lambda: done_event(row), style="small.TButton")
    done_button.grid(row = row + 1, column = 4, padx=5, pady=5, sticky="news")
    done_buttons.append(done_button)


def create_toolbar():
    play_icon = tkinter.PhotoImage(file='play-icon.png')
    play_button = ttk.Button(master=window, text="Play", image = play_icon, command = play_event, style = "big.TButton")
    play_button.grid(row = len(player_times) + 1, column = 0, padx=5, pady=5, sticky="news")

    next_icon = tkinter.PhotoImage(file='next-icon.png')
    next_button = ttk.Button(master=window, text="Next", image = next_icon, command = next_event, style = "big.TButton")
    next_button.grid(row = len(player_times) + 1, column = 1, padx=5, pady=5, sticky="news")

    pause_icon = tkinter.PhotoImage(file='pause-icon.png')
    pause_button = ttk.Button(master=window, text="Pause", image = pause_icon, command = pause_event, style = "big.TButton")
    pause_button.grid(row = len(player_times) + 1, column = 2, padx=5, pady=5, columnspan=3, sticky="news")


def key_pressed(event):
    if event.char == " ":
        next_event()
    if event.char == "p":
        pause_event()
    if event.char == "d":
        done_event(current_row)
    if event.char == "+":
        increase_font()
    if event.char == "-":
        decrease_font()


def increase_font():
    global font_size
    font_size += 5
    style.configure('big.TButton', font=(None, font_size))
    style.configure('small.TButton', font=(None, math.floor(font_size / 2)))
    style.configure('label.TLabel', font=(None, font_size))


def decrease_font():
    global font_size
    font_size -= 5
    style.configure('big.TButton', font=(None, font_size))
    style.configure('small.TButton', font=(None, math.floor(font_size / 2)))
    style.configure('label.TLabel', font=(None, font_size))


def main():
    global num_players
    player_names, initial_minutes = read_parameters()
    num_players = len(player_names)

    window.title("Grimdark Clock")
    window.geometry("800x600")

    title_label = ttk.Label(master = window, textvariable = title_text, style="label.TLabel")
    title_label.grid(row = 0, column = 1, columnspan = 3, sticky="news")

    for row in range(0, len(player_names)):
        create_player_row(player_names, row, initial_minutes)
        player_times.append(initial_minutes * 60)
        players_done.append(0)

    create_toolbar()

    window.after(100, tick)

    window.columnconfigure(tuple(range(5)), weight=1)
    window.rowconfigure(tuple(range(num_players + 2)), weight=1)

    style.configure('big.TButton', font=(None, font_size))
    style.configure('small.TButton', font=(None, math.floor(font_size / 2)))
    style.configure('label.TLabel', font=(None, font_size))

    window.bind("<Key>", key_pressed)
    window.mainloop()


if __name__ == "__main__":
    main()