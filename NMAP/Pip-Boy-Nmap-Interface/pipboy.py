import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import shlex
import webbrowser
import sys
import os

# --- Pip-Boy Color Palette ---
FNV_AMBER = "#ffb642" # The main glowing amber text color
FNV_DARK_AMBER = "#b07b2c" # For dimmed or secondary text
FNV_BG = "#1a1612" # The dark background of the screen
FNV_SCREEN_GLOW = "#2a241d" # A slightly lighter background for the screen area
LINK_COLOR = "#20c20e" # Bright green for clickable links
FONT_MAIN = ("Consolas", 11)
FONT_HEADER = ("Consolas", 14, "bold")

class PipBoyNmapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RobCo Pip-Boy 3000 - Term-Link")
        self.root.geometry("900x700")
        self.root.configure(bg=FNV_BG)
        self.root.resizable(False, False)

        self.current_scan_target = ""

        # --- Main Pip-Boy Screen Frame ---
        # This frame represents the actual glowing screen area.
        self.screen_frame = tk.Frame(
            root,
            bg=FNV_SCREEN_GLOW,
            bd=4,
            relief="ridge", # A ridge border gives it a slight 3D screen look
            highlightbackground=FNV_DARK_AMBER,
            highlightcolor=FNV_AMBER,
            highlightthickness=2
        )
        self.screen_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # --- Top Status Bar (mimics the top bar in the image) ---
        top_bar = tk.Frame(self.screen_frame, bg=FNV_SCREEN_GLOW)
        top_bar.pack(fill="x", pady=(10, 5), padx=10)

        # A line to separate the top bar
        tk.Frame(top_bar, height=2, bg=FNV_AMBER).pack(fill="x", side=tk.BOTTOM)

        tk.Label(
            top_bar,
            text="ROBCO TERMLINK PROTOCOL",
            font=FONT_HEADER,
            bg=FNV_SCREEN_GLOW,
            fg=FNV_AMBER
        ).pack(side=tk.LEFT)

        tk.Label(
            top_bar,
            text="> STATUS: UNAUTHORIZED",
            font=FONT_MAIN,
            bg=FNV_SCREEN_GLOW,
            fg=FNV_DARK_AMBER
        ).pack(side=tk.RIGHT)

        # --- Middle Content Area ---
        content_frame = tk.Frame(self.screen_frame, bg=FNV_SCREEN_GLOW)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Left Panel (Inputs & Options) ---
        left_panel = tk.Frame(content_frame, bg=FNV_SCREEN_GLOW)
        left_panel.pack(side=tk.LEFT, fill="y", padx=(0, 10))

        # Target Input
        tk.Label(
            left_panel,
            text="TARGET DESIG:",
            font=FONT_HEADER,
            bg=FNV_SCREEN_GLOW,
            fg=FNV_AMBER,
            anchor="w"
        ).pack(fill="x", pady=(0, 5))

        self.target_entry = tk.Entry(
            left_panel,
            font=FONT_HEADER,
            bg=FNV_BG,
            fg=FNV_AMBER,
            insertbackground=FNV_AMBER,
            relief="flat",
            bd=5
        )
        self.target_entry.pack(fill="x", pady=(0, 15))
        self.target_entry.insert(0, "127.0.0.1")

        # Scan Modules (V.A.T.S. style)
        modules_frame = tk.LabelFrame(
            left_panel,
            text=" [ SCAN MODULES ] ",
            font=FONT_MAIN,
            bg=FNV_SCREEN_GLOW,
            fg=FNV_AMBER,
            bd=2,
            relief="solid"
        )
        modules_frame.pack(fill="x", pady=10)

        self.var_sv = tk.BooleanVar()
        self.var_sc = tk.BooleanVar()
        self.var_os = tk.BooleanVar()

        chk_options = {
            "bg": FNV_SCREEN_GLOW,
            "fg": FNV_AMBER,
            "selectcolor": FNV_BG,
            "activebackground": FNV_SCREEN_GLOW,
            "activeforeground": FNV_AMBER,
            "font": FONT_MAIN,
            "anchor": "w"
        }

        tk.Checkbutton(modules_frame, text="VERSION_CHECK (-sV)", variable=self.var_sv, **chk_options).pack(fill="x", padx=5, pady=2)
        tk.Checkbutton(modules_frame, text="SCRIPT_EXEC (-sC)", variable=self.var_sc, **chk_options).pack(fill="x", padx=5, pady=2)
        tk.Checkbutton(modules_frame, text="OS_FINGERPRINT (-O)", variable=self.var_os, **chk_options).pack(fill="x", padx=5, pady=2)

        # Manual Override
        tk.Label(
            left_panel,
            text="MANUAL_OVERRIDE:",
            font=FONT_MAIN,
            bg=FNV_SCREEN_GLOW,
            fg=FNV_DARK_AMBER,
            anchor="w"
        ).pack(fill="x", pady=(15, 5))

        self.custom_entry = tk.Entry(
            left_panel,
            font=FONT_MAIN,
            bg=FNV_BG,
            fg=FNV_AMBER,
            insertbackground=FNV_AMBER,
            relief="flat",
            bd=5
        )
        self.custom_entry.pack(fill="x")
        self.custom_entry.insert(0, "-v")


        # --- Right Panel (Output) ---
        right_panel = tk.Frame(content_frame, bg=FNV_SCREEN_GLOW)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Output Label
        tk.Label(
            right_panel,
            text="DATA_BUFFER:",
            font=FONT_HEADER,
            bg=FNV_SCREEN_GLOW,
            fg=FNV_AMBER,
            anchor="w"
        ).pack(fill="x", pady=(0, 5))

        # ScrolledText for output
        self.output_area = scrolledtext.ScrolledText(
            right_panel,
            width=50,
            height=20,
            font=FONT_MAIN,
            bg=FNV_BG,
            fg=FNV_AMBER,
            bd=0,
            cursor="xterm",
            highlightthickness=0
        )
        self.output_area.pack(fill=tk.BOTH, expand=True)

        self.output_area.tag_config("hyperlink", foreground=LINK_COLOR, underline=1)
        self.output_area.tag_bind("hyperlink", "<Button-1>", self.on_link_click)
        self.output_area.tag_bind("hyperlink", "<Enter>", lambda e: self.output_area.config(cursor="hand2"))
        self.output_area.tag_bind("hyperlink", "<Leave>", lambda e: self.output_area.config(cursor="xterm"))

        # --- Bottom Navigation Bar ---
        bottom_bar = tk.Frame(self.screen_frame, bg=FNV_SCREEN_GLOW)
        bottom_bar.pack(fill="x", side=tk.BOTTOM, pady=(5, 10), padx=10)
        
        # A line to separate the bottom bar
        tk.Frame(bottom_bar, height=2, bg=FNV_AMBER).pack(fill="x", side=tk.TOP, pady=(0,10))

        # The "Initiate Scan" button, styled like a Pip-Boy tab
        self.scan_button = tk.Button(
            bottom_bar,
            text="[ INITIATE SCAN ]",
            font=FONT_HEADER,
            command=self.start_scan_thread,
            bg=FNV_SCREEN_GLOW,
            fg=FNV_AMBER,
            activebackground=FNV_AMBER,
            activeforeground=FNV_BG,
            relief="flat",
            bd=0,
            cursor="cross",
            padx=20,
            pady=5
        )
        self.scan_button.pack()
        
        self.print_to_screen("Welcome to RobCo Term-Link.\n> System Ready.\n> Waiting for input...\n")

    def print_to_screen(self, text):
        self.output_area.insert(tk.END, text)
        self.output_area.see(tk.END)
        self.highlight_links()

    def highlight_links(self):
        port_pattern = r"(\d+)/tcp"
        url_pattern = r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"

        for pattern, is_port in [(port_pattern, True), (url_pattern, False)]:
            start_index = "1.0"
            while True:
                count = tk.IntVar()
                pos = self.output_area.search(pattern, start_index, stopindex=tk.END, count=count, regexp=True)
                if not pos: break
                end_index = f"{pos}+{count.get()}c"
                
                self.output_area.tag_add("hyperlink", pos, end_index)
                matched_text = self.output_area.get(pos, end_index)
                
                if is_port:
                    port_num = matched_text.split('/')[0]
                    target_url = f"http://{self.current_scan_target}:{port_num}"
                else:
                    target_url = matched_text
                    
                self.output_area.tag_add(f"url_{target_url}", pos, end_index)
                start_index = end_index

    def on_link_click(self, event):
        index = self.output_area.index(f"@{event.x},{event.y}")
        tags = self.output_area.tag_names(index)
        for tag in tags:
            if tag.startswith("url_"):
                url = tag[4:]
                try:
                    try:
                        webbrowser.get('firefox').open_new_tab(url)
                    except webbrowser.Error:
                        webbrowser.open_new_tab(url)
                except Exception as e:
                    messagebox.showerror("Network Error", f"Link corrupted:\n{e}")
                break

    def start_scan_thread(self):
        target = self.target_entry.get()
        if not target:
            messagebox.showwarning("Input Error", "TARGET PARAMETER REQUIRED")
            return

        self.current_scan_target = target
        self.scan_button.config(state=tk.DISABLED, text="[ PROCESSING... ]", fg=FNV_DARK_AMBER)
        self.output_area.delete('1.0', tk.END)
        self.print_to_screen(f"> INITIATING PROTOCOL ON {target}...\n")

        scan_thread = threading.Thread(target=self.run_nmap, args=(target,))
        scan_thread.daemon = True
        scan_thread.start()

    def run_nmap(self, target):
        command = ["nmap"] 
        if self.var_sv.get(): command.append("-sV")
        if self.var_sc.get(): command.append("-sC")
        if self.var_os.get(): command.append("-O")
        
        custom_args = self.custom_entry.get().strip()
        if custom_args:
            command.extend(shlex.split(custom_args))
            
        command.append(target)

        self.root.after(0, self.print_to_screen, f"> Command: {' '.join(command)}\n\n")

        try:
            # Use a startupinfo to hide the console window on Windows
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                startupinfo=startupinfo
            )

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.root.after(0, self.print_to_screen, output)
            
            self.root.after(0, self.scan_finished)

        except Exception as e:
            self.root.after(0, self.print_to_screen, f"\n[!] CRITICAL FAILURE: {str(e)}")
            self.root.after(0, self.scan_finished)

    def scan_finished(self):
        self.print_to_screen("\n> PROCESS COMPLETE.")
        self.scan_button.config(state=tk.NORMAL, text="[ INITIATE SCAN ]", fg=FNV_AMBER)

if __name__ == "__main__":
    root = tk.Tk()
    app = PipBoyNmapGUI(root)
    root.mainloop()
