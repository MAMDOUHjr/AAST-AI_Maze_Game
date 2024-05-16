import tkinter as tk
from tkinter import ttk
import subprocess

def run_developer_mode():
    subprocess.Popen(["python", "developermode.py"])

def run_1_vs_1():
    subprocess.Popen(["python", "TEST6FORMINUE.py"])


root = tk.Tk()
root.title("Main Page")
root.geometry("400x300")
root.configure(bg="#1F2833")  


def create_button(text, command, y):
    button = ttk.Button(root, text=text, width=30,padding=15 ,command=command, style="Main.TButton")
    button.place(relx=0.5, rely=y, anchor="center")


style = ttk.Style()
style.configure("Main.TButton", foreground="black", background="#0B0C10", font=("comforta", 12, "bold"))


create_button("Generate a Maze (Developer Mode)", run_developer_mode, 0.4)
create_button("Play 1 vs 1", run_1_vs_1, 0.6)


root.mainloop()
