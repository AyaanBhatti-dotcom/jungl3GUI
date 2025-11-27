<div align="center">

# ⚔️ GARDEN FIELD EDITOR v8.0 ⚔️

**The Standard Issue Text Editor for SeeD Operatives**

<!-- Main Interface -->
<img width="700" alt="FF8 Nano Editor Main Interface" src="https://github.com/user-attachments/assets/375775e1-6585-4f5c-b658-0b055c7f4f3b" />

<br />

<!-- Menu Detail -->
<img width="300" alt="FF8 Nano Editor Menu Detail" src="https://github.com/user-attachments/assets/0c102c0e-1433-4429-9ac8-6956e2ac8f3b" />

<br />

> *"Orders are orders. Write the code, save the buffer, don't look back."*

</div>

## 🏰 About The Project

**GARDEN FIELD EDITOR** is a Python-based text editor that replicates the functionality of GNU nano but is skinned to match the sleek, gunmetal-grey interface of **Final Fantasy VIII**.

Designed for SeeD candidates who need to edit config files in the field while maintaining immersion. It features a responsive "Junction" menu system, CRT scanline overlays, and the iconic high-contrast palette of Balamb Garden's terminals.

## ✨ Features

* **Gunblade Grey Aesthetic:** A smooth gradient background (`#1e2024` to `#3a3e45`) that mimics the PS1 menu shading.
* **Junction Menu System:** The bottom command bar is laid out like the FF8 Battle Menu.
    * **JUNCTION:** Save File (`^O`)
    * **SCAN:** Open File (`^R`)
    * **RETREAT:** Exit Editor (`^X`)
* **CRT Scanlines:** Subtle horizontal lines overlay the entire interface for that 1999 terminal feel.
* **Nano Keybindings:** Fully supports standard nano shortcuts, so your muscle memory remains intact.
* **Dynamic Status:** The header tracks filename and modification status (turning **RED** when unsaved).

## 🎮 Junction System (Controls)

The interface maps standard text editor functions to SeeD combat protocols:

| Command | FF8 Protocol | Action |
| :--- | :--- | :--- |
| `Ctrl` + `O` | **JUNCTION** | Save the current buffer to disk. |
| `Ctrl` + `R` | **SCAN** | Open a file browser to read new data. |
| `Ctrl` + `X` | **RETREAT** | Close the terminal (prompts save if modified). |
| `Ctrl` + `K` | **CARD** | Cut the current line (Modify Card). |
| `Ctrl` + `U` | **REVIVE** | Paste the clipboard content (Life). |
| `Ctrl` + `G` | **TUTORIAL** | Open the help dialog. |

## ⚙️ Installation & Usage

1.  **Clone the Repository:**
    ```sh
    git clone [https://github.com/YOUR_USERNAME/FF8_Nano_Editor.git](https://github.com/YOUR_USERNAME/FF8_Nano_Editor.git)
    ```

2.  **Navigate to Field Directory:**
    ```sh
    cd FF8_Nano_Editor
    ```

3.  **Initialize Terminal:**
    ```sh
    python ff8_nano.py
    ```

## 📝 Field Notes

* **Fonts:** The editor uses **Consolas** for the text buffer to ensure code readability, while **Arial Bold** is used for the UI to mimic the high-res font used in the FF8 remaster/PC versions.
* **Cursor:** The insertion cursor is set to Cyan (`#00ffef`) to match the menu selection finger.

<br />

<div align="center">

*"Balamb Garden Disciplinary Committee approved."*

</div>
