import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from requests import get
from json import loads as jload
from ics import Calendar, Event
from datetime import datetime

def is_month_name(month):
    month_names = ['january', 'february', 'march', 'april', 'may', 'june',
                   'july', 'august', 'september', 'october', 'november', 'december']
    return month.lower() in month_names

def export_to_ics():
    selected_games = []
    for i, game in enumerate(games):
        if var_list[i].get() == 1:
            selected_games.append(game)

    calendar = Calendar()

    for game in selected_games:
        event = Event()
        event.name = game['title']
        event.begin = datetime.strptime(game['release_date'], '%Y-%m-%d')
        event.description = 'AAA Game' if game['is_AAA'] else 'Game'
        calendar.events.add(event)

    file_path = filedialog.asksaveasfilename(defaultextension=".ics", filetypes=[("ICS Files", "*.ics")])
    if file_path:
        with open(file_path, 'w') as f:
            f.write(str(calendar))
        print("ICS file exported successfully.")

plain_text = get("https://gamestatus.info/back/api/gameinfo/game/gamecalendar/?format=json").content.decode()
json = jload(plain_text)
json_calender = json["response_game_calendar"]

games = []
var_list = []

for month in json_calender:
    if is_month_name(month):
        upcoming_games_json = json_calender[month]
        if upcoming_games_json:
            for game in upcoming_games_json:
                games.append(game)

# Sort games based on 'is_AAA' key in descending order
games.sort(key=lambda x: x['is_AAA'], reverse=True)

root = tk.Tk()
root.title("Game Calendar")

canvas = tk.Canvas(root, height=400)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

for game in games:
    var = tk.IntVar()
    var_list.append(var)
    game_frame = tk.Frame(frame)
    game_frame.pack(anchor='w')
    checkbox = tk.Checkbutton(game_frame, text=game['title'] + ' ' + game['release_date'], variable=var)
    checkbox.pack(side=tk.LEFT)
    if game['is_AAA']:
        label = tk.Label(game_frame, text="(AAA)")
        label.pack(side=tk.LEFT)

export_button = tk.Button(frame, text="Export to ICS", command=export_to_ics)
export_button.pack()

canvas.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

root.mainloop()
