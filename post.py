import tkinter as tk
from tkinter import ttk

class Post:
    def __init__(self, parent, feedItem, utils):
        self.feedItem = feedItem
        self.utils = utils
        self.parent = parent

        self.frame = tk.Frame(parent,
            highlightbackground="grey",
            highlightcolor="grey",
            highlightthickness=2
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

        # top labels
        userLabel = ttk.Label(self.frame, text=displayName)
        handleLabel = ttk.Label(self.frame, text=f"@{handle}")
        userLabel.pack(anchor="nw", padx=10)
        handleLabel.pack(anchor="n", padx=10)

        # post text
        msg = tk.Message(self.frame,
            text=text,
            highlightbackground="grey",
            highlightcolor="grey",
            highlightthickness=2,
            aspect=300
        )
        msg.pack(anchor="center", pady=(5, 5))

        # interaction bar
        interactFrame = tk.Frame(self.frame)

        likeButton = tk.Button(
            interactFrame,
            text="\U0001f90d",
            command=lambda: self.utils.get("like", self.noop)(uri)
        )
        repostButton = tk.Button(
            interactFrame,
            text="\U0001F504",
            command=lambda: self.utils.get("repost", self.noop)(uri)
        )
        replyButton = tk.Button(
            interactFrame,
            text="\U0001f4ac",
            command=lambda: self.utils.get("reply", self.noop)(uri)
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
        otherMenu.add_command(label="Hide Post", command=lambda: self.utils.get("hide", self.noop)(uri))
        otherMenu.add_command(label="Block User", command=lambda: self.utils.get("block", self.noop)(author.did))

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

        interactFrame.pack(pady=(5, 5))
        self.frame.pack_propagate(False)

    def noop(self, *args, **kwargs):
        pass

    def getFrame(self):
        return self.frame
