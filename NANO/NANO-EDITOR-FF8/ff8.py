import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import os

# --- Balamb Garden Color Palette ---
FF8_BG_DARK = "#1e2024"     # Deep Gunmetal
FF8_BG_LIGHT = "#3a3e45"    # Menu Background
FF8_BORDER = "#989ba6"      # Silver/Grey Border
FF8_HIGHLIGHT = "#00ffef"   # "Cursor" Cyan
FF8_TEXT = "#ffffff"
FF8_DIM = "#888888"

# --- Fonts ---
# 'Times New Roman' or 'Arial' fits FF8's cleaner, hi-res look better than FF7's blocks
# 'Consolas' used for the actual text editing to keep the Nano feel
UI_FONT = ("Arial", 10, "bold")
EDITOR_FONT = ("Consolas", 12)
HEADER_FONT = ("Arial", 12, "bold")

class FF8Nano:
    def __init__(self, root):
        self.root = root
        self.root.title("SeeD // FIELD EDITOR")
        self.root.geometry("800x600")
        self.root.configure(bg="black")
        
        self.current_file = None
        self.is_modified = False

        # --- Background Gradient ---
        # FF8 used a smooth grey gradient. We simulate this with a canvas.
        self.canvas = tk.Canvas(root, highlightthickness=0, bg="black")
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.draw_ff8_gradient()

        # --- 1. Top Header (Nano Status Bar) ---
        self.header_frame = tk.Frame(root, bg=FF8_BG_DARK, bd=1, relief="solid")
        self.header_frame.place(x=10, y=10, width=780, height=40)
        
        # Draw inner border for that "Menu Box" look
        self.draw_menu_border(self.header_frame)

        # Filename Label (Centered)
        self.title_var = tk.StringVar(value="[ New Buffer ]")
        self.title_label = tk.Label(
            self.header_frame, 
            textvariable=self.title_var, 
            font=HEADER_FONT, 
            bg=FF8_BG_DARK, 
            fg=FF8_HIGHLIGHT
        )
        self.title_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Version / App Name (Left)
        tk.Label(
            self.header_frame, 
            text="GARDEN v8.0", 
            font=("Arial", 8), 
            bg=FF8_BG_DARK, 
            fg=FF8_DIM
        ).place(x=10, y=12)

        # Modified Indicator (Right)
        self.mod_label = tk.Label(
            self.header_frame, 
            text="", 
            font=("Arial", 10, "bold"), 
            bg=FF8_BG_DARK, 
            fg="#ff4040" # Red for unsaved changes
        )
        self.mod_label.place(x=700, y=10)

        # --- 2. The Editor (Main Body) ---
        self.editor_frame = tk.Frame(root, bg=FF8_BG_DARK, bd=0)
        self.editor_frame.place(x=10, y=60, width=780, height=440)
        
        # The Text Widget
        self.text_area = scrolledtext.ScrolledText(
            self.editor_frame,
            font=EDITOR_FONT,
            bg="#101214", # Very dark grey for typing area
            fg=FF8_TEXT,
            insertbackground=FF8_HIGHLIGHT, # Cyan Cursor
            bd=0,
            undo=True,
            padx=10, pady=10
        )
        self.text_area.pack(fill="both", expand=True)
        
        # Bindings for Nano shortcuts
        self.root.bind("<Control-o>", self.save_file)
        self.root.bind("<Control-s>", self.save_file) # Alternate
        self.root.bind("<Control-r>", self.open_file)
        self.root.bind("<Control-x>", self.exit_editor)
        self.text_area.bind("<<Modified>>", self.on_modified)

        # --- 3. The Bottom Menu (Junction System) ---
        # This mimics the 2-row shortcut list at the bottom of Nano
        self.menu_frame = tk.Frame(root, bg=FF8_BG_DARK, bd=1, relief="solid")
        self.menu_frame.place(x=10, y=510, width=780, height=80)
        self.draw_menu_border(self.menu_frame)

        # Grid layout for commands
        # ^G Help  ^O Write Out  ^W Where Is  ^K Cut Text
        # ^X Exit  ^R Read File  ^\ Replace   ^U Uncut Text
        
        commands = [
            ("^G", "TUTORIAL", self.show_help),
            ("^O", "JUNCTION (Save)", self.save_file),
            ("^X", "RETREAT (Exit)", self.exit_editor),
            ("^R", "SCAN (Open)", self.open_file),
            ("^K", "CARD (Cut)", self.cut_text),
            ("^U", "REVIVE (Paste)", self.paste_text)
        ]

        # Create the grid
        for i, (key, desc, cmd) in enumerate(commands):
            row = i // 2
            col = (i % 2) * 2 # Spread them out 
            
            # Frame for each command
            cmd_frame = tk.Frame(self.menu_frame, bg=FF8_BG_DARK)
            cmd_frame.grid(row=row, column=col, sticky="w", padx=20, pady=5)
            
            # The Key (e.g. ^X) in White
            lbl_key = tk.Label(cmd_frame, text=key, font=("Arial", 10, "bold"), bg="black", fg=FF8_HIGHLIGHT, width=4)
            lbl_key.pack(side=tk.LEFT)
            
            # The Desc (e.g. Exit) in Grey
            btn = tk.Button(
                cmd_frame, 
                text=desc, 
                font=UI_FONT, 
                bg=FF8_BG_DARK, 
                fg=FF8_TEXT,
                activebackground=FF8_HIGHLIGHT,
                activeforeground="black",
                bd=0,
                command=cmd,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            # Hover effect (The "Hand" cursor pointing logic)
            btn.bind("<Enter>", lambda e, b=btn: b.config(fg=FF8_HIGHLIGHT))
            btn.bind("<Leave>", lambda e, b=btn: b.config(fg=FF8_TEXT))

        self.menu_frame.grid_columnconfigure(1, weight=1) # Spacing
        self.menu_frame.grid_columnconfigure(3, weight=1)

        # Draw "Scanlines" (Optional aesthetic)
        self.draw_scanlines()

    def draw_ff8_gradient(self):
        # FF8 menus are slate grey
        w, h = 800, 600
        # Draw vertical bands
        steps = 20
        for i in range(steps):
            # Interpolate between two greys
            color_val = int(30 + (i * 1.5))
            hex_color = f"#{color_val:02x}{color_val:02x}{color_val:02x}"
            y0 = i * (h / steps)
            y1 = (i + 1) * (h / steps)
            self.canvas.create_rectangle(0, y0, w, y1, fill=hex_color, outline="")

    def draw_menu_border(self, parent):
        # FF8 borders are usually thin white lines inside the box
        # Tkinter Frames handle the outer border, we can put a canvas inside if we want strict accuracy
        # Or just rely on the 'bd=1, relief=solid' set in init.
        pass 

    def draw_scanlines(self):
        # Draws thin horizontal lines over the canvas to mimic CRT
        for y in range(0, 600, 4):
            self.canvas.create_line(0, y, 800, y, fill="#000000", stipple="gray25")

    # --- Functionality ---

    def on_modified(self, event=None):
        if self.text_area.edit_modified():
            self.is_modified = True
            self.mod_label.config(text="[MODIFIED]")
        self.text_area.edit_modified(False) # Reset the internal flag

    def open_file(self, event=None):
        path = filedialog.askopenfilename()
        if path:
            try:
                with open(path, 'r') as f:
                    content = f.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, content)
                self.current_file = path
                self.title_var.set(f"File: {os.path.basename(path)}")
                self.mod_label.config(text="")
                self.is_modified = False
            except Exception as e:
                messagebox.showerror("Scan Error", f"Failed to read data:\n{e}")

    def save_file(self, event=None):
        if not self.current_file:
            # Save As
            path = filedialog.asksaveasfilename()
            if not path: return
            self.current_file = path
        
        try:
            content = self.text_area.get(1.0, tk.END)
            with open(self.current_file, 'w') as f:
                f.write(content)
            self.title_var.set(f"File: {os.path.basename(self.current_file)}")
            self.mod_label.config(text="[SAVED]")
            self.root.after(2000, lambda: self.mod_label.config(text=""))
            self.is_modified = False
        except Exception as e:
            messagebox.showerror("Junction Error", f"Failed to write data:\n{e}")

    def cut_text(self, event=None):
        self.text_area.event_generate("<<Cut>>")

    def paste_text(self, event=None):
        self.text_area.event_generate("<<Paste>>")

    def exit_editor(self, event=None):
        if self.is_modified:
            if not messagebox.askyesno("Retreat?", "Data has been modified. Retreat without saving?"):
                return
        self.root.quit()

    def show_help(self, event=None):
        messagebox.showinfo("SeeD Tutorial", 
                            "Standard Nano Protocols Apply.\n\n"
                            "^O : Save Data (Junction)\n"
                            "^X : Close Terminal (Retreat)\n"
                            "^R : Load Data (Scan)")

if __name__ == "__main__":
    root = tk.Tk()
    app = FF8Nano(root)
    root.mainloop()
