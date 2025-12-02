import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import shlex
import webbrowser
import os
from PIL import Image, ImageTk # Requires: pip install pillow

# --- TOOL/LATERALUS Theming Constants ---
BG_COLOR = "#0a0a0a"   # Deep black
SCROLL_BG = "#0d0d0d"  # Almost black for output
INK_COLOR = "#ffd700"  # Bright golden text
TEXT_COLOR = "#ffd700" # Bright Golden
ACCENT_COLOR = "#ff0000" # Bright red accent
LINK_COLOR = "#ff6600" # Bright orange for links
FRAME_COLOR = "#1a0000" # Very dark red
BUTTON_BG = "#2d0000"  # Dark red for buttons
ENTRY_BG = "#1a1a1a"   # Dark gray for entries

# Weird ASCII Art
THIRD_EYE_ASCII = """
    ╱|、
   (˚ˎ 。7  
    |、˜〵          
    じしˍ,)ノ
"""

SPIRAL_ASCII = """
        ████▀
      ██▀   ▄██
     ██   ▄████
    ▐█▌ ██████
    ███ ██████
    ███ ██████
     ███████▀
      █████▀
        ▀▀
"""

EYE_TOP = """
╔════════════════════════════════════════════════════════════╗
║   ___     ___     ___     ___     ___     ___     ___      ║
║  (o o)   (o o)   (o o)   (o o)   (o o)   (o o)   (o o)     ║
"""

EYE_BOTTOM = """
║   \_/     \_/     \_/     \_/     \_/     \_/     \_/      ║
╚════════════════════════════════════════════════════════════╝
"""

ALEX_GREY_VIBES = """
    ▲ ▼ ▲ ▼ ▲ ▼ ▲ ▼ ▲ ▼ ▲ ▼ ▲ ▼ ▲
   ◢█████████████████████████████◣
  ◢███   ⊱ NEURAL PATHWAYS ⊰   ███◣
 ◢█████████████████████████████████◣
"""

FIBONACCI_SPIRAL = """
  ▄▄▄▄▄▄▄
 █░░░░░░█▄▄
 █░░░░░░░░░█▄
 █░░░░░░░░░░░█
 █░░1░1░2░3░█
  █░5░8░13░░█
   █░21░34░█
    ▀█░55█▀
       ▀█▀
"""

class LateralusNmapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LATERALUS :: Network Divination")
        self.root.geometry("950x950")
        
        # 1. SETUP CANVAS (The foundation)
        self.canvas = tk.Canvas(root, width=950, height=950, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # 2. LOAD BACKGROUND IMAGE WITH DIMMING
        try:
            possible_names = ["lateralus_bg.jpg", "lateralus_bg.png", "image.jpg", "image.png"]
            image_path = None
            
            for name in possible_names:
                if os.path.exists(name):
                    image_path = name
                    print(f"Loaded texture: {name}")
                    break
            
            if image_path:
                pil_image = Image.open(image_path)
                pil_image = pil_image.resize((950, 950), Image.Resampling.LANCZOS)
                
                # Dim the image to 40% brightness so text is readable
                from PIL import ImageEnhance
                enhancer = ImageEnhance.Brightness(pil_image)
                pil_image = enhancer.enhance(0.3)  # 30% brightness
                
                self.bg_photo = ImageTk.PhotoImage(pil_image)
                self.canvas.create_image(475, 475, image=self.bg_photo, anchor="center")
            else:
                print("No background image found. Using void black.")
                
        except Exception as e:
            print(f"Error loading image: {e}")

        # Store current scan target
        self.current_scan_target = ""

        # --- LAYOUT VIA CANVAS ---
        current_y = 30

        # Top Eye - with shadow for readability
        self.canvas.create_text(477, current_y+2, text=EYE_TOP, fill="#000000", font=("Courier New", 7))
        self.canvas.create_text(475, current_y, text=EYE_TOP, fill=ACCENT_COLOR, font=("Courier New", 7))
        current_y += 50

        # Title Section with shadow
        self.canvas.create_text(477, current_y+2, text="◬ ⊱ ∞ SPIRAL OUT ∞ ⊰ ◭", fill="#000000", font=("Arial", 24, "bold"))
        self.canvas.create_text(475, current_y, text="◬ ⊱ ∞ SPIRAL OUT ∞ ⊰ ◭", fill=TEXT_COLOR, font=("Arial", 24, "bold"))
        current_y += 35
        
        self.canvas.create_text(477, current_y+2, text="「 KEEP GOING 」", fill="#000000", font=("Courier New", 10, "italic"))
        self.canvas.create_text(475, current_y, text="「 KEEP GOING 」", fill=ACCENT_COLOR, font=("Courier New", 10, "italic"))
        current_y += 40

        # Side by Side Art with shadows
        self.canvas.create_text(202, current_y+2, text=SPIRAL_ASCII, fill="#000000", font=("Courier New", 8))
        self.canvas.create_text(200, current_y, text=SPIRAL_ASCII, fill=TEXT_COLOR, font=("Courier New", 8))
        
        self.canvas.create_text(477, current_y+2, text=FIBONACCI_SPIRAL, fill="#000000", font=("Courier New", 8))
        self.canvas.create_text(475, current_y, text=FIBONACCI_SPIRAL, fill=TEXT_COLOR, font=("Courier New", 8))
        
        self.canvas.create_text(752, current_y+2, text=THIRD_EYE_ASCII, fill="#000000", font=("Courier New", 8))
        self.canvas.create_text(750, current_y, text=THIRD_EYE_ASCII, fill=ACCENT_COLOR, font=("Courier New", 8))
        current_y += 90

        # Alex Grey Header with shadow
        self.canvas.create_text(477, current_y+2, text=ALEX_GREY_VIBES, fill="#000000", font=("Courier New", 7))
        self.canvas.create_text(475, current_y, text=ALEX_GREY_VIBES, fill=TEXT_COLOR, font=("Courier New", 7))
        current_y += 60

        # --- CONTROLS WITH BETTER VISIBILITY ---
        control_frame = tk.Frame(self.canvas, bg="#000000", bd=3, relief="ridge")
        
        inner_control = tk.Frame(control_frame, bg="#1a0000")
        inner_control.pack(padx=5, pady=5)
        
        tk.Label(
            inner_control, 
            text="◢ TARGET ENTITY ◣", 
            font=("Courier New", 11, "bold"), 
            bg="#1a0000", 
            fg=TEXT_COLOR
        ).grid(row=0, column=0, padx=10, pady=5)
        
        self.target_entry = tk.Entry(
            inner_control, 
            font=("Courier New", 12), 
            width=22, 
            bg=ENTRY_BG, 
            fg=TEXT_COLOR, 
            insertbackground=TEXT_COLOR, 
            relief="sunken",
            bd=2
        )
        self.target_entry.insert(0, "127.0.0.1")
        self.target_entry.grid(row=0, column=1, padx=10, pady=5)
        
        self.canvas.create_window(475, current_y, window=control_frame, anchor="center")
        current_y += 60

        # --- CHECKBOXES IN VISIBLE FRAME ---
        chk_container = tk.Frame(self.canvas, bg="#000000", bd=3, relief="ridge")
        chk_frame = tk.Frame(chk_container, bg="#1a0000")
        chk_frame.pack(padx=10, pady=10)
        
        tk.Label(
            chk_frame, 
            text="⊱ CONSCIOUSNESS PROBES ⊰", 
            font=("Courier New", 10, "bold"), 
            bg="#1a0000", 
            fg=TEXT_COLOR
        ).pack(pady=5)
        
        self.var_sv = tk.BooleanVar()
        self.var_sc = tk.BooleanVar()
        self.var_os = tk.BooleanVar()

        chk_opts = {
            "bg": "#1a0000", 
            "fg": TEXT_COLOR, 
            "selectcolor": "#000000", 
            "activebackground": "#1a0000", 
            "activeforeground": LINK_COLOR, 
            "font": ("Courier New", 10, "bold")
        }

        chk_inner = tk.Frame(chk_frame, bg="#1a0000")
        chk_inner.pack()
        
        tk.Checkbutton(chk_inner, text="▲ Version (-sV)", variable=self.var_sv, **chk_opts).pack(side=tk.LEFT, padx=15, pady=5)
        tk.Checkbutton(chk_inner, text="◆ Scripts (-sC)", variable=self.var_sc, **chk_opts).pack(side=tk.LEFT, padx=15, pady=5)
        tk.Checkbutton(chk_inner, text="● OS Detect (-O)", variable=self.var_os, **chk_opts).pack(side=tk.LEFT, padx=15, pady=5)

        self.canvas.create_window(475, current_y, window=chk_container, anchor="center")
        current_y += 80

        # --- CUSTOM ARGS & BUTTON IN VISIBLE FRAME ---
        action_container = tk.Frame(self.canvas, bg="#000000", bd=3, relief="ridge")
        action_frame = tk.Frame(action_container, bg="#1a0000")
        action_frame.pack(padx=15, pady=15)
        
        tk.Label(
            action_frame, 
            text="◢ Custom Ritual:", 
            bg="#1a0000", 
            fg=ACCENT_COLOR, 
            font=("Courier New", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        self.custom_entry = tk.Entry(
            action_frame, 
            font=("Courier New", 10), 
            width=20, 
            bg=ENTRY_BG, 
            fg=TEXT_COLOR, 
            insertbackground=TEXT_COLOR, 
            relief="sunken",
            bd=2
        )
        self.custom_entry.pack(side=tk.LEFT, padx=10)

        self.scan_button = tk.Button(
            action_frame, 
            text="⊙ OPEN THIRD EYE ⊙", 
            font=("Courier New", 12, "bold"),
            command=self.start_scan_thread,
            bg=BUTTON_BG, 
            fg=TEXT_COLOR, 
            activebackground=ACCENT_COLOR,
            activeforeground="#000000",
            relief="raised", 
            bd=4, 
            cursor="hand2",
            width=22
        )
        self.scan_button.pack(side=tk.LEFT, padx=15)

        self.canvas.create_window(475, current_y, window=action_container, anchor="center")
        current_y += 70

        # --- OUTPUT AREA ---
        self.canvas.create_text(477, current_y+2, text="▼ ▼ ▼ ∞ TRANSMISSION CHAMBER ∞ ▼ ▼ ▼", fill="#000000", font=("Courier New", 11, "bold"))
        self.canvas.create_text(475, current_y, text="▼ ▼ ▼ ∞ TRANSMISSION CHAMBER ∞ ▼ ▼ ▼", fill=ACCENT_COLOR, font=("Courier New", 11, "bold"))
        current_y += 25

        # Frame for ScrolledText with better visibility
        scroll_container = tk.Frame(self.canvas, bd=4, relief="ridge", bg="#000000")
        
        self.output_area = scrolledtext.ScrolledText(
            scroll_container, 
            width=90, 
            height=16, 
            font=("Courier New", 9, "bold"), 
            bg=SCROLL_BG, 
            fg=INK_COLOR, 
            bd=2,
            relief="sunken",
            insertbackground=TEXT_COLOR
        )
        self.output_area.pack(padx=3, pady=3)
        
        # Hyperlinks setup
        self.output_area.tag_config("hyperlink", foreground=LINK_COLOR, underline=1)
        self.output_area.tag_bind("hyperlink", "<Button-1>", self.on_link_click)
        self.output_area.tag_bind("hyperlink", "<Enter>", lambda e: self.output_area.config(cursor="hand2"))
        self.output_area.tag_bind("hyperlink", "<Leave>", lambda e: self.output_area.config(cursor="arrow"))

        self.canvas.create_window(475, current_y, window=scroll_container, anchor="n")
        current_y += 280 

        # Bottom Art with shadow
        self.canvas.create_text(477, current_y+2, text=EYE_BOTTOM, fill="#000000", font=("Courier New", 7))
        self.canvas.create_text(475, current_y, text=EYE_BOTTOM, fill=ACCENT_COLOR, font=("Courier New", 7))
        current_y += 40
        
        self.canvas.create_text(477, current_y+2, text="「 Overthinking, overanalyzing separates the body from the mind 」", fill="#000000", font=("Courier New", 9, "italic"))
        self.canvas.create_text(475, current_y, text="「 Overthinking, overanalyzing separates the body from the mind 」", fill=TEXT_COLOR, font=("Courier New", 9, "italic"))

        # Initial Print
        self.print_to_scroll("◬━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◭\n")
        self.print_to_scroll("   ⊱ Awaiting consciousness expansion... ⊰\n")
        self.print_to_scroll("   ⊱ Select your probes and open the third eye... ⊰\n")
        self.print_to_scroll("◭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◬\n\n")

    def print_to_scroll(self, text):
        self.output_area.insert(tk.END, text)
        self.output_area.see(tk.END)
        self.highlight_links()

    def highlight_links(self):
        port_pattern = r"(\d+)/tcp"
        url_pattern = r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"

        start_index = "1.0"
        while True:
            count = tk.IntVar()
            pos = self.output_area.search(port_pattern, start_index, stopindex=tk.END, count=count, regexp=True)
            if not pos: break
            end_index = f"{pos}+{count.get()}c"
            self.output_area.tag_add("hyperlink", pos, end_index)
            matched_text = self.output_area.get(pos, end_index)
            port_num = matched_text.split('/')[0]
            target_url = f"http://{self.current_scan_target}:{port_num}"
            self.output_area.tag_add(f"url_{target_url}", pos, end_index)
            start_index = end_index

        start_index = "1.0"
        while True:
            count = tk.IntVar()
            pos = self.output_area.search(url_pattern, start_index, stopindex=tk.END, count=count, regexp=True)
            if not pos: break
            end_index = f"{pos}+{count.get()}c"
            self.output_area.tag_add("hyperlink", pos, end_index)
            matched_url = self.output_area.get(pos, end_index)
            self.output_area.tag_add(f"url_{matched_url}", pos, end_index)
            start_index = end_index

    def on_link_click(self, event):
        index = self.output_area.index(f"@{event.x},{event.y}")
        tags = self.output_area.tag_names(index)
        for tag in tags:
            if tag.startswith("url_"):
                url = tag[4:]
                print(f"◬ Spiraling to: {url}")
                try:
                    webbrowser.open_new_tab(url)
                except Exception as e:
                    messagebox.showerror("⊗ Consciousness Blocked ⊗", f"Failed to open portal:\n{e}")
                break

    def start_scan_thread(self):
        target = self.target_entry.get()
        if not target:
            messagebox.showwarning("⊗ Incomplete Ritual ⊗", "A target entity must be specified!")
            return

        self.current_scan_target = target
        self.scan_button.config(state=tk.DISABLED, text="⊙ CHANNELING... ⊙")
        self.output_area.delete('1.0', tk.END)
        self.print_to_scroll(f"\n   ⊱∞⊰ ═══════════════════════════════════════════════════ ⊱∞⊰\n")
        self.print_to_scroll(f"              ◢█▓▒░ SPIRAL OUT ░▒▓█◣\n")
        self.print_to_scroll(f"              Probing entity: {target}\n")
        self.print_to_scroll(f"              ◥█▓▒░ KEEP GOING ░▒▓█◤\n")
        self.print_to_scroll(f"   ⊱∞⊰ ═══════════════════════════════════════════════════ ⊱∞⊰\n\n")

        scan_thread = threading.Thread(target=self.run_nmap, args=(target,))
        scan_thread.daemon = True
        scan_thread.start()

    def run_nmap(self, target):
        command = ["nmap"] 
        if self.var_sv.get(): command.append("-sV")
        if self.var_sc.get(): command.append("-sC")
        if self.var_os.get(): command.append("-O")
        command.append("-v")
        
        custom_args = self.custom_entry.get().strip()
        if custom_args:
            command.extend(shlex.split(custom_args))
        command.append(target)

        self.root.after(0, self.print_to_scroll, f"   ⊱ Ritual Invocation: {' '.join(command)}\n\n")

        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.root.after(0, self.print_to_scroll, output)
            self.root.after(0, self.scan_finished)
        except Exception as e:
            self.root.after(0, self.print_to_scroll, f"\n   ⊗⊗⊗ Transmission interrupted: {str(e)} ⊗⊗⊗\n")
            self.root.after(0, self.scan_finished)

    def scan_finished(self):
        self.print_to_scroll("\n   ⊱∞⊰ ═══════════════════════════════════════════════════ ⊱∞⊰\n")
        self.print_to_scroll("              ◢█▓▒░ VISION COMPLETE ░▒▓█◣\n")
        self.print_to_scroll("              Third eye remains open.\n")
        self.print_to_scroll("              Spiral out. Keep going.\n")
        self.print_to_scroll("              ◥█▓▒░ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ░▒▓█◤\n")
        self.print_to_scroll("   ⊱∞⊰ ═══════════════════════════════════════════════════ ⊱∞⊰\n")
        self.scan_button.config(state=tk.NORMAL, text="⊙ OPEN THIRD EYE ⊙")

if __name__ == "__main__":
    root = tk.Tk()
    app = LateralusNmapGUI(root)
    root.mainloop()
