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
player_name_labels = []
time_label_values = []
player_times = []
up_down_buttons = []
done_values = []
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
    title_text.set("Playing")
    state = 1
    enable_up_down(False)


def pause_event():
    global state
    title_text.set("Paused")
    state = 0
    enable_up_down(True)


def is_done(row):
    return done_values[row].get() == 1


def done_event(row):
    if is_done(row) and row == current_row:
        next_event()


def next_event():
    original_row = current_row
    next_row()
    while is_done(current_row) and current_row != original_row:
        next_row()
    if current_row == original_row and is_done(current_row):
        pause_event()
    player_name_labels[original_row].configure(style="label.TLabel")
    player_name_labels[current_row].configure(style="focus.TLabel")


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
    if time_left >= 0:
        minutes = math.floor(time_left / 60)
        time_left = time_left - minutes * 60
        seconds = math.floor(time_left)
        minutes_text = str(minutes).zfill(2)
        seconds_text = str(seconds).zfill(2)
        return f'{minutes_text}:{seconds_text}'
    else:
        time_left = time_left * -1
        minutes = math.floor(time_left / 60)
        time_left = time_left - minutes * 60
        seconds = math.floor(time_left)
        minutes_text = str(minutes).zfill(2)
        seconds_text = str(seconds).zfill(2)
        return f'-{minutes_text}:{seconds_text}'



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
    if initial_minutes < 0 or initial_minutes > 120:
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
    if row == 0:
        name_label.configure(style="focus.TLabel")
    name_label.grid(row = row + 1, column = 0, padx=5, pady=5, sticky="news")
    player_name_labels.append(name_label)

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

    done_value = tkinter.IntVar(value=0)
    done_button = ttk.Checkbutton(master=window, text="Done", command = lambda: done_event(row),
                                  variable=done_value,
                                  style="small.TCheckbutton")
    done_button.grid(row = row + 1, column = 4, padx=5, pady=5, sticky="news")
    done_values.append(done_value)


def create_toolbar():
    play_button = ttk.Button(master=window, text="Play", command = play_event, style = "big.TButton")
    play_button.grid(row = len(player_times) + 1, column = 0, padx=5, pady=5, sticky="news")

    next_button = ttk.Button(master=window, text="Next", command = next_event, style = "big.TButton")
    next_button.grid(row = len(player_times) + 1, column = 1, padx=5, pady=5, sticky="news")

    pause_button = ttk.Button(master=window, text="Pause", command = pause_event, style = "big.TButton")
    pause_button.grid(row = len(player_times) + 1, column = 2, padx=5, pady=5, columnspan=3, sticky="news")


def key_pressed(event):
    if event.char == " " or event.char == "n":
        next_event()
    if event.char == "p":
        pause_event()
    if event.char == "d":
        done_event(current_row)
    if event.char == "+":
        increase_font()
    if event.char == "-":
        decrease_font()


def set_styles():
    style.configure('big.TButton', font=(None, font_size))
    style.configure('small.TButton', font=(None, math.floor(font_size / 2)))
    style.configure('label.TLabel', font=(None, font_size))
    style.configure('focus.TLabel', font=(None, font_size), background='green')
    style.configure('small.TCheckbutton', font=(None, font_size))


def increase_font():
    global font_size
    font_size += 5
    set_styles()


def decrease_font():
    global font_size
    font_size -= 5
    set_styles()


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

    create_toolbar()

    window.after(100, tick)

    window.columnconfigure("all", weight=1)
    window.rowconfigure("all", weight=1)

    set_styles()
    window.bind("<Key>", key_pressed)
    window.mainloop()


if __name__ == "__main__":
    main()