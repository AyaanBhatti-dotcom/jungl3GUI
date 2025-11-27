import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox, ttk
import subprocess
import threading
import re

# --- FF7 Color Palette ---
TEXT_WHITE = "#e8e8e8"
TEXT_CYAN = "#00ffff"      # Headers / Important Items (Filenames)
TEXT_YELLOW = "#ffff00"    # Numbers / Offsets
TEXT_GREEN = "#5dfc6a"     # Magic / File Types
TEXT_RED = "#ff4040"       # Errors
TEXT_SHADOW = "#151515"    # Dark shadow
BG_DARK = "#000020"        # Dark Blue Background
BORDER_COLOR = "#dedede"

# --- Fonts ---
LOG_FONT = ("Consolas", 11)
HEADER_FONT = ("Consolas", 12, "bold")
NAME_FONT = ("Consolas", 28, "bold")

class FF7Binwalk:
    def __init__(self, root):
        self.root = root
        self.root.title("BINWALK // AVALANCHE PROTOCOL")
        self.root.geometry("900x700")
        self.root.configure(bg="black")
        
        self.canvas = tk.Canvas(root, highlightthickness=0, bg="black")
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.draw_ff7_gradient()

        # --- 1. Header Window ---
        self.create_window(20, 20, 860, 95)
        
        tk.Label(root, text="NAME:", font=("Consolas", 10, "bold"), bg="#000040", fg=TEXT_CYAN).place(x=40, y=30)
        tk.Label(root, text="BINWALK", font=NAME_FONT, bg="#000040", fg=TEXT_SHADOW).place(x=42, y=47)
        tk.Label(root, text="BINWALK", font=NAME_FONT, bg="#000040", fg=TEXT_WHITE).place(x=40, y=45)

        tk.Label(root, text="LV", font=("Consolas", 10, "bold"), bg="#000040", fg=TEXT_CYAN).place(x=760, y=35)
        tk.Label(root, text="99", font=("Consolas", 20), bg="#000040", fg=TEXT_WHITE).place(x=790, y=30)
        tk.Label(root, text="HP", font=("Consolas", 10, "bold"), bg="#000040", fg=TEXT_CYAN).place(x=760, y=65)
        tk.Label(root, text="9999", font=("Consolas", 12), bg="#000040", fg=TEXT_WHITE).place(x=790, y=65)

        # --- 2. Target Window ---
        self.create_window(20, 110, 860, 190)
        
        tk.Label(root, text="EQUIP WEAPON (File):", font=HEADER_FONT, bg="#000040", fg=TEXT_CYAN).place(x=40, y=125)
        self.file_path = tk.StringVar(value="No Equipment")
        
        self.file_btn = tk.Button(
            root, text=" SELECT ", font=HEADER_FONT, command=self.select_file,
            bg="#000020", fg=TEXT_WHITE, activebackground="#000050", activeforeground=TEXT_WHITE,
            bd=1, relief="solid", cursor="hand2"
        )
        self.file_btn.place(x=40, y=150)
        
        self.file_label = tk.Label(root, textvariable=self.file_path, font=("Consolas", 11, "italic"), bg="#000040", fg="#aaaaaa")
        self.file_label.place(x=140, y=155)

        # --- 3. Materia Slots ---
        self.create_window(20, 210, 600, 270)
        self.var_extract = tk.BooleanVar()
        self.var_matryoshka = tk.BooleanVar()
        self.var_entropy = tk.BooleanVar()

        self.create_materia_toggle(root, 40, 225, TEXT_GREEN, "EXTRACT (-e)", self.var_extract)
        self.create_materia_toggle(root, 200, 225, TEXT_YELLOW, "RECURSIVE (-M)", self.var_matryoshka)
        self.create_materia_toggle(root, 380, 225, TEXT_RED, "ENTROPY (-E)", self.var_entropy)

        # --- 4. Limit Break ---
        self.create_window(620, 210, 860, 270)
        
        tk.Frame(root, bg="black").place(x=640, y=245, width=200, height=10)
        self.limit_bar = tk.Frame(root, bg="#440022")
        self.limit_bar.place(x=640, y=245, width=0, height=10)
        
        self.cast_btn = tk.Button(
            root, text="LIMIT BREAK", font=("Consolas", 14, "bold"), command=self.start_scan_thread,
            bg="#200000", fg=TEXT_WHITE, activebackground="#d6498b", bd=1, relief="raised", cursor="hand2"
        )
        self.cast_btn.place(x=640, y=212, width=200, height=30)

        # --- 5. Battle Log ---
        self.create_window(20, 290, 860, 680)
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Vertical.TScrollbar", background="#000040", troughcolor="#000020", bordercolor="#000040", arrowcolor=TEXT_WHITE)

        log_frame = tk.Frame(root, bg=BG_DARK)
        log_frame.place(x=35, y=305, width=810, height=360)

        self.scrollbar = ttk.Scrollbar(log_frame, orient="vertical")
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.output_area = tk.Text(
            log_frame, font=LOG_FONT, bg=BG_DARK, fg=TEXT_WHITE, bd=0,
            yscrollcommand=self.scrollbar.set, padx=10, pady=10, spacing1=2
        )
        self.output_area.pack(side=tk.LEFT, fill="both", expand=True)
        self.scrollbar.config(command=self.output_area.yview)

        # --- Text Output Configuration ---
        self.output_area.tag_config("header", foreground=TEXT_CYAN, font=("Consolas", 11, "bold"))
        self.output_area.tag_config("offset", foreground=TEXT_YELLOW)
        self.output_area.tag_config("filetype", foreground=TEXT_GREEN, font=("Consolas", 11, "bold"))
        self.output_area.tag_config("info", foreground="#888888") # Gray for generic text
        self.output_area.tag_config("filename_label", foreground="#aaaaaa") # The text "name:"
        self.output_area.tag_config("filename", foreground=TEXT_CYAN, font=("Consolas", 11, "bold")) # The actual file name!
        self.output_area.tag_config("error", foreground=TEXT_RED)
        self.output_area.tag_config("system", foreground="#d6498b")

        self.log_message("Battle Log Initialized...", "system")

    def draw_ff7_gradient(self):
        w, h = 900, 700
        colors = ["#000050", "#000060", "#000070", "#000080", "#000090"]
        self.canvas.create_rectangle(0, 0, w, h, fill="#000020", outline="")
        for i, color in enumerate(colors):
            m = i * 40
            self.canvas.create_rectangle(m, m, w-m, h-m, outline="", fill=color)

    def create_window(self, x1, y1, x2, y2):
        self.canvas.create_rectangle(x1, y1, x2, y2, outline=BORDER_COLOR, width=3)
        self.canvas.create_rectangle(x1+3, y1+3, x2-3, y2-3, outline="#555555", width=1)

    def create_materia_toggle(self, parent, x, y, color, text, variable):
        frame = tk.Frame(parent, bg="#000040")
        frame.place(x=x, y=y)
        c = tk.Canvas(frame, width=25, height=25, bg="#000040", highlightthickness=0)
        c.pack(side=tk.LEFT)
        
        socket_id = c.create_oval(2, 2, 23, 23, outline="#888", width=2)
        orb_id = c.create_oval(4, 4, 21, 21, fill="", outline="") 

        label = tk.Label(frame, text=text, font=("Consolas", 10, "bold"), bg="#000040", fg=TEXT_WHITE)
        label.pack(side=tk.LEFT, padx=5)

        def toggle(event):
            val = not variable.get()
            variable.set(val)
            if val:
                c.itemconfig(orb_id, fill=color)
                c.itemconfig(socket_id, outline="white")
                label.config(fg=color)
            else:
                c.itemconfig(orb_id, fill="")
                c.itemconfig(socket_id, outline="#888")
                label.config(fg=TEXT_WHITE)

        c.bind("<Button-1>", toggle)
        label.bind("<Button-1>", toggle)

    def select_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.file_path.set(path)
            self.log_message(f"Equipped: {path}", "info")

    def log_message(self, text, tag=None):
        self.output_area.insert(tk.END, f"{text}\n", tag)
        self.output_area.see(tk.END)

    def parse_binwalk_line(self, line):
        line = line.strip()
        if not line: return
        
        # 1. Headers (DECIMAL HEX DESCRIPTION)
        if "DECIMAL" in line and "DESCRIPTION" in line:
            self.output_area.insert(tk.END, line + "\n", "header")
            self.output_area.insert(tk.END, "-"*90 + "\n", "header")
            return

        # 2. Standard Binwalk Line
        match = re.match(r'^(\d+)\s+(0x[0-9A-Fa-f]+)\s+(.*)$', line)
        if match:
            decimal, hexval, desc = match.groups()
            
            # Insert Offsets (Yellow)
            self.output_area.insert(tk.END, f"{decimal:<12}", "offset")
            self.output_area.insert(tk.END, f"{hexval:<12}", "offset")
            
            # 3. Analyze Description
            
            # First, check if the description contains ", name: "
            # This is common in Zip, Squashfs, CPIO etc.
            if ", name: " in desc:
                # Split only on the first occurrence to be safe
                info_part, filename_part = desc.split(", name: ", 1)
                
                # Insert the generic info (Gray/Green)
                tag = "info"
                if any(k in info_part.lower() for k in ["gzip", "zip", "squashfs", "filesystem"]):
                    tag = "filetype"
                self.output_area.insert(tk.END, info_part, tag)
                
                # Insert the label (Gray)
                self.output_area.insert(tk.END, ", name: ", "filename_label")
                
                # Insert the FILENAME (Cyan + Bold) <- This makes it standout!
                self.output_area.insert(tk.END, f"{filename_part}\n", "filename")
                
            else:
                # No specific name field, check for keywords for generic highlighting
                desc_tag = "info"
                if any(k in desc.lower() for k in ["gzip", "lzma", "squashfs", "zip", "png", "jpeg", "filesystem", "executable"]):
                    desc_tag = "filetype"
                self.output_area.insert(tk.END, f"{desc}\n", desc_tag)
                
        else:
            # Errors or Misc
            if "error" in line.lower() or "failed" in line.lower():
                self.output_area.insert(tk.END, line + "\n", "error")
            else:
                self.output_area.insert(tk.END, line + "\n")
        
        self.output_area.see(tk.END)

    def animate_limit_bar(self):
        if self.scanning:
            current_width = int(self.limit_bar.place_info()['width'])
            new_width = current_width + 5
            if new_width > 200: new_width = 0
            self.limit_bar.place(width=new_width)
            
            colors = ["#d6498b", "#a12f66", "#ff5ec4"]
            self.limit_bar.config(bg=colors[new_width % 3])
            
            self.root.after(50, self.animate_limit_bar)
        else:
            self.limit_bar.place(width=200)
            self.limit_bar.config(bg="#d6498b")

    def start_scan_thread(self):
        target = self.file_path.get()
        if target == "No Equipment":
            self.log_message("Miss! (No target selected)", "error")
            return

        self.cast_btn.config(state=tk.DISABLED, text="CASTING...")
        self.output_area.delete('1.0', tk.END) 
        self.log_message(f"> Cloud casts Binwalk on target!", "system")
        
        self.scanning = True
        self.animate_limit_bar()
        
        t = threading.Thread(target=self.run_binwalk, args=(target,))
        t.daemon = True
        t.start()

    def run_binwalk(self, target):
        cmd = ["binwalk"]
        if self.var_extract.get(): cmd.append("-e")
        if self.var_matryoshka.get(): cmd.append("-M")
        if self.var_entropy.get(): cmd.append("-E")
        cmd.append(target)
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in process.stdout:
                self.root.after(0, self.parse_binwalk_line, line)
            
            process.wait()
            self.root.after(0, self.scan_finished)

        except Exception as e:
             self.root.after(0, self.log_message, f"9999 DAMAGE! Error: {e}", "error")
             self.root.after(0, self.scan_finished)

    def scan_finished(self):
        self.scanning = False
        self.log_message("\n> Victory Fanfare.mp3", "system")
        self.cast_btn.config(state=tk.NORMAL, text="LIMIT BREAK")

if __name__ == "__main__":
    root = tk.Tk()
    app = FF7Binwalk(root)
    root.mainloop()
