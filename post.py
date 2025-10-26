import tkinter as tk
from tkinter import ttk
import io
import requests
from PIL import Image, ImageTk

class Post:
    def __init__(self, parent, feedItem, utils):
        self.feedItem = feedItem
        self.utils = utils
        self.parent = parent
        self.imageRefs = []  # pretend to care about the images because otherwise garbage collector eats them

        self.frame = tk.Frame(
            parent,
            highlightbackground="grey",
            highlightcolor="grey",
            highlightthickness=2,
        )
        self.buildUI()

    def buildUI(self):
        post = self.feedItem.post
        author = post.author
        record = post.record

        displayName = getattr(author, "display_name", "(unknown user)")
        handle = getattr(author, "handle", "@unknown")
        text = getattr(record, "text", "(no content)")
        uri = getattr(post, "uri", None)
        cid = getattr(post, "cid", None)

        # top labels
        userLabel = ttk.Label(self.frame, text=displayName)
        handleLabel = ttk.Label(self.frame, text=f"@{handle}")
        userLabel.pack(anchor="nw", padx=10, fill="x")
        handleLabel.pack(anchor="n", padx=10, fill="x")

        # post text
        msg = tk.Message(
            self.frame,
            text=text,
            highlightbackground="grey",
            highlightcolor="grey",
            highlightthickness=2,
            aspect=300
        )
        msg.pack(anchor="center", pady=(5, 5), fill="x")

        # try to render any image embeds
        self.renderEmbeds(post)

        # interaction bar
        interactFrame = tk.Frame(self.frame)

        likeButton = tk.Button(
            interactFrame,
            text="\U0001f90d",
            command=lambda: self.utils.get("like", self.noop)(uri, cid)
        )
        repostButton = tk.Button(
            interactFrame,
            text="\U0001F504",
            command=lambda: self.utils.get("repost", self.noop)(uri, cid)
        )
        replyButton = tk.Button(
            interactFrame,
            text="\U0001f4ac",
            command=lambda: self.utils.get("reply", self.noop)(uri, cid)
        )

        likeButton.pack(side="left", padx=10)
        repostButton.pack(side="left", padx=10)
        replyButton.pack(side="left", padx=10)

        # other menu
        otherMenu = tk.Menu(interactFrame, tearoff=0)
        otherMenu.add_command(label="Share", command=lambda: self.utils.get("share", self.noop)(uri))
        otherMenu.add_command(label="Copy Post Text", command=lambda: self.utils.get("copy", self.noop)(text))
        otherMenu.add_separator()
        otherMenu.add_command(label="Follow User", command=lambda: self.utils.get("follow", self.noop)(author.did))
        otherMenu.add_separator()
        otherMenu.add_command(label="i haven't implemented these yet", command=self.noop)
        otherMenu.add_separator()
        otherMenu.add_command(label="Hide Post", command=lambda: self.utils.get("hide", self.noop)(uri))
        otherMenu.add_command(label="Block User", command=lambda: self.utils.get("block", self.noop)(author.did))
        
        otherMenu.entryconfig("i haven't implemented these yet", state="disabled")
        otherMenu.entryconfig("Hide Post", state="disabled")
        otherMenu.entryconfig("Block User", state="disabled")

        def showOtherMenu():
            x = otherMenuButton.winfo_rootx()
            y = otherMenuButton.winfo_rooty() + otherMenuButton.winfo_height()
            otherMenu.tk_popup(x, y)

        otherMenuButton = tk.Button(
            interactFrame,
            text="\u22ef",
            relief="raised",
            command=showOtherMenu
        )
        otherMenuButton.pack(side="left", padx=10)

        interactFrame.pack(pady=(5, 5), fill="x")

    def renderEmbeds(self, post):
        embed = getattr(post, "embed", None)
        if not embed:
            return

        if hasattr(embed, "images"):
            for img in embed.images:
                url = getattr(img, "thumb", None) or getattr(img, "fullsize", None)
                if not url:
                    continue
                try:
                    resp = requests.get(url, timeout=10)
                    resp.raise_for_status()
                    pilImg = Image.open(io.BytesIO(resp.content))
                    pilImg.thumbnail((400, 400))  # resize
                    tkImg = ImageTk.PhotoImage(pilImg)

                    imgLabel = tk.Label(self.frame, image=tkImg)
                    imgLabel.pack(pady=(5, 5))
                    self.imageRefs.append(tkImg)  # keep reference
                except Exception as e:
                    print("failed to load image:", e)

    def noop(self, *args, **kwargs):
        pass

    def getFrame(self):
        return self.frame
    

    def __str__(self):
        return "Post(\n" + str(self.parent) + ",\n" + str(self.feedItem) + ",\n" + str(self.utils) + ",\n)"
