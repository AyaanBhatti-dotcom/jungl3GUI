<div align="center">

# ☢️ New Vegas NMAP GUI ☢️

<img width="425" height="300" alt="RobCo Logo" src="https://github.com/user-attachments/assets/6606d1af-1306-4056-a61a-6708df9be74a" />

### **RobCo Industries' Finest Network Diagnostic Tool**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Nmap](https://img.shields.io/badge/Tool-Nmap-blue.svg?style=for-the-badge)](https://nmap.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<br/>

<img src="https://github.com/user-attachments/assets/605b9a9f-f37a-433c-903f-350e216e6f51" alt="New Vegas Nmap GUI Screenshot" width="800"/>

<br/>

> *"Accessing RobCo Unified Operating System. Terminal Protocol Initiated."*

</div>

---

## 📟 About The Project

**New Vegas NMAP GUI** is a Python-based graphical frontend for the **Nmap** port scanner, designed with a **Fallout: New Vegas** Pip-Boy aesthetic.

Tired of bland, uninspired terminal windows? This tool brings the wasteland to your reconnaissance workflow. It wraps common Nmap functionalities in a RobCo Industries-approved terminal interface, complete with phosphor green text, scan-line effects, and V.A.T.S.-assisted targeting parameters.

### 🦎 Origins (The Elder Scans)
This project is a retro-futuristic variation of the **[Skyrim NMAP GUI](https://github.com/AyaanBhatti-dotcom/Skyrim-NMAP-GUI)**. We traded the parchment and magic for CRTs and radiation, optimizing the code for the post-apocalyptic hacker.

## ✨ Features

* **Authentic Pip-Boy Aesthetic:** A full green-screen monochrome UI (`#1eff00`) on a CRT-black background.
* **V.A.T.S. Targeting:** Quickly toggle common Nmap flags via the interface:
    * `[ ] VERSION_DETECT (-sV)`
    * `[ ] SCRIPT_ENGINE (-sC)`
    * `[ ] OS_FINGERPRINT (-O)`
* **Manual Override:** A dedicated input field for entering custom Nmap arguments (e.g., `-p- -T4 -Pn`).
* **Live Data Uplink:** Non-blocking threading allows you to watch the scan output stream in real-time.
* **Hyperlink Detection:** Automatically detects open ports and URLs in the output.
    * *Ports (e.g., `80/tcp`) turn into clickable Cyan links.*
    * *Clicking them launches Firefox (or default browser).*

## ⚙️ Prerequisites

This is a **GUI frontend**. The actual scanning is done by Nmap. You **must** have Nmap installed on your system.

* **Nmap:** 
* **Python 3.x:** Standard installation

## 🚀 Installation & Usage

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/AyaanBhatti-dotcom/New_Vegas_NMAP_GUI.git
    ```

2.  **Navigate to the directory**:
    ```bash
    cd New_Vegas_NMAP_GUI
    ```

3.  **Initialize the Uplink**:
    ```bash
    python pipboy_scan.py
    ```

---

## 📖 How to Use

1.  **Target Host:** Enter the IP address (e.g., `10.10.10.5`) in the target field.
2.  **Select Parameters:** Check the V.A.T.S. boxes for the scan type you need.
3.  **Execute:** Click **`[ INITIALIZE UPLINK ]`**.
4.  **Analyze:** Wait for the scan to finish. Click any highlighted Cyan text to open that port in your browser.

---

<div align="center">

*"RobCo is not responsible for any misuse of this terminal protocol or any subsequent visits from Caesar's Legion due to unauthorized network probing."*

</div>
