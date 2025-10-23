import tkinter as tk
from tkinter import ttk, filedialog
import traceback
import ast
import time
import os

DEBOUNCE_MS = 600
AUTOSAVE_INTERVAL = 10000  # ms

starterCode = '''# example: define build_ui(root) to create widgets inside the provided container.
# you may import modules if you need them, e.g. from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

def build_ui(root):
    # root is a frame managed by the designer. create widgets inside it.
    lbl = ttk.Label(root, text="hello from user code")
    lbl.pack(padx=8, pady=8)
    entry = ttk.Entry(root)
    entry.pack(padx=8, pady=4)
    def onClick():
        print("button clicked, entry contains:", entry.get())
    btn = ttk.Button(root, text="press me", command=onClick)
    btn.pack(padx=8, pady=8)
'''

class DesignerApp:
    def __init__(self, master):
        self.master = master
        master.title("tk designer, live runner")
        master.geometry("1000x600")

        self.currentPath = None
        self.autosaveEnabled = False
        self.lastSaveTime = 0

        self.leftPane = ttk.Frame(master)
        self.rightPane = ttk.Frame(master)
        self.leftPane.pack(side="left", fill="both", expand=True)
        self.rightPane.pack(side="right", fill="both", expand=True)

        # toolbar
        toolFrame = ttk.Frame(self.leftPane)
        toolFrame.pack(side="top", fill="x")

        ttk.Button(toolFrame, text="run", command=self.runNow).pack(side="left", padx=4, pady=4)
        ttk.Button(toolFrame, text="stop", command=self.stopPreview).pack(side="left", padx=4, pady=4)
        ttk.Button(toolFrame, text="clear console", command=self.clearConsole).pack(side="left", padx=4, pady=4)
        ttk.Button(toolFrame, text="save", command=self.saveFile).pack(side="left", padx=4, pady=4)
        ttk.Button(toolFrame, text="save as", command=self.saveAs).pack(side="left", padx=4, pady=4)
        ttk.Button(toolFrame, text="open", command=self.openFile).pack(side="left", padx=4, pady=4)
        self.autoSaveBtn = ttk.Button(toolFrame, text="enable autosave", command=self.toggleAutoSave)
        self.autoSaveBtn.pack(side="left", padx=4, pady=4)

        ttk.Label(self.leftPane, text="code editor").pack(anchor="w", padx=6)
        self.editor = tk.Text(self.leftPane, wrap="none", undo=True)
        self.editor.pack(fill="both", expand=True, padx=6, pady=(0,6))
        try: self.editor.configure(font=("Consolas", 11))
        except Exception: pass

        self.editor.insert("1.0", starterCode)
        self.editor.bind("<KeyRelease>", self.onEdit)
        self.lastEditTime = None
        self.scheduledJob = None

        ttk.Label(self.rightPane, text="live preview").pack(anchor="w", padx=6)
        self.previewArea = ttk.Frame(self.rightPane, relief="sunken")
        self.previewArea.pack(fill="both", expand=True, padx=6, pady=(0,6))

        ttk.Label(self.rightPane, text="console / errors").pack(anchor="w", padx=6)
        self.console = tk.Text(self.rightPane, height=10, wrap="none")
        self.console.pack(fill="x", padx=6, pady=(0,6))

        self.previewContainer = None
        self.isRunning = False
        self.currentUserGlobals = None

        self.master.after(AUTOSAVE_INTERVAL, self.autoSaveLoop)
        self.runNow()

    def onEdit(self, event=None):
        if self.scheduledJob is not None:
            self.master.after_cancel(self.scheduledJob)
        self.scheduledJob = self.master.after(DEBOUNCE_MS, self.runNow)

    def clearConsole(self):
        self.console.delete("1.0", "end")

    def log(self, *args):
        text = " ".join(map(str, args)) + "\n"
        self.console.insert("end", text)
        self.console.see("end")

    def stopPreview(self):
        if self.previewContainer:
            for child in self.previewContainer.winfo_children():
                try: child.destroy()
                except Exception: pass
            self.previewContainer.destroy()
            self.previewContainer = None
        self.isRunning = False
        self.log("[preview stopped]")

    def runNow(self):
        code = self.editor.get("1.0", "end")
        self.clearConsole()
        try:
            ast.parse(code)
        except Exception:
            self.log("[syntax error]\n" + traceback.format_exc())
            return

        userGlobals = {}
        userGlobals["print"] = lambda *a, **kw: self.log(*a)
        userGlobals["tk"] = tk
        userGlobals["ttk"] = ttk

        try:
            exec(code, userGlobals)
        except Exception:
            self.log("[exception during exec]\n" + traceback.format_exc())
            return

        buildUi = userGlobals.get("build_ui")
        if not callable(buildUi):
            self.log("[error] expected function build_ui(root)")
            return

        self.stopPreview()
        self.previewContainer = ttk.Frame(self.previewArea)
        self.previewContainer.pack(fill="both", expand=True, padx=4, pady=4)
        innerFrame = ttk.Frame(self.previewContainer)
        innerFrame.pack(fill="both", expand=True, padx=4, pady=4)

        try:
            buildUi(innerFrame)
            self.isRunning = True
            self.currentUserGlobals = userGlobals
            self.log("[ok] ui built")
        except Exception:
            self.log("[exception while running build_ui]\n" + traceback.format_exc())

    def saveFile(self):
        if not self.currentPath:
            return self.saveAs()
        try:
            code = self.editor.get("1.0", "end-1c")
            with open(self.currentPath, "w", encoding="utf-8") as f:
                f.write(code)
            self.lastSaveTime = time.time()
            self.log(f"[saved to {os.path.basename(self.currentPath)}]")
        except Exception as e:
            self.log("[error saving file]", e)

    def saveAs(self):
        path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files","*.py"), ("All files","*.*")])
        if not path:
            return
        self.currentPath = path
        self.saveFile()

    def openFile(self):
        path = filedialog.askopenfilename(filetypes=[("Python files","*.py"), ("All files","*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", code)
            self.currentPath = path
            self.log(f"[opened {os.path.basename(path)}]")
            self.runNow()
        except Exception as e:
            self.log("[error opening file]", e)

    def toggleAutoSave(self):
        self.autosaveEnabled = not self.autosaveEnabled
        label = "disable autosave" if self.autosaveEnabled else "enable autosave"
        self.autoSaveBtn.configure(text=label)
        self.log(f"[autosave {'enabled' if self.autosaveEnabled else 'disabled'}]")

    def autoSaveLoop(self):
        if self.autosaveEnabled and self.currentPath:
            try:
                code = self.editor.get("1.0", "end-1c")
                with open(self.currentPath, "w", encoding="utf-8") as f:
                    f.write(code)
                self.lastSaveTime = time.time()
                self.log(f"[autosaved {os.path.basename(self.currentPath)}]")
            except Exception as e:
                self.log("[error during autosave]", e)
        self.master.after(AUTOSAVE_INTERVAL, self.autoSaveLoop)

if __name__ == "__main__":
    root = tk.Tk()
    app = DesignerApp(root)
    root.mainloop()
