# 🌀 LATERALUS :: Network Divination Scanner

<div align="center">

<img width="345" height="337" alt="Lateralus Logo" src="https://github.com/user-attachments/assets/4056633e-7e58-44de-a2b9-70239ca324dc" />

**◬ ⊱ ∞ SPIRAL OUT ∞ ⊰ ◭**  
**「 KEEP GOING 」**

*A Tool/Lateralus-themed Nmap GUI scanner featuring Alex Grey-inspired visionary art, sacred geometry, and consciousness expansion.*

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Nmap](https://img.shields.io/badge/Requires-Nmap-darkred.svg)](https://nmap.org/)

</div>

---

## ⊱ Overview ⊰

**LATERALUS :: Network Divination** is a psychedelic Nmap GUI that transforms mundane port scanning into a mystical experience. Inspired by Tool's album *Lateralus*, Alex Grey's visionary artwork, and sacred geometry, this scanner brings consciousness expansion to network reconnaissance.

### ✨ Features

- 🎨 **Visionary Background**: Alex Grey-inspired anatomical/spiritual artwork
- 🌀 **Sacred Geometry**: Fibonacci spirals, third eye symbolism, and geometric patterns
- 👁️ **Weird ASCII Art**: Eyes, spirals, and mystical symbols everywhere
- 🔗 **Clickable Port Links**: Automatically converts discovered ports into clickable HTTP links
- ⚡ **Full Nmap Integration**: All your favorite Nmap flags and custom arguments
- 🎭 **Tool Aesthetics**: Dark golden text, blood red accents, and consciousness-expanding vibes

---

## 📋 Prerequisites

### Required
- **Python 3.7+**
- **Nmap** installed and in your system PATH
  - Ubuntu/Debian: `sudo apt install nmap`
  - Arch: `sudo pacman -S nmap`
  - macOS: `brew install nmap`
  - Windows: [Download from nmap.org](https://nmap.org/download.html)

### Python Dependencies
```bash
pip install pillow
```

---

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/lateralus-scanner.git
cd lateralus-scanner
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Add background image (optional but recommended)**
   - Save your Alex Grey-style background as `lateralus_bg.jpg` or `lateralus_bg.png`
   - Place it in the same directory as the script
   - The app will auto-detect and dim it for readability

4. **Run the scanner**
```bash
python lateralus_scanner.py
```

---

## 🎮 Usage

### Basic Scan
1. Enter target IP in the **TARGET ENTITY** field
2. Select your consciousness probes (scan options):
   - **▲ Version (-sV)**: Detect service versions
   - **◆ Scripts (-sC)**: Run default NSE scripts
   - **● OS Detect (-O)**: Identify operating system
3. Click **⊙ OPEN THIRD EYE ⊙** to begin scanning

### Custom Rituals
Add custom Nmap flags in the **Custom Ritual** field:
```
-p- --min-rate 10000
-sU -p 161,162
-Pn --script vuln
```

### Clickable Ports
Discovered TCP ports automatically become clickable links:
- Click any `80/tcp`, `443/tcp`, etc. to open in browser
- URLs found in scan output are also clickable

---

## 🎨 Customization

### Change Color Scheme
Edit the constants at the top of `lateralus_scanner.py`:
```python
TEXT_COLOR = "#ffd700"   # Bright Golden
ACCENT_COLOR = "#ff0000" # Bright Red
LINK_COLOR = "#ff6600"   # Orange links
```

### Add Your Own ASCII Art
Modify the ASCII art strings:
```python
THIRD_EYE_ASCII = """
Your custom
ASCII art
here
"""
```

### Use Different Background
Replace `lateralus_bg.jpg` with any image. The script will:
- Auto-detect common image formats (jpg, png)
- Resize to fit the window
- Dim to 30% brightness for text readability

---

## 📸 Screenshots

```
   ⊱∞⊰ ═══════════════════════════════════════════════════ ⊱∞⊰
              ◢█▓▒░ SPIRAL OUT ░▒▓█◣
              Probing entity: 10.10.10.10
              ◥█▓▒░ KEEP GOING ░▒▓█◤
   ⊱∞⊰ ═══════════════════════════════════════════════════ ⊱∞⊰
```

---

## ⚠️ Disclaimer

**This tool is for educational and authorized testing purposes only.**

- Only scan networks you own or have explicit permission to test
- Unauthorized port scanning may be illegal in your jurisdiction
- The author assumes no liability for misuse of this tool

*"Overthinking, overanalyzing separates the body from the mind"*

---

## 🛠️ Technical Details

- **GUI Framework**: Tkinter with Canvas layering
- **Background Processing**: Threading for non-blocking scans
- **Image Processing**: PIL/Pillow for background dimming
- **Regex Parsing**: Real-time hyperlink detection in output
- **Process Management**: Subprocess for Nmap execution

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add more weird ASCII art
- Improve the sacred geometry
- Enhance the psychedelic experience
- Fix bugs (if you can find them in the spiral)

---

## 📜 License

MIT License - Spiral out freely

---

## 🙏 Acknowledgments

- **Tool** - For *Lateralus* and inspiring consciousness expansion
- **Alex Grey** - For visionary art that reveals the interconnectedness of all things
- **The Nmap Project** - For the legendary network scanner
- **Fibonacci** - For the spiral sequence (1, 1, 2, 3, 5, 8, 13...)

---

<div align="center">

```
    ▲ ▼ ▲ ▼ ▲ ▼ ▲ ▼ ▲ ▼ ▲ ▼ ▲ ▼ ▲
   ◢█████████████████████████████◣
  ◢███   ⊱ NEURAL PATHWAYS ⊰   ███◣
 ◢█████████████████████████████████◣

⊱ Spiral out. Keep going. ⊰
```

**Made with 👁️ and sacred geometry**

</div>
