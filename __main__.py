import webbrowser
import atproto
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import post
import utils

CLIENT = atproto.Client()
CLIENTPROFILE = None

LOGINPOPUP = tk.Tk()
LOGINPOPUP.title("LOGIN")
# LOGINPOPUP = tk.Frame(root)
# LOGINPOPUP.pack()

def setupClient(username, password):
    global CLIENT
    global CLIENTPROFILE
    CLIENTPROFILE = CLIENT.login(username, password)
    # print(CLIENTPROFILE)

def trySetupClient():
    try:
        setupClient(LOGINUSER.get(), LOGINPASS.get())
        LOGINPOPUP.destroy()
    except Exception as e:
        messagebox.showwarning("error", str(e))

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
LOGINBUTTON = ttk.Button(LOGINPOPUP, text="login", command=trySetupClient)
LOGINBUTTON.pack()

LOGINPOPUP.mainloop()

print("login successful")
print(CLIENTPROFILE.display_name)
utils.CLIENT = CLIENT


#----------------MAIN UI (COPIED FROM appbox.py)------------------#
root = tk.Tk()
root.geometry("800x600")
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
FEEDSCROLLwindow = FEEDSCROLLcanvas.create_window((0, 0), window=FEEDSCROLLframe, anchor="nw")
FEEDSCROLLcanvas.configure(yscrollcommand=FEEDSCROLLscroller.set)

def checkScroll():
    start, end = FEEDSCROLLcanvas.yview()
    if end == 1.0:
        global TIMELINE
        if TIMELINE.cursor == None:
            messagebox.showwarning("feed error", "you've reached the end of your feed!")
        timeline = CLIENT.app.bsky.feed.get_timeline(params={"cursor": TIMELINE.cursor})
        for item in TIMELINE.feed:
            POSTS.append(post.Post(FEEDSCROLLframe, item, utils.Utils))
            POSTS[-1].getFrame().pack(fill="x", pady=5, padx=5)
def _onMouseWheel(event):
    FEEDSCROLLcanvas.yview_scroll(int(-1*(event.delta/120)), "units")
    checkScroll()
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
for i in range(100):
    sub = tk.Frame(FEEDSCROLLframe, bg=f"#FFFFaa", bd=2, relief="ridge")
    sub.pack(fill="x", pady=5, padx=5)
    tk.Label(sub, text=f"frame {i}", bg=sub["bg"]).pack(side="left", padx=10)
    tk.Button(sub, text="click").pack(side="right", padx=10)
"""

#----------------sidebar time!!!----------------#
INFOFRAME = tk.Frame(POSTFRAME)
WRITERFRAME = tk.Frame(POSTFRAME)
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


def sendPost():
    text = WRITERBOX.get("1.0", "end-1c").strip()
    if not text:
        messagebox.showwarning("empty", "post cannot be empty!")
        return
    try:
        CLIENT.app.bsky.feed.post.create(
            repo=CLIENT.me.did,
            record={
                "text": text,
                "createdAt": utils.nowIso(),
            }
        )
        print("posted")
        WRITERBOX.delete("1.0", "end")
        WRITERREMAININGCHARA["text"] = "0"
        WRITERREMAININGCHARA["fg"] = "black"
    except Exception as e:
        messagebox.showerror("error", f"post failed: {e}")


WRITERPOSTBUTTON = tk.Button(WRITERFOOTERRACK, text="Post", command=sendPost)
WRITERPOSTBUTTON.pack(side="right", padx=5,pady=5)
WRITERBOX = tk.Text(WRITERCONTAINER)
WRITERBOX.pack(fill="both", expand=True)
WRITERREMAININGCHARA = tk.Label(WRITERFOOTERRACK, text="320", fg="black")
WRITERREMAININGCHARA.pack(side="left", padx=5)
#----------------MAIN UI (COPIED FROM appbox.py)------------------#

INFOUSERTEXT["text"] = CLIENTPROFILE.handle
INFOFOLLOWERTEXT["text"] = str(CLIENTPROFILE.followers_count) + " followers"
INFOFOLLOWINGTEXT["text"] = str(CLIENTPROFILE.follows_count) + " follows"
INFOPOSTSTEXT["text"] = str(CLIENTPROFILE.posts_count) + " posts"

TIMELINE = CLIENT.app.bsky.feed.get_timeline()

POSTS = []
for item in TIMELINE.feed:
    POSTS.append(post.Post(FEEDSCROLLframe, item, utils.Utils))
    POSTS[-1].getFrame().pack(fill="x", pady=5, padx=5)

#----------------------postbox logic lmao------------------------#

def remainingText(event):
    content = WRITERBOX.get("1.0", "end-1c")
    WRITERREMAININGCHARA["text"] = str(320 - len(content))
    if len(content) >= 320:
        WRITERREMAININGCHARA["fg"] = "red"
    else:
        WRITERREMAININGCHARA["fg"] = "black"
    WRITERBOX.edit_modified(False)

WRITERBOX.bind("<<Modified>>", remainingText)

root.mainloop()