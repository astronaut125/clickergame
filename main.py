#still evading the law

import tkinter as tk

window = tk.Tk()
window.title("MaliciousProgramTotallyNotHacking.exe")
window.geometry("300x300")

points = 0
activeMultiplier = 1
unlock_threshold = 10

auto_clickers = 0
auto_clicker_cost = 5

label = tk.Label(window, text="Points: 0", font=("Comic Sans", 16))
label.pack(pady=20)

#Slabel to show multiplier and auto-clickers
status_label = tk.Label(window, text=f"Multiplier: {activeMultiplier} | Auto-Clickers: {auto_clickers}", font=("Comic Sans", 12))
status_label.pack(pady=5)

def increase_points():
    global points
    points += 1 * activeMultiplier
    label.config(text=f"Points: {points}")
    #Update label when clicking
    status_label.config(text=f"Multiplier: {activeMultiplier} | Auto-Clickers: {auto_clickers}")

def upgrade_action():
    global activeMultiplier, points, unlock_threshold 
    if points >= unlock_threshold:
        points -= unlock_threshold
        activeMultiplier += 1
        label.config(text=f"Points: {points}")
        unlock_threshold += 10
        upgrade_button.config(text=f"Upgrade (costs {unlock_threshold})")
        #Update label after upgrading
        status_label.config(text=f"Multiplier: {activeMultiplier} | Auto-Clickers: {auto_clickers}")
        print("You wasted your money lol")

def buy_auto_clicker():
    global points, auto_clickers, auto_clicker_cost
    if points >= auto_clicker_cost:
        points -= auto_clicker_cost
        auto_clickers += 1
        label.config(text=f"Points: {points}")
        auto_clicker_cost += 25
        autoclicker.config(text=f"We raised our prices! AutoClicker now costs {auto_clicker_cost} Press this button to buy Autoclicker again")
        #Update label after buying auto-clicker
        status_label.config(text=f"Multiplier: {activeMultiplier} | Auto-Clickers: {auto_clickers}")

def auto_click():
    global points
    if auto_clickers > 0:
        points += auto_clickers
        label.config(text=f"Points: {points}")
        #Update auto click status
        status_label.config(text=f"Multiplier: {activeMultiplier} | Auto-Clickers: {auto_clickers}")
    window.after(1000, auto_click)

click_button = tk.Button(window, text="Cause Destruction", command=increase_points, font=("Comic Sans", 14))
click_button.pack(pady=10)

# Upgrade button label to tell truth
upgrade_button = tk.Button(window, text=f"Upgrade (costs {unlock_threshold})", command=upgrade_action, font=("Comic Sans", 14))
upgrade_button.pack(pady=10)

autoclicker = tk.Button(window, text="Buy Worker Drone to work for u bcuz ur lazy human (costs a lot of money totally)", command=buy_auto_clicker, font=("Comic Sans", 14))
autoclicker.pack(pady=10)

#colors
window.configure(bg="#007BFF")
label.config(bg="#FF00EA", fg="#00FF1E")
#color for the new label
status_label.config(bg="#FF00EA", fg="#000000")
click_button.config(bg="#D3FC03", fg="#FF004C", activebackground="#FEB201")
upgrade_button.config(bg="#00FFD0", fg="#00A088", activeforeground="#FF0000")
autoclicker.config(bg="#FF6EFF", fg="#000000", activeforeground="#FFFFFF")

window.after(1000, auto_click)
window.mainloop()