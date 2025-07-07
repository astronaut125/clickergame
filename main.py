#waiting for scrape

import tkinter as tk
import random
import sys
import os
import json
import platform
import signal
import pathlib
from PIL import Image, ImageTk

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

save_file = os.path.join(str(pathlib.Path.home()), "MarsCorn_progress.json")

def show_message(text, duration=3000):
    message_var.set(text)
    window.after(duration, lambda: message_var.set(""))

def load_progress():
    global points, activeMultiplier, auto_clickers, auto_clicker_cost, unlock_threshold
    try:
        with open(save_file, "r") as f:
            data = json.load(f)
            points = data.get("points", 0)
            activeMultiplier = data.get("multiplier", 1)
            auto_clickers = data.get("auto_clickers", 0)
            auto_clicker_cost = data.get("auto_clicker_cost", 1000)
            unlock_threshold = data.get("unlock_threshold", 10)
            refresh_ui_after_load()
    except Exception:
        show_message("⚠️ No saved progress found or failed to load.")

def save_progress():
    try:
        with open(save_file, "w") as f:
            json.dump({
                "points": points,
                "multiplier": activeMultiplier,
                "auto_clickers": auto_clickers,
                "auto_clicker_cost": auto_clicker_cost,
                "unlock_threshold": unlock_threshold
            }, f)
        show_message("📎 Progress saved!")
    except Exception as e:
        show_message(f"❌ Failed to save: {e}")

def refresh_ui_after_load():
    points_var.set(f"Points: {points}")
    status_var.set(f"Multiplier: {activeMultiplier} | Auto-Clickers: {auto_clickers}")
    upgrade_button.config(text=f"Upgrade ({unlock_threshold})")
    autoclicker.config(text=f"Buy Worker Drone to work for you bcuz ur lazy ({auto_clicker_cost})")
    rebuild_auto_clicker_display()

def rebuild_auto_clicker_display():
    for widget in cursor_frame.winfo_children():
        widget.destroy()
    cursor_canvas.delete("all")
    cursor_sprites.clear()
    cursors.clear()
    for i in range(auto_clickers):
        if cursor_img:
            x = 50 + i * 40
            y = 10
            sprite_id = cursor_canvas.create_image(x, y, image=cursor_img)
            cursor_sprites.append((sprite_id, x, y))
        else:
            cursor = tk.Label(cursor_frame, text="🖚️", font=("Comic Sans", 20), bg="#007BFF")
            cursor.pack(side="left", padx=5)
            cursors.append(cursor)

window = tk.Tk()
window.title("Mars Corn")
window.geometry("900x700")

points = 0
activeMultiplier = 1
unlock_threshold = 10
auto_clickers = 0
auto_clicker_cost = 1000

points_var = tk.StringVar(value=f"Points: {points}")
status_var = tk.StringVar(value=f"Multiplier: {activeMultiplier} | Auto-Clickers: {auto_clickers}")
message_var = tk.StringVar(value="")

label = tk.Label(window, textvariable=points_var, font=("Comic Sans", 16), bg="#FF00EA", fg="#00FF1E")
label.pack(pady=20)

status_label = tk.Label(window, textvariable=status_var, font=("Comic Sans", 12), bg="#FF00EA", fg="#000000")
status_label.pack(pady=5)

message_label = tk.Label(window, textvariable=message_var, font=("Comic Sans", 12), bg="#007BFF", fg="#FFFFFF")
message_label.pack(pady=10)

cursor_frame = tk.Frame(window, bg="#007BFF", height=50)
cursor_frame.pack(pady=5)

cursor_canvas = tk.Canvas(window, width=900, height=100, bg="#007BFF", highlightthickness=0)
cursor_canvas.pack(pady=10)
cursor_sprites = []
cursors = []

cursor_img = None
cursor_click_img = None
try:
    cursor_path = resource_path("cursor.png")
    cursor_click_path = resource_path("cursor_click.png")
    cursor_img_raw = Image.open(cursor_path).resize((32, 32))
    cursor_click_img_raw = Image.open(cursor_click_path).resize((32, 32))
    cursor_img = ImageTk.PhotoImage(cursor_img_raw)
    cursor_click_img = ImageTk.PhotoImage(cursor_click_img_raw)
    window.cursor_img = cursor_img
    window.cursor_click_img = cursor_click_img
except Exception:
    cursor_img = None
    cursor_click_img = None

def update_labels():
    points_var.set(f"Points: {points}")
    status_var.set(f"Multiplier: {activeMultiplier} | Auto-Clickers: {auto_clickers}")

def increase_points():
    global points
    crit = random.random() < 0.1
    gain = activeMultiplier * (5 if crit else 1)
    points += gain
    update_labels()
    if crit:
        show_message("💥 You caused a lot of chaos, young human...")

def upgrade_action():
    global activeMultiplier, points, unlock_threshold
    if points >= unlock_threshold:
        points -= unlock_threshold
        activeMultiplier += 1
        unlock_threshold += 10
        upgrade_button.config(text=f"Upgrade ({unlock_threshold})")
        update_labels()
        show_message("🛠️ You wasted your money lol")
    else:
        show_message("❌ Not enough points to upgrade.")

def buy_auto_clicker():
    global points, auto_clickers, auto_clicker_cost
    if points >= auto_clicker_cost:
        points -= auto_clicker_cost
        auto_clickers += 1
        auto_clicker_cost += 25
        autoclicker.config(text=f"Buy Worker Drone to work for you bcuz ur lazy ({auto_clicker_cost})")
        update_labels()
        show_message("🛒 Worker Drone hired!")
        if cursor_img:
            x = 50 + (auto_clickers - 1) * 40
            y = 10
            sprite_id = cursor_canvas.create_image(x, y, image=cursor_img)
            cursor_sprites.append((sprite_id, x, y))
        else:
            cursor = tk.Label(cursor_frame, text="🖚️", font=("Comic Sans", 20), bg="#007BFF")
            cursor.pack(side="left", padx=5)
            cursors.append(cursor)
    else:
        show_message("❌ Not enough points to buy a Worker Drone.")

def get_click_button_position():
    x = click_button.winfo_rootx() - window.winfo_rootx()
    y = click_button.winfo_rooty() - window.winfo_rooty() - 550
    return x + click_button.winfo_width() // 2, y + click_button.winfo_height() // 2

def move_cursor_toward(sprite_id, x, y, dx, dy, steps):
    if steps <= 0:
        cursor_canvas.itemconfig(sprite_id, image=cursor_click_img)
        window.after(100, lambda: cursor_canvas.itemconfig(sprite_id, image=cursor_img))
        reset_cursor_positions()
        return
    cursor_canvas.move(sprite_id, dx, dy)
    window.after(30, lambda: move_cursor_toward(sprite_id, x + dx, y + dy, dx, dy, steps - 1))

def animate_cursor_clicks():
    target_x, target_y = get_click_button_position()
    for i, (sprite_id, _, _) in enumerate(cursor_sprites):
        x0, y0 = cursor_canvas.coords(sprite_id)
        dx = (target_x - x0) / 10
        dy = (target_y - y0) / 10
        move_cursor_toward(sprite_id, x0, y0, dx, dy, steps=10)

def reset_cursor_positions():
    for sprite_id, x, y in cursor_sprites:
        cursor_canvas.coords(sprite_id, x, y)

def auto_click():
    global points
    if auto_clickers > 0:
        points += auto_clickers
        update_labels()
        animate_cursor_clicks()
    window.after(1000, auto_click)

def reset_game():
    global points, activeMultiplier, auto_clickers, auto_clicker_cost, unlock_threshold
    points = 0
    activeMultiplier = 1
    auto_clickers = 0
    auto_clicker_cost = 1000
    unlock_threshold = 10
    rebuild_auto_clicker_display()
    update_labels()
    upgrade_button.config(text=f"Upgrade ({unlock_threshold})")
    autoclicker.config(text=f"Buy Worker Drone to work for you bcuz ur lazy ({auto_clicker_cost})")
    show_message("🔄 Game reset!")

click_button = tk.Button(window, text="Cause Destruction", command=increase_points, font=("Comic Sans", 14), bg="#D3FC03", fg="#FF004C", activebackground="#FEB201")
click_button.pack(pady=10)

upgrade_button = tk.Button(window, text=f"Upgrade ({unlock_threshold})", command=upgrade_action, font=("Comic Sans", 14), bg="#00FFD0", fg="#00A088", activeforeground="#FF0000")
upgrade_button.pack(pady=10)

autoclicker = tk.Button(window, text=f"Buy Worker Drone to work for you bcuz ur lazy ({auto_clicker_cost})", command=buy_auto_clicker, font=("Comic Sans", 14), bg="#FF6EFF", fg="#000000", activeforeground="#FFFFFF")
autoclicker.pack(pady=10)

save_button = tk.Button(window, text="Save Progress", command=save_progress, font=("Comic Sans", 14), bg="#A3FFB0", fg="#000000", activebackground="#77FF9E")
save_button.pack(pady=10)

load_button = tk.Button(window, text="📂 Load Progress", command=load_progress, font=("Comic Sans", 14), bg="#B0D8FF", fg="#000000", activebackground="#78BCFF")
load_button.pack(pady=10)

reset_button = tk.Button(window, text="❌ Reset Game", command=reset_game, font=("Comic Sans", 14), bg="#FFB0B0", fg="#000000", activebackground="#FF7A7A")
reset_button.pack(pady=10)

def on_closing():
    save_progress()
    window.destroy()
    os._exit(0)

window.configure(bg="#007BFF")
window.after(1000, auto_click)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
