# example: define build_ui(root) to create widgets inside the provided container.
# you may import modules if you need them, e.g. from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

def build_ui(root):
    # root is a frame managed by the designer. create widgets inside it.
    POSTFRAME = tk.Frame(root,
highlightbackground="grey",
highlightcolor="grey",
highlightthickness=2)
    USERlabel = ttk.Label(POSTFRAME, text="placeholder")
    HANDLElabel = ttk.Label(POSTFRAME, text="@doctorplaceholder.bsky.app")
    USERlabel.pack(anchor="nw", padx=10)
    HANDLElabel.pack(anchor="n", padx=10)
    POSTCONTENTmessage = tk.Message(POSTFRAME, text="long text long long text\nnewlines\ni love newlines\nlong text long long text wowie", 
highlightbackground="grey",
highlightcolor="grey",
highlightthickness=2,
aspect="300"
)
    POSTCONTENTmessage.pack(anchor="center")
    INTERACTFRAME = tk.Frame(POSTFRAME)
    LIKEBUTTON = tk.Button(INTERACTFRAME, anchor="center", text="\U0001f90d")
    REPOSTBUTTON = tk.Button(INTERACTFRAME, anchor="e", text="\U0001F504")
    REPLYBUTTON = tk.Button(INTERACTFRAME, anchor="w", text="\U0001f4ac")
    LIKEBUTTON.pack(side="left", padx=10)
    REPOSTBUTTON.pack(side="left", padx=10)
    REPLYBUTTON.pack(side="left", padx=10)
    OTHERMENU = tk.Menu(INTERACTFRAME, tearoff=0)
    OTHERMENU.add_command(label="Share")
    OTHERMENU.add_command(label="Copy Post Text")
    OTHERMENU.add_separator()
    OTHERMENU.add_command(label="Follow User")
    OTHERMENU.add_separator()
    OTHERMENU.add_command(label="Hide Post")
    OTHERMENU.add_command(label="Block User")
    
    def showOtherMenu():
        x = OTHERMENUbutton.winfo_rootx()
        y = OTHERMENUbutton.winfo_rooty() + OTHERMENUbutton.winfo_height()
        OTHERMENU.tk_popup(x, y)
    
    OTHERMENUbutton = tk.Button(INTERACTFRAME,
text="\U000022ef",
relief="raised",
command=showOtherMenu)
    OTHERMENUbutton.pack(side="left", padx=10)
    INTERACTFRAME.pack()
    POSTFRAME.pack()



