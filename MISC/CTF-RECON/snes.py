import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import sys
import os

# --- PIL Check ---
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class UltraTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("N E T C A T // Z E R O  U L T R A // T E R M I N A L")
        self.root.geometry("900x750")
        
        # Cool Factor: Transparency
        self.root.attributes('-alpha', 0.95)

        # --- THEME CONFIG ---
        self.colors = {
            "bg": "#0f0f0f",         
            "fg": "#e0e0e0",         
            "input_bg": "#1a1a1a",   
            "ice_blue": "#9bdcff",   
            "silver": "#b0b0b0",     
            "alert": "#ff4444",
            "dark_grey": "#444444"
        }

        self.root.configure(bg=self.colors["bg"])

        # --- BACKGROUND LAYER ---
        self.canvas = tk.Canvas(root, bg=self.colors["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        if PIL_AVAILABLE:
            self.load_images()

        # --- MAIN FRAME ---
        self.main_frame = tk.Frame(self.canvas, bg=self.colors["bg"])
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.92)

        # --- HEADER (Logo + Controls) ---
        self.top_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.top_frame.pack(fill=tk.X, pady=(0, 10))

        # Logo (Left side of header)
        if hasattr(self, 'tk_logo'):
            logo_lbl = tk.Label(self.top_frame, image=self.tk_logo, bg=self.colors["bg"], bd=0)
            logo_lbl.pack(side=tk.LEFT, padx=(0, 20))

        # Controls (Right side of header)
        ctrl_frame = tk.Frame(self.top_frame, bg=self.colors["bg"])
        ctrl_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # IP/Port Inputs
        self.make_input(ctrl_frame, "BIND IP", "0.0.0.0", 14)
        self.make_input(ctrl_frame, "PORT", "4444", 8)

        # Action Button
        self.listen_btn = tk.Button(ctrl_frame, text="INITIATE", command=self.toggle_listener,
                                    bg=self.colors["ice_blue"], fg="#000000", 
                                    font=("Helvetica", 9, "bold"), bd=0, padx=15)
        self.listen_btn.pack(side=tk.LEFT, padx=10)

        # --- THE TERMINAL WINDOW ---
        # Frame for the glowing border effect
        self.term_border = tk.Frame(self.main_frame, bg=self.colors["ice_blue"], padx=1, pady=1)
        self.term_border.pack(fill=tk.BOTH, expand=True)

        self.term = scrolledtext.ScrolledText(self.term_border, bg="#050505", fg=self.colors["ice_blue"],
                                              insertbackground="white", # The cursor color
                                              font=("Consolas", 11), bd=0, selectbackground="#333")
        self.term.pack(fill=tk.BOTH, expand=True)
        
        # Tags for colors
        self.term.tag_config("banner", foreground=self.colors["ice_blue"])
        self.term.tag_config("system", foreground=self.colors["silver"])
        self.term.tag_config("cryptic", foreground=self.colors["dark_grey"])

        # TERMINAL LOGIC
        self.print_banner()

        # Key Bindings
        self.term.bind("<Return>", self.on_enter)
        self.term.bind("<Key>", self.on_key_press)
        self.term.bind("<BackSpace>", self.on_backspace)
        
        # State Variables
        self.server_socket = None
        self.client_socket = None
        self.is_listening = False
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def print_banner(self):
        # Slant Style ASCII
        art = r"""
   __  __  ___  _   _ ____ _____ _____ ____      ____    _  _____ 
  |  \/  |/ _ \| \ | / ___|_   _| ____|  _ \    / ___|  / \|_   _|
  | |\/| | | | |  \| \___ \ | | |  _| | |_) |  | |     / _ \ | |  
  | |  | | |_| | |\  |___) || | | |___|  _ <   | |___ / ___ \| |  
  |_|  |_|\___/|_| \_|____/ |_| |_____|_| \_\   \____/_/   \_\_|  
        """
        self.term.insert(tk.END, "Initializing ZERO ULTRA Kernel...\n", "system")
        self.term.insert(tk.END, art, "banner")
        self.term.insert(tk.END, "\nSystem Ready. Waiting for connection...\n", "system")
        self.term.insert(tk.END, ">>> ")
        
        # IMPORTANT: This locks the banner so you can't delete it
        self.term.mark_set("input_limit", "end-1c")
        self.term.mark_gravity("input_limit", tk.LEFT)

    def make_input(self, parent, label, default, width):
        f = tk.Frame(parent, bg=self.colors["bg"])
        f.pack(side=tk.LEFT, padx=5)
        tk.Label(f, text=label, bg=self.colors["bg"], fg=self.colors["silver"], font=("Arial", 7)).pack(anchor="w")
        e = tk.Entry(f, width=width, bg="#222", fg="white", bd=0, insertbackground="white")
        e.insert(0, default)
        e.pack()
        # Store reference
        if label == "BIND IP": self.ip_entry = e
        else: self.port_entry = e

    def load_images(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Background
        bg_path = os.path.join(script_dir, "background.png")
        if os.path.exists(bg_path):
            try:
                bg_img = Image.open(bg_path).resize((1920, 1080), Image.Resampling.LANCZOS)
                self.tk_bg = ImageTk.PhotoImage(bg_img)
                self.canvas.create_image(0, 0, image=self.tk_bg, anchor="nw")
            except: pass
        # Logo
        logo_path = os.path.join(script_dir, "claw_logo.png")
        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                # Resize specifically for the header
                img.thumbnail((60, 60), Image.Resampling.LANCZOS)
                self.tk_logo = ImageTk.PhotoImage(img)
            except: pass

    # --- TERMINAL EVENT HANDLERS ---

    def on_key_press(self, event):
        """Prevent user from typing in the history area"""
        if self.term.compare("insert", "<", "input_limit"):
            self.term.mark_set("insert", "end")
            return "break"
        return None

    def on_backspace(self, event):
        """Prevent deleting the prompt or history"""
        if self.term.compare("insert", "<=", "input_limit"):
            return "break"
        return None

    def on_enter(self, event):
        """Handle command sending"""
        # 1. Get text from limit to end
        cmd_text = self.term.get("input_limit", "end-1c")
        
        # 2. Send to socket (If connected)
        if self.client_socket:
            try:
                self.client_socket.send((cmd_text + "\n").encode('utf-8'))
            except:
                self.system_msg("[!] Connection Lost")
                self.stop_listening()
        
        # 3. Add newline visually
        self.term.insert("end", "\n")
        
        # 4. Update the limit so this command becomes 'history'
        self.term.mark_set("input_limit", "end-1c")
        self.term.see(tk.END)
        return "break" # Prevent default newline behavior

    def system_msg(self, msg):
        """Write system messages (safe to run from threads)"""
        self.term.insert(tk.END, f"\n{msg}\n", "system")
        self.term.see(tk.END)
        self.term.mark_set("input_limit", "end-1c")

    def socket_write(self, text):
        """Write raw socket output to terminal"""
        self.term.insert(tk.END, text)
        self.term.see(tk.END)
        # IMPORTANT: Move the input limit forward so user types AFTER the output
        self.term.mark_set("input_limit", "end-1c")

    # --- NETWORKING LOGIC ---

    def toggle_listener(self):
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()

    def start_listening(self):
        try:
            ip = self.ip_entry.get()
            port = int(self.port_entry.get())
            
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((ip, port))
            self.server_socket.listen(1)
            
            self.is_listening = True
            self.listen_btn.config(text="ABORT", bg=self.colors["alert"])
            # Clear screen except for banner? No, let's just append.
            self.system_msg(f"[*] LISTENING ON {ip}:{port}...")
            
            threading.Thread(target=self.accept_connection, daemon=True).start()
        except Exception as e:
            self.system_msg(f"[!] ERROR: {e}")

    def accept_connection(self):
        try:
            client, addr = self.server_socket.accept()
            self.client_socket = client
            self.root.after(0, lambda: self.system_msg(f"[+] UPLINK ESTABLISHED: {addr[0]}"))
            self.receive_data()
        except: pass

    def receive_data(self):
        while self.is_listening and self.client_socket:
            try:
                data = self.client_socket.recv(4096)
                if not data: break
                text = data.decode('utf-8', errors='ignore')
                # GUI updates must happen on main thread
                self.root.after(0, lambda t=text: self.socket_write(t))
            except: break
        self.root.after(0, self.stop_listening)

    def stop_listening(self):
        self.is_listening = False
        if self.client_socket: 
            try: self.client_socket.close() 
            except: pass
        if self.server_socket: 
            try: self.server_socket.close() 
            except: pass
            
        self.listen_btn.config(text="INITIATE", bg=self.colors["ice_blue"])
        self.system_msg("[*] SESSION TERMINATED")

    def on_close(self):
        self.stop_listening()
        self.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = UltraTerminal(root)
    root.mainloop()
