#waiting for scrape

import tkinter as tk
import random
import sys
import os
from PIL import Image, ImageTk

# --- Safe resource path for PyInstaller ---
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

window = tk.Tk()
window.title("Mars Corn")
window.geometry("900x700")

points = 0
activeMultiplier = 1
unlock_threshold = 10

auto_clickers = 0
auto_clicker_cost = 500

label = tk.Label(window, text="Points: 0", font=("Comic Sans", 16))
label.pack(pady=20)

status_label = tk.Label(window, text=f"Multiplier: {activeMultiplier} | Auto-Clickers: {auto_clickers}", font=("Comic Sans", 12))
status_label.pack(pady=5)

cursor_frame = tk.Frame(window, bg="#007BFF", height=50)
cursor_frame.pack(pady=5)
cursors = []

cursor_canvas = tk.Canvas(window, width=900, height=100, bg="#007BFF", highlightthickness=0)
cursor_canvas.pack(pady=10)
cursor_sprites = []

# --- Try to load cursor.png safely ---
cursor_img = None
try:
    cursor_path = resource_path("cursor.png")
    print("Loading image from:", cursor_path)
    cursor_img_raw = Image.open(cursor_path).resize((32, 32))
    cursor_img = ImageTk.PhotoImage(cursor_img_raw)
    window.cursor_img = cursor_img  # prevent garbage collection
except Exception as e:
    print("⚠️ Failed to load cursor.png. Falling back to emoji.")
    print(e)
    cursor_img = None

def increase_points():
    global points
    crit = random.random() < 0.1
    gain = activeMultiplier * (5 if crit else 1)
    points += gain
    label.config(text=f"Points: {points}")
    status_label.config(text=f"Multiplier: {activeMultiplier} | Auto-Clickers: {auto_clickers}")
    if crit:
        print("You caused a lot of chaos young human...")

def upgrade_action():
    global activeMultiplier, points, unlock_threshold 
    if points >= unlock_threshold:
        points -= unlock_threshold
        activeMultiplier += 1
        unlock_threshold += 10
        label.config(text=f"Points: {points}")
        upgrade_button.config(text=f"Upgrade (costs {unlock_threshold})")
        status_label.config(text=f"Multiplier: {activeMultiplier} | Auto-Clickers: {auto_clickers}")
        print("You wasted your money lol")

def buy_auto_clicker():
    global points, auto_clickers, auto_clicker_cost
    if points >= auto_clicker_cost:
        points -= auto_clicker_cost
        auto_clickers += 1
        auto_clicker_cost += 25
        label.config(text=f"Points: {points}")
        autoclicker.config(text=f"We raised our prices! AutoClicker now costs {auto_clicker_cost} Press this button to buy Autoclicker again")
        status_label.config(text=f"Multiplier: {activeMultiplier} | Auto-Clickers: {auto_clickers}")
        
        if cursor_img:
            x = 50 + (auto_clickers - 1) * 40
            y = 10
            sprite_id = cursor_canvas.create_image(x, y, image=cursor_img)
            cursor_sprites.append((sprite_id, x, y))
        else:
            cursor = tk.Label(cursor_frame, text="🖱️", font=("Comic Sans", 20), bg="#007BFF")
            cursor.pack(side="left", padx=5)
            cursors.append(cursor)

def animate_cursor_clicks():
    for sprite_id, x, y in cursor_sprites:
        cursor_canvas.move(sprite_id, 0, 20)
    window.after(150, reset_cursor_positions)

def reset_cursor_positions():
    for sprite_id, x, y in cursor_sprites:
        cursor_canvas.coords(sprite_id, x, y)

def auto_click():
    global points
    if auto_clickers > 0:
        points += auto_clickers
        label.config(text=f"Points: {points}")
        status_label.config(text=f"Multiplier: {activeMultiplier} | Auto-Clickers: {auto_clickers}")
        animate_cursor_clicks()
    window.after(1000, auto_click)

click_button = tk.Button(window, text="Cause Destruction", command=increase_points, font=("Comic Sans", 14))
click_button.pack(pady=10)

upgrade_button = tk.Button(window, text=f"Upgrade (costs {unlock_threshold})", command=upgrade_action, font=("Comic Sans", 14))
upgrade_button.pack(pady=10)

autoclicker = tk.Button(window, text="Buy Worker Drone to work for u bcuz ur lazy human (costs a lot of money totally not 500)", command=buy_auto_clicker, font=("Comic Sans", 14))
autoclicker.pack(pady=10)

window.configure(bg="#007BFF")
label.config(bg="#FF00EA", fg="#00FF1E")
status_label.config(bg="#FF00EA", fg="#000000")
click_button.config(bg="#D3FC03", fg="#FF004C", activebackground="#FEB201")
upgrade_button.config(bg="#00FFD0", fg="#00A088", activeforeground="#FF0000")
autoclicker.config(bg="#FF6EFF", fg="#000000", activeforeground="#FFFFFF")

window.after(1000, auto_click)
window.mainloop()
