import tkinter as tk
from tkinter import messagebox
from pynput.keyboard import Controller
import threading
import time
import random

keyboard = Controller()
typingActive = False
loopTyping = False

# --- Auto-Typing Function ---
def calculate_delay_per_char(wpm, device="computer"):
    """Calculate delay per character based on WPM and device type."""
    base_delay = 60 / (wpm * 5)  # 5 chars per word
    if device == "phone":
        base_delay *= 1.4  # slower for phone-like behavior
    return max(base_delay, 0.02)  # minimum 20ms per char

def auto_type_text(text, wpm=100, accuracy=95, device="computer"):
    global typingActive
    delay = calculate_delay_per_char(wpm, device)
    while typingActive:
        for char in text:
            if not typingActive:
                return
            # simulate typo based on accuracy
            if random.randint(0,100) > accuracy:
                wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
                keyboard.type(wrong_char)
                keyboard.press('\b')
                keyboard.release('\b')
                time.sleep(delay*2)
            keyboard.type(char)
            time.sleep(delay)
        if not loopTyping:
            typingActive = False
            break
        else:
            time.sleep(int(delay*10))  # short delay before looping

# --- GUI Handlers ---
def start_typing():
    global typingActive, loopTyping
    text = text_box.get("1.0", tk.END).rstrip()
    if not text:
        messagebox.showwarning("No Text", "Please enter text to auto-type.")
        return
    try:
        wpm = int(wpm_entry.get())
        acc = int(accuracy_entry.get())
        loopTyping = loop_var.get()
        device = device_var.get()
    except:
        messagebox.showerror("Error", "Invalid settings")
        return

    typingActive = True
    messagebox.showinfo("Get Ready", "Switch to the window where you want text typed. Typing starts in 3 seconds...")
    time.sleep(3)
    threading.Thread(target=auto_type_text, args=(text,wpm,acc,device), daemon=True).start()

def stop_typing():
    global typingActive
    typingActive = False

# --- GUI Setup ---
root = tk.Tk()
root.title("PC AutoTyper")

tk.Label(root, text="Paste your text below:").pack()
text_box = tk.Text(root, height=10, width=50)
text_box.pack(pady=5)

tk.Label(root, text="Typing speed (WPM)").pack()
wpm_entry = tk.Entry(root)
wpm_entry.insert(0,"100")
wpm_entry.pack(pady=2)

tk.Label(root, text="Typing accuracy (0-100%)").pack()
accuracy_entry = tk.Entry(root)
accuracy_entry.insert(0,"95")
accuracy_entry.pack(pady=2)

tk.Label(root, text="Device type").pack()
device_var = tk.StringVar(value="computer")
tk.OptionMenu(root, device_var, "computer", "phone").pack(pady=2)

loop_var = tk.BooleanVar()
tk.Checkbutton(root, text="Loop typing", variable=loop_var).pack(pady=2)

tk.Button(root, text="Start Auto Typing", command=start_typing).pack(pady=10)
tk.Button(root, text="Stop Typing", command=stop_typing).pack(pady=5)

root.mainloop()
