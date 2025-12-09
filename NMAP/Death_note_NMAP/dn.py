import tkinter as tk
from tkinter import scrolledtext, messagebox, font
import subprocess
import threading
import shlex
import webbrowser
import os
import sys
from PIL import Image, ImageTk  # pip install pillow

# --- THEME PALETTE (Gothic & Death Note) ---
COLORS = {
    "bg": "#050505",          # Almost pure black
    "fg": "#e0e0e0",          # Bone white
    "accent": "#ff0000",      # Blood red (Kira)
    "misa": "#bfaee3",        # Light Lavender (Misa)
    "misa_dark": "#5e2a84",   # Deep Purple
    "entry_bg": "#121212",    # Dark paper
    "button_bg": "#2b0000",   # Dried blood
    "button_active": "#ff3333",
    "border": "#333333"
}

# --- ASCII ARTIFACTS ---
# Centered and padded for 950px width
RYUK_APPLE = """
      .:'
   __ :'__
.'`  `-'  ``.
:          .-'
:         :
 :         :
  `.__.-.__.'
"""

MISA_CROSS = """
      †
    †††††
      †
      †
      †
"""

KIRA_LOGO = """
      K I R A
    d8b   db  .d88b.  
    888o  88 .8P  Y8. 
    88V8o 88 88    88 
    88 V8o88 88    88 
    88  V888 `8b  d8' 
    VP   V8P  `Y88P'  
"""

TITLE_ART = """
DEATH NOTE
NETWORK  JUDGMENT
"""

class DeathNoteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KIRA :: NEW WORLD ORDER")
        self.root.geometry("900x950")
        self.root.configure(bg=COLORS["bg"])
        self.root.resizable(False, False)

        # Font Configurations (Fallbacks for cross-platform compatibility)
        self.font_header = font.Font(family="Old English Text MT", size=28, weight="bold")
        # Fallback if Old English isn't installed
        if "Old English Text MT" not in font.families():
             self.font_header = font.Font(family="Times New Roman", size=28, weight="bold")

        self.font_mono = font.Font(family="Courier New", size=10)
        self.font_mono_bold = font.Font(family="Courier New", size=11, weight="bold")
        self.font_ui = font.Font(family="Arial", size=10)

        # 1. SETUP CANVAS
        self.canvas = tk.Canvas(
            root, 
            width=900, 
            height=950, 
            bg=COLORS["bg"], 
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # 2. BACKGROUND TEXTURE LOADER
        self.load_background()

        # 3. UI BUILDER
        self.build_ui()
        
        # State
        self.current_scan_target = ""

    def load_background(self):
        """Attempts to load a background image, dims it, and centers it."""
        try:
            possible_names = ["deathnote_bg.jpg", "paper.jpg", "texture.png"]
            image_path = None
            
            for name in possible_names:
                if os.path.exists(name):
                    image_path = name
                    break
            
            if image_path:
                pil_image = Image.open(image_path)
                # Resize to fit window
                pil_image = pil_image.resize((900, 950), Image.Resampling.LANCZOS)
                
                # Darken image for readability
                from PIL import ImageEnhance
                enhancer = ImageEnhance.Brightness(pil_image)
                pil_image = enhancer.enhance(0.20)  # 20% brightness
                
                self.bg_photo = ImageTk.PhotoImage(pil_image)
                self.canvas.create_image(450, 475, image=self.bg_photo, anchor="center")
        except Exception as e:
            print(f"Background load skipped: {e}")

    def build_ui(self):
        current_y = 50

        # --- HEADER ---
        # Shadow effect for title
        self.canvas.create_text(453, current_y+3, text=TITLE_ART, fill="#1a0000", font=self.font_header, justify="center")
        self.canvas.create_text(450, current_y, text=TITLE_ART, fill=COLORS["fg"], font=self.font_header, justify="center")
        current_y += 100

        self.canvas.create_text(
            450, current_y, 
            text="「 I AM THE GOD OF THE NEW WORLD 」", 
            fill=COLORS["accent"], 
            font=(self.font_mono_bold.cget("family"), 12, "bold")
        )
        current_y += 60

        # --- ART ROW ---
        # Apple (Left), Logo (Center), Cross (Right)
        self.canvas.create_text(150, current_y, text=RYUK_APPLE, fill=COLORS["accent"], font=self.font_mono)
        self.canvas.create_text(450, current_y, text=KIRA_LOGO, fill=COLORS["fg"], font=("Courier New", 8, "bold"))
        self.canvas.create_text(750, current_y, text=MISA_CROSS, fill=COLORS["misa"], font=self.font_mono)
        current_y += 90

        # --- TARGET INPUT ---
        input_container = tk.Frame(self.canvas, bg=COLORS["bg"], bd=1, relief="solid")
        
        # Inner padding frame
        inner_frame = tk.Frame(input_container, bg=COLORS["bg"], padx=10, pady=10)
        inner_frame.pack()

        tk.Label(
            inner_frame, 
            text="VICTIM IDENTIFIER (IP):", 
            font=self.font_mono_bold, 
            bg=COLORS["bg"], 
            fg=COLORS["fg"]
        ).pack(anchor="w")

        self.target_entry = tk.Entry(
            inner_frame, 
            font=("Courier New", 16), 
            width=24, 
            bg=COLORS["entry_bg"], 
            fg=COLORS["accent"], 
            insertbackground=COLORS["accent"],
            relief="flat",
            bd=5
        )
        self.target_entry.insert(0, "127.0.0.1")
        self.target_entry.pack(pady=(5, 0))

        self.canvas.create_window(450, current_y, window=input_container, anchor="center")
        current_y += 100

        # --- OPTIONS (SHINIGAMI EYES) ---
        opt_container = tk.Frame(self.canvas, bg=COLORS["bg"])
        
        tk.Label(
            opt_container, 
            text="-- SHINIGAMI EYES DEAL --", 
            font=("Courier New", 9), 
            bg=COLORS["bg"], 
            fg=COLORS["misa"]
        ).pack(pady=5)

        self.var_sv = tk.BooleanVar() # Version
        self.var_sc = tk.BooleanVar() # Scripts
        self.var_os = tk.BooleanVar() # OS

        chk_frame = tk.Frame(opt_container, bg=COLORS["bg"])
        chk_frame.pack()

        chk_style = {
            "bg": COLORS["bg"], "fg": COLORS["fg"], 
            "selectcolor": "#222", "activebackground": COLORS["bg"], 
            "activeforeground": COLORS["accent"], "font": self.font_mono,
            "bd": 0
        }

        tk.Checkbutton(chk_frame, text="True Name (-sV)", variable=self.var_sv, **chk_style).pack(side="left", padx=10)
        tk.Checkbutton(chk_frame, text="Hidden Secrets (-sC)", variable=self.var_sc, **chk_style).pack(side="left", padx=10)
        tk.Checkbutton(chk_frame, text="Lifespan (-O)", variable=self.var_os, **chk_style).pack(side="left", padx=10)

        self.canvas.create_window(450, current_y, window=opt_container, anchor="center")
        current_y += 80

        # --- EXECUTE BUTTON ---
        btn_frame = tk.Frame(self.canvas, bg=COLORS["bg"])
        
        self.custom_entry = tk.Entry(
            btn_frame, font=("Courier New", 10), width=15, 
            bg=COLORS["entry_bg"], fg="#666", relief="flat"
        )
        self.custom_entry.insert(0, "-v") # Default verbose
        self.custom_entry.pack(side="left", padx=10)

        self.scan_button = tk.Button(
            btn_frame, 
            text="D E L E T E", 
            font=("Courier New", 14, "bold"),
            bg=COLORS["button_bg"], 
            fg=COLORS["fg"],
            activebackground=COLORS["button_active"], 
            activeforeground="#000",
            relief="flat", 
            cursor="tcross",
            width=18,
            command=self.start_scan_thread
        )
        self.scan_button.pack(side="left", padx=10)

        self.canvas.create_window(450, current_y, window=btn_frame, anchor="center")
        current_y += 60

        # --- THE NOTEBOOK OUTPUT ---
        self.canvas.create_text(450, current_y, text="▼ JUDGMENT LOG ▼", fill=COLORS["misa"], font=self.font_mono_bold)
        current_y += 20

        # Container for border
        log_frame = tk.Frame(self.canvas, bg=COLORS["fg"], bd=1)
        
        self.output_area = scrolledtext.ScrolledText(
            log_frame, 
            width=92, 
            height=16, 
            font=("Courier New", 9), 
            bg="#111", 
            fg=COLORS["fg"],
            insertbackground=COLORS["accent"],
            bd=0,
            padx=10,
            pady=10
        )
        self.output_area.pack()
        
        # Styling Tags
        self.output_area.tag_config("kira", foreground=COLORS["accent"])
        self.output_area.tag_config("misa", foreground=COLORS["misa"])
        self.output_area.tag_config("link", foreground=COLORS["button_active"], underline=1)
        self.output_area.tag_bind("link", "<Button-1>", self.on_link_click)
        self.output_area.tag_bind("link", "<Enter>", lambda e: self.output_area.config(cursor="hand2"))
        self.output_area.tag_bind("link", "<Leave>", lambda e: self.output_area.config(cursor="arrow"))

        self.canvas.create_window(450, current_y, window=log_frame, anchor="n")
        
        # Initial Text
        self.log("Death Note initialized...\n", "misa")
        self.log("Waiting for name entry.\n")

    def log(self, text, tag=None):
        self.output_area.insert(tk.END, text, tag)
        self.output_area.see(tk.END)
        self.scan_for_links()

    def scan_for_links(self):
        """Highlights IP addresses and Ports to make them clickable."""
        # Regex for Ports (e.g., 80/tcp) and URLs
        patterns = [
            (r"(\d+/tcp)", "port"),
            (r"(http[s]?://\S+)", "url")
        ]
        
        for pattern, type_ in patterns:
            start_index = "1.0"
            while True:
                count = tk.IntVar()
                pos = self.output_area.search(pattern, start_index, stopindex=tk.END, count=count, regexp=True)
                if not pos: break
                
                end_index = f"{pos}+{count.get()}c"
                text_match = self.output_area.get(pos, end_index)
                
                self.output_area.tag_add("link", pos, end_index)
                
                # Store the data in a unique tag for retrieval on click
                data_tag = f"data_{text_match}_{type_}"
                self.output_area.tag_add(data_tag, pos, end_index)
                
                start_index = end_index

    def on_link_click(self, event):
        try:
            index = self.output_area.index(f"@{event.x},{event.y}")
            tags = self.output_area.tag_names(index)
            
            for tag in tags:
                if tag.startswith("data_"):
                    # Extract data from tag name (format: data_TEXT_TYPE)
                    _, text, type_ = tag.split("_", 2)
                    
                    if type_ == "url":
                        webbrowser.open(text)
                    elif type_ == "port":
                        port = text.split("/")[0]
                        url = f"http://{self.current_scan_target}:{port}"
                        if messagebox.askyesno("Investigate?", f"Open {url} in browser?"):
                            webbrowser.open(url)
                    break
        except Exception as e:
            print(e)

    def start_scan_thread(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showerror("Rules of Death Note", "You must write a name (IP) in the note.")
            return

        self.current_scan_target = target
        self.scan_button.config(state="disabled", text="WRITING...", bg="#000")
        
        self.output_area.delete('1.0', tk.END)
        self.log(f"----------------------------------------\n")
        self.log(f" TARGET: {target}\n", "kira")
        self.log(f"----------------------------------------\n\n")

        # Run in separate thread to keep UI responsive
        t = threading.Thread(target=self.run_nmap, args=(target,))
        t.daemon = True
        t.start()

    def run_nmap(self, target):
        cmd = ["nmap"]
        if self.var_sv.get(): cmd.append("-sV")
        if self.var_sc.get(): cmd.append("-sC")
        if self.var_os.get(): cmd.append("-O")
        
        # Add custom args
        custom = self.custom_entry.get().strip()
        if custom:
            cmd.extend(shlex.split(custom))
            
        cmd.append(target)
        
        try:
            # Check if nmap is installed first
            try:
                subprocess.run(["nmap", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                self.root.after(0, self.log, "ERROR: Nmap not found in PATH.\n", "kira")
                self.root.after(0, self.reset_button)
                return

            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                # Create no window flag for Windows to hide the console pop-up
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )

            for line in iter(process.stdout.readline, ''):
                self.root.after(0, self.log, line)
            
            process.stdout.close()
            process.wait()
            
            self.root.after(0, self.log, "\n[ JUDGMENT COMPLETE ]\n", "kira")
            
        except Exception as e:
            self.root.after(0, self.log, f"\nERROR: {str(e)}\n", "kira")
        
        self.root.after(0, self.reset_button)

    def reset_button(self):
        self.scan_button.config(state="normal", text="D E L E T E", bg=COLORS["button_bg"])

if __name__ == "__main__":
    root = tk.Tk()
    app = DeathNoteGUI(root)
    root.mainloop()
