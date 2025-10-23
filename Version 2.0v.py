import tkinter as tk
from tkinter import messagebox
from pynput.keyboard import Controller, Key
import threading
import time
import random
import json

# ------------------- Globals -------------------
keyboard = Controller()
typing_active = False
stats_window = None
session_data = []
scheduler_list = []

# ------------------- Typing Settings -------------------
settings = {
    "wpm": 100,
    "accuracy": 95,
    "device": "computer",  # computer or phone
    "loop": False,
    "start_delay": 3  # seconds before typing starts
}

# ------------------- Helper Functions -------------------
def calculate_ms_per_char(wpm, device):
    base = 12000 / max(1, wpm)  # 5 chars per word
    if device == "phone":
        base *= 1.4
    return max(base, 25)

def random_typo(c):
    char = c
    while char == c:
        char = chr(random.randint(32, 125))
    return char

def type_text(text):
    global typing_active, session_data
    ms_per_char = calculate_ms_per_char(settings["wpm"], settings["device"])
    correct_chars = 0
    total_chars = len(text)

    for i, c in enumerate(text):
        if not typing_active:
            break
        if c == '\n':
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(ms_per_char / 1000)
            continue

        # Decide typo
        make_typo = random.randint(0, 100) >= settings["accuracy"]
        if make_typo:
            wrong_char = random_typo(c)
            keyboard.type(wrong_char)
            time.sleep(ms_per_char / 1000 * 2)
            keyboard.press(Key.backspace)
            keyboard.release(Key.backspace)
            time.sleep(0.08)
        keyboard.type(c)
        if not make_typo:
            correct_chars += 1
        time.sleep(ms_per_char / 1000)
        update_stats(i+1, total_chars, correct_chars)

    # Save session
    session_data.append({
        "text": text,
        "wpm": settings["wpm"],
        "accuracy": round((correct_chars/total_chars)*100 if total_chars>0 else 0,2),
        "timestamp": time.time()
    })

def start_typing_thread(text):
    global typing_active
    def delayed_start():
        time.sleep(settings["start_delay"])
        while typing_active:
            type_text(text)
            if not settings["loop"]:
                break
    typing_active = True
    threading.Thread(target=delayed_start, daemon=True).start()

def stop_typing():
    global typing_active
    typing_active = False

# ------------------- Stats Window -------------------
def create_stats_window():
    global stats_window
    if stats_window is not None:
        return
    stats_window = tk.Toplevel()
    stats_window.title("Typing Stats")
    stats_window.geometry("250x100+1000+500")
    stats_window.attributes("-topmost", True)
    stats_window.protocol("WM_DELETE_WINDOW", lambda: None)
    stats_window.resizable(False, False)

    stats_window.label = tk.Label(stats_window, text="WPM: 0 | Accuracy: 0%")
    stats_window.label.pack(padx=10, pady=10)

def update_stats(progress, total, correct):
    if stats_window:
        wpm = settings["wpm"]
        acc = round((correct/total)*100 if total>0 else 0,2)
        stats_window.label.config(text=f"Progress: {progress}/{total}\nWPM: {wpm} | Accuracy: {acc}%")
        stats_window.update()

# ------------------- Scheduler -------------------
def add_to_scheduler(text, delay_sec):
    scheduler_list.append((text, delay_sec))
    messagebox.showinfo("Scheduler", f"Text added to scheduler with {delay_sec}s delay")

def run_scheduler():
    global scheduler_list, typing_active
    for text, delay_sec in scheduler_list:
        if not typing_active:
            break
        messagebox.showinfo("Scheduler", f"Typing next text in {delay_sec} seconds")
        time.sleep(delay_sec)
        if typing_active:
            type_text(text)
    messagebox.showinfo("Scheduler", "All scheduled texts completed.")

def start_scheduler_thread():
    threading.Thread(target=run_scheduler, daemon=True).start()

# ------------------- GUI -------------------
root = tk.Tk()
root.title("Python AutoTyper")
root.geometry("650x650")

# ---------- Text Box ----------
tk.Label(root, text="Text to Auto-Type:").pack(pady=(10,0))
text_box = tk.Text(root, height=10, width=70)
text_box.pack(padx=10, pady=(0,10))

# ---------- Settings Frame ----------
settings_frame = tk.Frame(root)
settings_frame.pack(pady=10, fill="x", padx=10)

tk.Label(settings_frame, text="WPM:").grid(row=0, column=0, padx=5, sticky="w")
wpm_entry = tk.Entry(settings_frame, width=5)
wpm_entry.insert(0, str(settings["wpm"]))
wpm_entry.grid(row=0, column=1, padx=5)

tk.Label(settings_frame, text="Accuracy:").grid(row=0, column=2, padx=5, sticky="w")
acc_entry = tk.Entry(settings_frame, width=5)
acc_entry.insert(0, str(settings["accuracy"]))
acc_entry.grid(row=0, column=3, padx=5)

tk.Label(settings_frame, text="Device:").grid(row=0, column=4, padx=5, sticky="w")
device_var = tk.StringVar(value=settings["device"])
tk.OptionMenu(settings_frame, device_var, "computer", "phone").grid(row=0, column=5, padx=5)

loop_var = tk.BooleanVar(value=settings["loop"])
tk.Checkbutton(settings_frame, text="Loop Typing", variable=loop_var).grid(row=0, column=6, padx=5)

tk.Label(settings_frame, text="Start Delay (s):").grid(row=1, column=0, padx=5, sticky="w")
delay_entry = tk.Entry(settings_frame, width=5)
delay_entry.insert(0, str(settings["start_delay"]))
delay_entry.grid(row=1, column=1, padx=5)

# ---------- Buttons Frame ----------
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

tk.Button(buttons_frame, text="Start Auto Typing", width=20, command=lambda: start_typing_thread(text_box.get("1.0", "end-1c"))).grid(row=0, column=0, padx=5, pady=5)
tk.Button(buttons_frame, text="Stop Typing", width=20, command=stop_typing).grid(row=0, column=1, padx=5, pady=5)
tk.Button(buttons_frame, text="Show Stats Widget", width=20, command=create_stats_window).grid(row=1, column=0, padx=5, pady=5)
tk.Button(buttons_frame, text="Save Session Data", width=20, command=lambda: json.dump(session_data, open("typing_sessions.json","w"))).grid(row=1, column=1, padx=5, pady=5)

# ---------- Scheduler Section ----------
tk.Label(root, text="Scheduler (text + delay in sec)").pack(pady=(20,5))
sched_text = tk.Text(root, height=5, width=70)
sched_text.pack(padx=10)

sched_buttons_frame = tk.Frame(root)
sched_buttons_frame.pack(pady=5)
tk.Button(sched_buttons_frame, text="Add to Scheduler (5s delay)", width=25, command=lambda: add_to_scheduler(sched_text.get("1.0","end-1c"),5)).grid(row=0, column=0, padx=5, pady=5)
tk.Button(sched_buttons_frame, text="Start Scheduler", width=25, command=start_scheduler_thread).grid(row=0, column=1, padx=5, pady=5)

root.mainloop()
