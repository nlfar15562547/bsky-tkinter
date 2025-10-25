import tkinter as tk
from tkinter import messagebox
import atproto
import clipboard
from datetime import datetime, timezone

CLIENT = None # INITIALIZE THIS VRO ♥♥♥

def nowIso():
    return datetime.now(timezone.utc).isoformat()

def like(uri, cid):
    try:
        CLIENT.app.bsky.feed.like.create(
            repo=CLIENT.me.did,
            record={
                "subject": {"uri": uri, "cid": cid},
                "createdAt": nowIso(),
            }
        )
        print(f"liked {uri}")
    except Exception as e:
        print("like failed:", e)

def repost(uri, cid):
    try:
        CLIENT.app.bsky.feed.repost.create(
            repo=CLIENT.me.did,
            record={
                "subject": {"uri": uri, "cid": cid},
                "createdAt": nowIso(),
            }
        )
        print(f"reposted {uri}")
    except Exception as e:
        print("repost failed:", e)

def reply(uri, cid):
    # popup window
    popup = tk.Toplevel()
    popup.title("Reply to Post")
    popup.geometry("400x300")
    popup.resizable(False, False)

    tk.Label(popup, text="reply:").pack(anchor="nw", padx=10, pady=5)
    textBox = tk.Text(popup, wrap="word", height=10, width=50)
    textBox.pack(padx=10, pady=5, fill="both", expand=True)

    def sendReply():
        text = textBox.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("empty", "reply cannot be empty!")
            return
        try:
            CLIENT.app.bsky.feed.post.create(
                repo=CLIENT.me.did,
                record={
                    "text": text,
                    "reply": {
                        "root": {"uri": uri, "cid": cid},
                        "parent": {"uri": uri, "cid": cid},
                    },
                    "createdAt": nowIso(),
                }
            )
            print("replied to", uri)
            popup.destroy()
        except Exception as e:
            messagebox.showerror("error", f"reply failed: {e}")

    tk.Button(popup, text="Send", command=sendReply).pack(pady=10)

def share(uri):
    clipboard.copy(uri)
    print(f"copied post link to clipboard: {uri}")

def copy(text):
    clipboard.copy(text)
    print("copied text to clipboard")

def follow(did):
    try:
        CLIENT.app.bsky.graph.follow.create(
            repo=CLIENT.me.did,
            record={
                "subject": did,
                "createdAt": nowIso(),
            }
        )
        print(f"followed {did}")
    except Exception as e:
        print("follow failed:", e)

def hide(uri):
    print(f"unimplemented, but pretending to hide: {uri}")

def block(did):
    try:
        CLIENT.app.bsky.graph.block.create(
            repo=CLIENT.me.did,
            record={
                "subject": did,
                "createdAt": nowIso(),
            }
        )
        print(f"blocked {did}")
    except Exception as e:
        print("block failed:", e)

Utils = {
    "like": like,
    "repost": repost,
    "reply": reply,
    "share": share,
    "copy": copy,
    "follow": follow,
    "hide": hide,
    "block": block,
}
