# define build_ui(root) to create widgets inside the given container
import tkinter as tk
from tkinter import ttk

def build_ui(root):

    LOGINPOPUP = tk.Toplevel(root)
    LOGINPOPUP.title("LOGIN")
    # LOGINPOPUP = tk.Frame(root)
    # LOGINPOPUP.pack()

    LOGINPASS = ttk.Entry(LOGINPOPUP, show="*")
    LOGINUSER = ttk.Entry(LOGINPOPUP)
    LOGINPASSLABEL = ttk.Label(LOGINPOPUP, text="password:")
    LOGINUSERLABEL = ttk.Label(LOGINPOPUP, text="username:")
    LOGINLABEL = ttk.Label(LOGINPOPUP, text="log into bluesky:")
    LOGINLABEL.pack(padx=5,pady=5)
    LOGINUSERLABEL.pack()
    LOGINUSER.pack()
    LOGINPASSLABEL.pack()
    LOGINPASS.pack()
    LOGINBUTTON = ttk.Button(LOGINPOPUP, text="login")
    LOGINBUTTON.pack()