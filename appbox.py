# example: define build_ui(root) to create widgets inside the provided container.
# you may import modules if you need them, e.g. from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

def build_ui(root):
    # root is a frame managed by the designer. create widgets inside it.
    FEEDFRAME = tk.Frame(root)
    POSTFRAME = tk.Frame(root)
    
    # left 66%
    FEEDFRAME.place(relx=0, rely=0, relwidth=0.66, relheight=1)
    # right 33%
    POSTFRAME.place(relx=0.66, rely=0, relwidth=0.34, relheight=1)

    FEEDSCROLLcontainer = tk.Frame(FEEDFRAME)
    FEEDSCROLLcontainer.pack(fill="both", expand=True)
    FEEDSCROLLcanvas = tk.Canvas(FEEDSCROLLcontainer)
    FEEDSCROLLscroller = tk.Scrollbar(FEEDSCROLLcontainer)    
    FEEDSCROLLframe = tk.Frame(FEEDSCROLLcanvas)
    FEEDSCROLLwind = FEEDSCROLLcanvas.create_window((0, 0), window=FEEDSCROLLframe, anchor="nw")
    FEEDSCROLLcanvas.configure(yscrollcommand=FEEDSCROLLscroller.set)

    def _onMouseWheel(event):
        FEEDSCROLLcanvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def _updateScrollRegion(event):
        FEEDSCROLLcanvas.configure(scrollregion=FEEDSCROLLcanvas.bbox("all"))
    def onCanvasConfigure(event):
        FEEDSCROLLcanvas.itemconfig(FEEDSCROLLwindow, width=event.width)

    FEEDSCROLLcanvas.bind("<Configure>", onCanvasConfigure)

    FEEDSCROLLcanvas.bind_all("<MouseWheel>", _onMouseWheel)
    FEEDSCROLLframe.bind("<Configure>", _updateScrollRegion)
    FEEDSCROLLcanvas.pack(side="left", fill="both", anchor="nw")
    FEEDSCROLLscroller.pack(side="right",fill="y")
    # FEEDSCROLLframe.pack() <- FUCKASS LINE THAT KILLS YOUR CODE!!!! EVIL!!!! DO NOT USE!!!!
    
    """
    # placeholder subframes
    for i in range(2):
        sub = tk.Frame(FEEDSCROLLframe, bg=f"#FFFFaa", bd=2, relief="ridge")
        sub.pack(fill="x", pady=5, padx=5)
        tk.Label(sub, text=f"frame {i}", bg=sub["bg"]).pack(side="left", padx=10)
        tk.Button(sub, text="click").pack(side="right", padx=10)
    """

    #----------------sidebar time!!!----------------#
    INFOFRAME = tk.Frame(POSTFRAME)
    WRITERFRAME = tk.Frame(POSTFRAME, bg="purple")
    # left 66%
    INFOFRAME.place(relx=0, rely=0, relwidth=1, relheight=0.66)
    # right 33%
    WRITERFRAME.place(rely=0.66, relwidth=1, relheight=0.34)
    #-------------------info bar--------------------#
    INFOUSERTEXT = tk.Label(INFOFRAME, text="@placeholder.bsky.app")
    INFOUSERTEXT.pack(anchor="w", side="top")
    INFOFOLLOWERTEXT = tk.Label(INFOFRAME, text="1 bajillion followers")
    INFOFOLLOWERTEXT.pack(anchor="w", side="top")
    INFOFOLLOWINGTEXT = tk.Label(INFOFRAME, text="1 follow")
    INFOFOLLOWINGTEXT.pack(anchor="w", side="top")
    INFOPOSTSTEXT = tk.Label(INFOFRAME, text="36K posts")
    INFOPOSTSTEXT.pack(anchor="w", side="top")
    #-------------------post bar--------------------#
    WRITERCONTAINER = tk.Frame(WRITERFRAME, 
# bg="white",
relief="sunken", 
highlightbackground="grey", 
highlightcolor="grey", 
highlightthickness=2
)
    WRITERCONTAINER.pack(fill="both", expand=True)
    WRITERFOOTERRACK = tk.Frame(WRITERCONTAINER)
    WRITERFOOTERRACK.pack(fill="x", side="bottom")
    WRITERPOSTBUTTON = tk.Button(WRITERFOOTERRACK, text="Post")
    WRITERPOSTBUTTON.pack(side="right", padx=5,pady=5)
    WRITERBOX = tk.Text(WRITERCONTAINER)
    WRITERBOX.pack(fill="both", expand=True)
    WRITERREMAININGCHARA = tk.Label(WRITERFOOTERRACK, text="-1984", fg="red")
    WRITERREMAININGCHARA.pack(side="left", padx=5)