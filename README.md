# Python AutoTyper

Python AutoTyper with GUI, adjustable WPM, accuracy, and optional loop typing. Auto-types text like a human into any application.

---

## 1. Prerequisites

- Python 3.11.9 or later (Windows, Linux, Mac)
- `pynput` library for keyboard simulation
- `tkinter` (built-in with Python)

---

## 2. Install Required Library

```bash
pip install pynput
```
---

## 3. How to Use
1. Paste the text you want to auto-type in the text box.

2. Set WPM (words per minute, e.g., 100).

3. Set Accuracy (0-100%, e.g., 95).

4. Select Device type:

5. computer – faster typing

6. phone – slower, safer typing

7. Check Loop typing if you want it repeated.

8. Click Start Auto Typing and switch to the target window. Typing begins automatically after 3 seconds.

9. Click Stop Typing to stop anytime.
---

## Using Without Python (EXE version)
If you want to use the AutoTyper without installing Python, you can convert the script to a standalone executable using **PyInstaller**.

## Convert Your Script to EXE
1. Open Command Prompt
2. Navigate to your project folder:
```bash
cd C:\Users\YourName\Documents\AutoTyper
```
3. Run PyInstaller:
```bash
pyinstaller --onefile --windowed auto_typer.py
```


