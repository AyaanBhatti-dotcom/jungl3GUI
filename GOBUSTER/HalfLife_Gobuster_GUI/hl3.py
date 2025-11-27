import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading
import sys
import os
import re
import glob
import webbrowser
from urllib.parse import urlparse
import time

# Check if we are on Linux/Mac for PTY support
try:
    import pty
    HAS_PTY = True
except ImportError:
    HAS_PTY = False # Windows users fall back to standard pipes

# --- Black Mesa Color Palette ---
BM_BG_DARK = "#121212"
BM_BG_GRAY = "#2b2b2b"
BM_ORANGE = "#ffb600"
BM_GREEN = "#95c44f"
BM_TEXT_WHITE = "#e0e0e0"
BM_ALERT = "#ff3333"

# --- Fonts ---
TITLE_FONT = ("Verdana", 16, "bold") 
LABEL_FONT = ("Verdana", 9, "bold")
TERM_FONT = ("Consolas", 10)
BTN_FONT = ("Trebuchet MS", 11, "bold")

class AutocompleteEntry(tk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<Tab>", self.autocomplete)

    def autocomplete(self, event):
        current_text = self.get()
        check_path = os.path.expanduser(current_text)
        dirname, basename = os.path.split(check_path)
        if not dirname: dirname = "."
        search_pattern = os.path.join(dirname, basename + "*")
        matches = glob.glob(search_pattern)
        if not matches: return "break"
        
        completion = ""
        if len(matches) == 1:
            completion = matches[0]
            if os.path.isdir(completion): completion += os.sep
        else:
            completion = os.path.commonprefix(matches)

        self.delete(0, tk.END)
        self.insert(0, completion)
        self.icursor(tk.END) 
        self.xview_moveto(1) 
        return "break"

class BlackMesaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Black Mesa Network Tool [v 4.0 - Live Feed]")
        self.root.geometry("1050x800") 
        self.root.configure(bg=BM_BG_DARK)
        self.setup_styles()
        
        self.current_process = None
        self.master_fd = None
        self.hits_found = 0
        self.is_scanning = False
        self.total_words = 0

        # --- Top Header ---
        header_frame = tk.Frame(root, bg=BM_BG_DARK)
        header_frame.pack(fill=tk.X, pady=(15, 10), padx=20)
        tk.Label(header_frame, text="BLACK MESA", font=TITLE_FONT, bg=BM_BG_DARK, fg=BM_TEXT_WHITE).pack(anchor="w")
        tk.Label(header_frame, text="RESEARCH FACILITY // SECTOR 7G // NETWORK ANALYSIS", font=("Verdana", 7), bg=BM_BG_DARK, fg=BM_ORANGE).pack(anchor="w")
        tk.Frame(root, bg=BM_ORANGE, height=3).pack(fill=tk.X, padx=20, pady=(0, 15))

        # --- Main Layout ---
        container = tk.Frame(root, bg=BM_BG_DARK)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        # === LEFT PANEL ===
        controls_frame = tk.Frame(container, bg=BM_BG_GRAY, bd=2, relief=tk.RAISED)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15), ipadx=10, ipady=10)

        tk.Label(controls_frame, text=":: CONFIGURATION ::", font=LABEL_FONT, bg=BM_BG_GRAY, fg=BM_ORANGE).pack(pady=(10, 20))

        # Target
        self.create_label(controls_frame, "TARGET SPECIMEN (URL):")
        self.target_entry = tk.Entry(controls_frame, font=TERM_FONT, bg="#111", fg=BM_GREEN, insertbackground=BM_GREEN, bd=2, relief=tk.SUNKEN, width=40)
        self.target_entry.pack(fill=tk.X, padx=10, pady=(0, 15))
        self.target_entry.insert(0, "http://")

        # Wordlist
        self.create_label(controls_frame, "DATA DICTIONARY:")
        wl_frame = tk.Frame(controls_frame, bg=BM_BG_GRAY)
        wl_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.wordlist_entry = AutocompleteEntry(wl_frame, font=TERM_FONT, bg="#111", fg=BM_GREEN, insertbackground=BM_GREEN, bd=2, relief=tk.SUNKEN, width=40)
        self.wordlist_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(wl_frame, text="...", font=LABEL_FONT, bg="#444", fg=BM_TEXT_WHITE, command=self.browse_wordlist, width=3).pack(side=tk.RIGHT, padx=(5,0))

        tk.Frame(controls_frame, height=10, bg=BM_BG_GRAY).pack()

        # Buttons
        self.scan_btn = tk.Button(controls_frame, text="INITIATE RESONANCE", font=BTN_FONT, 
                                  bg=BM_ORANGE, fg="#000", activebackground=BM_GREEN,
                                  command=self.start_scan)
        self.scan_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(5, 15))
        
        self.abort_btn = tk.Button(controls_frame, text="ABORT SEQUENCE", font=BTN_FONT, 
                                   bg="#444", fg="#888", state=tk.DISABLED,
                                   command=self.abort_scan)
        self.abort_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(5, 5))

        # Progress Bar
        self.progress = ttk.Progressbar(controls_frame, mode='indeterminate', style="Hazard.Horizontal.TProgressbar")
        self.progress.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))
        
        # --- Live Feed Stats ---
        self.stats_frame = tk.Frame(controls_frame, bg=BM_BG_GRAY)
        self.stats_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(5,0))

        self.live_word_var = tk.StringVar(value="[ PROCESSED: 0 ]")
        tk.Label(self.stats_frame, textvariable=self.live_word_var, font=("Consolas", 10, "bold"), bg=BM_BG_GRAY, fg=BM_ORANGE, anchor="w").pack(fill=tk.X)

        self.total_target_var = tk.StringVar(value="[ TOTAL TARGETS: -- ]")
        tk.Label(self.stats_frame, textvariable=self.total_target_var, font=("Consolas", 9), bg=BM_BG_GRAY, fg="#888", anchor="w").pack(fill=tk.X)

        self.status_var = tk.StringVar(value="SYSTEM: STANDBY")
        tk.Label(controls_frame, textvariable=self.status_var, font=("Verdana", 8), bg=BM_BG_GRAY, fg=BM_TEXT_WHITE, anchor="w").pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 5))

        # === RIGHT PANEL ===
        grid_frame = tk.Frame(container, bg=BM_BG_DARK)
        grid_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        top_bar = tk.Frame(grid_frame, bg=BM_BG_DARK)
        top_bar.pack(fill=tk.X, pady=(0,5))
        tk.Label(top_bar, text=">_ ANOMALOUS SIGNALS DETECTED", font=("Verdana", 8), bg=BM_BG_DARK, fg=BM_GREEN).pack(side=tk.LEFT)
        self.anomalies_var = tk.StringVar(value="[ ANOMALIES: 0 ]")
        tk.Label(top_bar, textvariable=self.anomalies_var, font=("Verdana", 8, "bold"), bg=BM_BG_DARK, fg=BM_ORANGE).pack(side=tk.RIGHT)

        columns = ("path", "status", "size")
        self.tree = ttk.Treeview(grid_frame, columns=columns, show="headings", style="BlackMesa.Treeview")
        scrollbar = ttk.Scrollbar(grid_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree.heading("path", text="DIRECTORY PATH")
        self.tree.heading("status", text="STATUS CODE")
        self.tree.heading("size", text="RESPONSE SIZE")
        self.tree.column("path", width=350, anchor="w")
        self.tree.column("status", width=100, anchor="center")
        self.tree.column("size", width=100, anchor="center")
        self.tree.bind("<Double-1>", self.on_double_click)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("BlackMesa.Treeview", background="black", foreground=BM_GREEN, fieldbackground="black", font=TERM_FONT, rowheight=25, borderwidth=0)
        style.configure("BlackMesa.Treeview.Heading", background=BM_BG_GRAY, foreground=BM_ORANGE, font=("Verdana", 9, "bold"), relief="flat")
        style.map("BlackMesa.Treeview", background=[('selected', BM_ORANGE)], foreground=[('selected', 'black')])
        style.configure("Hazard.Horizontal.TProgressbar", troughcolor="#111", background=BM_ORANGE, thickness=10)

    def create_label(self, parent, text):
        tk.Label(parent, text=text, font=("Verdana", 8), bg=BM_BG_GRAY, fg=BM_TEXT_WHITE, anchor="w").pack(fill=tk.X, padx=10, pady=(0, 2))

    def browse_wordlist(self):
        filename = filedialog.askopenfilename(title="Load Data Dictionary")
        if filename:
            self.wordlist_entry.delete(0, tk.END)
            self.wordlist_entry.insert(0, filename)
            self.wordlist_entry.icursor(tk.END)
            self.wordlist_entry.xview_moveto(1)
            self.count_words_thread(filename)

    def count_words_thread(self, filepath):
        threading.Thread(target=self.count_words, args=(filepath,), daemon=True).start()

    def count_words(self, filepath):
        try:
            self.total_target_var.set("[ TARGETS: Counting... ]")
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                self.total_words = sum(1 for _ in f)
            self.total_target_var.set(f"[ TOTAL TARGETS: {self.total_words:,} ]")
        except:
            self.total_target_var.set("[ TARGETS: ERROR ]")

    def start_scan(self):
        target = self.target_entry.get().strip()
        wordlist = self.wordlist_entry.get().strip()

        if not target or target == "http://":
            messagebox.showwarning("Access Denied", "Target Specimen Invalid.")
            return
        if not wordlist:
            messagebox.showwarning("Data Missing", "Dictionary File Required.")
            return

        for item in self.tree.get_children(): self.tree.delete(item)
        self.hits_found = 0
        self.anomalies_var.set(f"[ ANOMALIES: 0 ]")
        self.live_word_var.set(f"[ PROCESSED: 0 ]")
        
        self.scan_btn.config(state=tk.DISABLED, text="SCANNING...", bg="#555")
        self.abort_btn.config(state=tk.NORMAL, bg=BM_ALERT, fg="white")
        self.status_var.set("SYSTEM: PROCESSING DATA...")
        self.progress.start(10)
        
        if self.total_words == 0:
            self.count_words_thread(wordlist)

        thread = threading.Thread(target=self.run_gobuster, args=(target, wordlist))
        thread.daemon = True
        thread.start()

    def abort_scan(self):
        if self.current_process:
            self.status_var.set("SYSTEM: ABORTING SEQUENCE...")
            try: self.current_process.terminate()
            except: pass

    def run_gobuster(self, target, wordlist):
        command = ["gobuster", "dir", "-u", target, "-w", wordlist, "--no-error", "--no-color"]
        print(f"[DEBUG] Running command: {' '.join(command)}")

        try:
            # --- PLATFORM SPECIFIC EXECUTION ---
            if HAS_PTY:
                # LINUX: Use PTY to force Gobuster to think it's in a terminal
                # This makes it output the "Progress: 123/456" lines
                master, slave = pty.openpty()
                self.master_fd = master
                
                self.current_process = subprocess.Popen(
                    command,
                    stdout=slave,
                    stderr=slave, # Gobuster outputs progress to stderr usually
                    close_fds=True
                )
                os.close(slave) # Close slave in parent
                
                # Read from the MASTER FD
                self.read_from_pty(master)
                
            else:
                # WINDOWS: Fallback to standard pipe (Progress bar likely won't show)
                self.current_process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1
                )
                self.read_from_pipe(self.current_process.stdout)

            # Cleanup
            self.current_process.wait()
            if self.master_fd:
                try: os.close(self.master_fd)
                except: pass

            if self.current_process.returncode == 0:
                 self.root.after(0, self.scan_finished, "SEQUENCE COMPLETE", BM_ORANGE)
            else:
                 self.root.after(0, self.scan_finished, "SEQUENCE ABORTED", BM_ALERT)

        except Exception as e:
             print(f"[ERROR] {e}")
             self.root.after(0, self.scan_error, f"SYSTEM FAILURE: {e}")
        finally:
            self.current_process = None

    def read_from_pty(self, fd):
        """Reads raw bytes from the pseudo-terminal."""
        regex_result = re.compile(r"^(\S+)(?:\s+\(Status:\s*(\d+)\))?.*?\[Size:\s*(\d+)\](?:\s+\[-->\s*(.+)\])?")
        regex_progress = re.compile(r"Progress:\s+(\d+)")

        buffer = ""
        while True:
            try:
                # Read 1024 bytes at a time
                data = os.read(fd, 1024)
                if not data: break
                
                # Decode bytes to string (ignore errors for safety)
                text_chunk = data.decode('utf-8', errors='ignore')
                
                # Process the chunk
                # We need to handle \r (carriage return) which updates the progress bar
                for char in text_chunk:
                    if char == '\r' or char == '\n':
                        if not buffer: continue
                        
                        # CLEAN BUFFER: Remove ANSI escape codes (color codes)
                        clean_line = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', buffer)
                        
                        # CHECK FOR PROGRESS
                        prog_match = regex_progress.search(clean_line)
                        if prog_match:
                            current = int(prog_match.group(1))
                            self.root.after(0, self.update_live_count, current)
                        
                        # CHECK FOR HITS
                        else:
                            match = regex_result.search(clean_line)
                            if match:
                                raw_path = match.group(1)
                                status = match.group(2)
                                size = match.group(3)
                                redirect_url = match.group(4)
                                
                                final_path = raw_path
                                if redirect_url:
                                    try:
                                        parsed = urlparse(redirect_url)
                                        if parsed.path: final_path = parsed.path
                                    except: pass
                                    if not status: status = "REDIRECT"
                                if not status: status = "200"

                                self.root.after(0, self.add_row, final_path, status, size)
                        
                        buffer = ""
                    else:
                        buffer += char

            except OSError:
                break # Process exited

    def read_from_pipe(self, pipe):
        """Fallback reader for Windows"""
        regex_result = re.compile(r"^(\S+)(?:\s+\(Status:\s*(\d+)\))?.*?\[Size:\s*(\d+)\](?:\s+\[-->\s*(.+)\])?")
        for line in pipe:
            line = line.strip()
            match = regex_result.search(line)
            if match:
                self.root.after(0, self.add_row, match.group(1), match.group(2), match.group(3))

    def update_live_count(self, count):
        self.live_word_var.set(f"[ PROCESSED: {count:,} ]")

    def add_row(self, path, status, size):
        self.tree.insert("", tk.END, values=(path, status, size))
        self.hits_found += 1
        self.anomalies_var.set(f"[ ANOMALIES: {self.hits_found} ]")

    def on_double_click(self, event):
        item = self.tree.selection()
        if item:
            path = self.tree.item(item[0], "values")[0]
            if path.startswith("http"): webbrowser.open(path)
            else:
                base_url = self.target_entry.get().strip()
                full_url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
                webbrowser.open(full_url)

    def scan_finished(self, message, color):
        self.progress.stop()
        self.status_var.set(f"SYSTEM: {message}")
        self.scan_btn.config(state=tk.NORMAL, text="INITIATE RESONANCE", bg=BM_ORANGE)
        self.abort_btn.config(state=tk.DISABLED, bg="#444", fg="#888")

    def scan_error(self, message):
        self.progress.stop()
        self.status_var.set("SYSTEM: ERROR DETECTED")
        self.scan_btn.config(state=tk.NORMAL, text="INITIATE RESONANCE", bg=BM_ORANGE)
        self.abort_btn.config(state=tk.DISABLED, bg="#444", fg="#888")
        messagebox.showerror("System Failure", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackMesaGUI(root)
    root.mainloop()
