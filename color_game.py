import tkinter as tk
import random
import colorgenerate as cg

# Game settings
GAME_TIME = 30
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 620
BUTTON_AREA_SIZE = 420
MAX_WRONG = 3

score = 0
wrong_count = 0
time_left = GAME_TIME
timer_running = False
game_paused = False
game_mode = None  # 'time' or 'mistake'

round_history = []         # list: stores round details
round_summary = {}         # dictionary: stores game summary

# Determine grid size and color similarity based on score
def get_grid_size(score):
    if score < 5:
        grid = 3
    elif score < 10:
        grid = 4
    else:
        grid = 5

    factor = 1.5 - min(score * 0.03, 0.45)
    if random.random() < 0.5:
        factor = 2 - factor

    return grid, factor

# Check if the clicked button is correct
def check_answer(index, special_index):
    global score, wrong_count, timer_running
    if not timer_running or game_paused:
        return

    result = {"round": len(round_history)+1, "clicked_index": index, "special_index": special_index}

    if index == special_index:
        score += 1
        result["result"] = "correct"
        result["score"] = score
        score_label.config(text=f"Score: {score}")
        round_history.append(result)
        root.after(100, start_game)
    else:
        result["result"] = "wrong"
        result["score"] = score
        round_history.append(result)
        if game_mode == "mistake":
            wrong_count += 1
            mistake_label.config(text=f"❌ {wrong_count}/{MAX_WRONG}")
            if wrong_count >= MAX_WRONG:
                end_game("Too many wrong answers!")

# Start a new round of the game
def start_game():
    if not timer_running or game_paused:
        return

    for widget in button_frame.winfo_children():
        widget.destroy()

    grid_size, factor = get_grid_size(score)
    total_buttons = grid_size ** 2

    base_hex, base_rgb = cg.generate_color()
    special_hex = cg.adjust_brightness(base_rgb, factor)
    special_index = random.randint(0, total_buttons - 1)

    btn_size = BUTTON_AREA_SIZE // grid_size - 8

    for row in range(grid_size):
        for col in range(grid_size):
            i = row * grid_size + col
            color = special_hex if i == special_index else base_hex
            btn = tk.Button(
                button_frame,
                width=btn_size // 8,
                height=btn_size // 16,
                bg=color,
                command=lambda i=i: check_answer(i, special_index),
                relief="flat",
                bd=0
            )
            btn.place(
                x=col * (btn_size + 8) + 4,
                y=row * (btn_size + 8) + 4,
                width=btn_size,
                height=btn_size
            )

# Update countdown timer
def update_timer():
    global time_left
    if game_mode == "time" and timer_running and not game_paused:
        if time_left > 0:
            time_left -= 1
            timer_label.config(text=f"{time_left}")
            root.after(1000, update_timer)
        else:
            end_game("Time's up!")

# End the game and show results
def end_game(message):
    global timer_running
    timer_running = False

    for widget in button_frame.winfo_children():
        widget.destroy()

    correct_count = sum(1 for r in round_history if r.get("result") == "correct")
    wrong_count_local = sum(1 for r in round_history if r.get("result") == "wrong")

    round_summary["total_rounds"] = len(round_history)
    round_summary["correct"] = correct_count
    round_summary["wrong"] = wrong_count_local

    print("=== Game Summary ===")
    print(round_summary)

    game_over_frame = tk.Frame(button_frame, bg="white", relief="solid", bd=2)
    game_over_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(game_over_frame, text="Game Over!", font=("Arial", 28, "bold"), bg="white", fg="#333333").pack(pady=20)
    tk.Label(game_over_frame, text=f"Final Score: {score}", font=("Arial", 22), bg="white", fg="#333333").pack(pady=10)

    restart_btn = tk.Button(
        game_over_frame,
        text="Play Again",
        font=("Arial", 16, "bold"),
        bg="#FF9900",
        fg="white",
        command=show_mode_selection,
        relief="flat",
        bd=0,
        padx=20,
        pady=10
    )
    restart_btn.pack(pady=20)

# Toggle pause
def toggle_pause():
    global game_paused
    if timer_running:
        game_paused = not game_paused
        if game_paused:
            pause_btn.config(text="▶")
            pause_overlay = tk.Frame(button_frame, bg="#f0f0f0", relief="solid", bd=1)
            pause_overlay.place(x=0, y=0, width=BUTTON_AREA_SIZE, height=BUTTON_AREA_SIZE)
            pause_overlay.tag = "pause_overlay"
            tk.Label(pause_overlay, text="PAUSED", font=("Arial", 36, "bold"), bg="#f0f0f0", fg="#333333").place(relx=0.5, rely=0.5, anchor="center")
        else:
            pause_btn.config(text="॥")
            for widget in button_frame.winfo_children():
                if hasattr(widget, 'tag') and widget.tag == "pause_overlay":
                    widget.destroy()
            if game_mode == "time":
                update_timer()

# Start game with selected mode
def start_mode(selected_mode):
    global game_mode, timer_running, score, time_left, wrong_count, game_paused, round_history
    game_mode = selected_mode
    timer_running = True
    game_paused = False
    score = 0
    wrong_count = 0
    time_left = GAME_TIME
    round_history.clear()

    mode_frame.pack_forget()
    top_frame.pack(fill="x", pady=10)
    button_frame.pack(pady=5)
    score_label.config(text=f"Score: {score}")

    if game_mode == "mistake":
        mistake_label.config(text=f"❌ 0/{MAX_WRONG}")
        mistake_label.pack(side="right", padx=20)
        timer_label.place_forget()
    else:
        mistake_label.pack_forget()
        timer_label.place(relx=0.5, rely=0.5, anchor="center")
        timer_label.config(text=f"{GAME_TIME}")
        update_timer()

    pause_btn.config(text="॥")
    start_game()

# Show mode selection screen
def show_mode_selection():
    top_frame.pack_forget()
    button_frame.pack_forget()
    mode_frame.pack(pady=100)

# Main window setup
root = tk.Tk()
root.title("Bet U can't see")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.configure(bg="#f8f8f8")
root.resizable(False, False)

# Mode selection screen
mode_frame = tk.Frame(root, bg="#f8f8f8")
mode_frame.pack(pady=100)

title_label = tk.Label(mode_frame, text="Bet U Can't See", font=("Arial", 28, "bold"), bg="#f8f8f8", fg="#333333")
title_label.pack(pady=10)

mode_label = tk.Label(mode_frame, text="Select Game Mode", font=("Arial", 18), bg="#f8f8f8", fg="#555555")
mode_label.pack(pady=20)

time_mode_btn = tk.Button(mode_frame, text="🕒 Timed Mode", font=("Arial", 16, "bold"), bg="#FF9900", fg="white", command=lambda: start_mode("time"), relief="flat", bd=0, padx=20, pady=10, width=20)
time_mode_btn.pack(pady=5)

mistake_mode_btn = tk.Button(mode_frame, text="❌ Mistake Mode", font=("Arial", 16, "bold"), bg="#FF6666", fg="white", command=lambda: start_mode("mistake"), relief="flat", bd=0, padx=20, pady=10, width=20)
mistake_mode_btn.pack(pady=5)
# Top info bar
top_frame = tk.Frame(root, bg="#f8f8f8")

score_label = tk.Label(top_frame, text="Score: 0", font=("Arial", 20, "bold"), bg="#f8f8f8", fg="#555555")
score_label.pack(side="left", padx=20)

mistake_label = tk.Label(top_frame, text=f"❌ 0/{MAX_WRONG}", font=("Arial", 16), bg="#f8f8f8", fg="#FF5555")

timer_label = tk.Label(top_frame, text=f"{time_left}", font=("Arial", 18, "bold"), bg="#FF9999", fg="white", padx=10, pady=5)

pause_btn = tk.Button(top_frame, text="॥", font=("Arial", 15, "bold"), bg="#FFCC66", fg="white", command=toggle_pause, relief="flat", bd=0, padx=10, pady=5)
pause_btn.pack(side="right", padx=45)

# Game area
button_frame = tk.Frame(root, width=BUTTON_AREA_SIZE, height=BUTTON_AREA_SIZE, bg="#e8e8e8", bd=0)

# Launch mode selection screen
show_mode_selection()

# Start main event loop
root.mainloop()