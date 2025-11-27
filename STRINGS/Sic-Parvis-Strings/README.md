# SIC-PARVIS-STRINGS 🧭

> *"Sic Parvis Magna — Greatness from small beginnings."*

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Sic Parvis Strings** is a Python-based binary analysis tool that wraps the functionality of the `strings` command in an immersive, *Uncharted*-inspired journal interface. Designed for CTF players and digital archaeologists who want their tools to feel as adventurous as the hunt itself.

---

## 📸 The Interface

<div align="center">
  <img src="https://github.com/user-attachments/assets/4a13f449-d2ef-4198-a388-5224513dcfc5" alt="Full Journal UI" width="100%">
</div>
<br>
<div align="center">
  <img src="https://github.com/user-attachments/assets/4bd1557c-87d3-4766-b0c6-7e8348fc48e8" alt="Sidebar Detail" width="200">
</div>

---

## 🗺️ Features

* **Artifact Extraction:** Scans binary files (executables, images, dumps) and extracts human-readable ASCII strings.
* **Immersive UI:** A fully custom PyQt6 interface styled like Nathan Drake's field journal.
    * Procedural "Leather" and "Paper" textures (CSS gradients).
    * Handwritten-style menu navigation.
    * Tactile visual feedback and "taped" report aesthetics.
* **CTF Ready:** Perfect for finding flags, hidden passwords, or embedded messages in challenge files.
* **Cross-Platform:** Runs on Linux, Windows, and macOS without needing native command-line tools.
* **Export Logs:** Save your findings to a text file (`drakes_journal.txt`) for further analysis.

## 🎒 Installation

### Prerequisites
You need **Python 3** installed on your system.

### Setup
1.  Clone the repository:
    ```bash
    git clone https://github.com/AyaanBhatti-dotcom/SIC-PARVIS-STRINGS.git
    cd SIC-PARVIS-STRINGS
    ```

2.  Install the dependencies:
   

3.  Launch the journal:
    ```bash
    python drake.py
    ```

## 🔦 Usage

1.  **Launch the app.**
2.  Click **"Found Artifact..."** on the sidebar to open the file explorer.
3.  Select any file you want to analyze.
4.  Watch as the tool deciphers the "runes" (strings) onto the journal page.
5.  Click **"Update Log..."** to save the output to a text file.

## 🎨 Aesthetic Details

This tool eschews standard window decorations for a "diegetic" interface:
* **The Font Stack:** Uses `Segoe Print`, `Bradley Hand`, or `URW Chancery L` depending on your OS to maintain the handwritten look.
* **The Red Marker:** Buttons feature a "messy" red circle on hover, mimicking a marker circle drawn on a map.
* **Lighting:** Radial gradients create a vignette effect, simulating a workspace lit by a lantern or dim light.

## 🤝 Contributing

Got an idea to make it even better? Feel free to open an issue or submit a Pull Request.
* **ToDo:** Add "Search/Grep" functionality for specific flags (e.g., searching for `flag{`).

## 📜 License

This project is open source and available under the [MIT License](LICENSE).
