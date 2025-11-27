<div align="center">

# ☢️ Half-Life Gobuster GUI
### Sector 7G Standard Issue Network Analysis Tool

<img width="600" alt="Black Mesa Gobuster GUI Screenshot" src="https://github.com/user-attachments/assets/b9802a5b-2308-4c91-84c3-3d283ae52c60" />

<br/>
<br/>

[![Python](https://img.shields.io/badge/Python-3.x-FFB600?style=for-the-badge&logo=python&logoColor=black)](https://www.python.org/)
[![Tool](https://img.shields.io/badge/Powered_By-Gobuster-95c44f?style=for-the-badge)](https://github.com/OJ/gobuster)
[![Clearance](https://img.shields.io/badge/Clearance-Top_Secret-red?style=for-the-badge)]()

**A fully functional, Half-Life inspired graphical wrapper for `gobuster` with real-time feedback and interactive results.**

</div>

---

## 📂 Accessing The Terminal

Tired of staring at standard command-line output? This tool wraps the powerful **Gobuster** directory scanner in a **Black Mesa Research Facility** interface (HEV Suit Orange & CRT Green).

It is designed to streamline the reconnaissance workflow during CTFs and security audits while keeping you immersed in the *Half-Life* aesthetic.

## ⚡ Features

* **☢️ HEV Aesthetic:** A high-contrast Dark/Orange/Green theme designed for the Anomalous Materials Lab.
* **🔭 Live Progress Feed:** Features a real-time word count tracker (`Processed: 1,500 / 14,000`) and mission timer.
* **📝 Smart Autocomplete:** Includes a custom Bash-style input. Press `TAB` to auto-complete file paths for your wordlists.
* **📊 Anomaly Grid:** Parses raw text output into a clean, sortable data table (Path, Status, Size).
* **🔗 Quick Uplink:** Double-click any result to instantly open the URL in your default web browser.
* **🛑 Emergency Abort:** Hard-kill switch to terminate the scanning process immediately.

## ⚙️ Prerequisites

This tool is a **GUI Frontend**. You must have the core resonance equipment installed on your system:

1.  **Python 3.x**
2.  **Gobuster** 
3.  **OS:** Linux or macOS is recommended (for full PTY live-progress support). Windows is supported but may lack the live word counter.

## 🚀 Installation & Initialization

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/AyaanBhatti-dotcom/HalfLife_Gobuster_GUI.git
    cd HalfLife_Gobuster_GUI
    ```

2.  **Initiate Sequence:**
    ```bash
    python3 hl3.py
    ```

## 🕹️ Usage Protocol

1.  **Target Specimen:** Enter the target URL (e.g., `http://10.10.10.5`).
2.  **Data Dictionary:** Enter the path to your wordlist (e.g., `/usr/share/wordlists/dirb/common.txt`).
    * *Tip: Start typing the path and hit `TAB` to use the built-in autocomplete.*
3.  **Initiate Resonance:** Click the Orange button to begin the scan.
4.  **Analysis:** Watch the "Anomalous Signals" grid populate. Double-click an entry to investigate.

## ⚠️ Classification Warning

**AUTHORIZED PERSONNEL ONLY.**

This tool is intended for **legal security auditing** and **Capture The Flag (CTF)** usage only. The developer assumes no liability for unauthorized resonance cascades or network intrusions.

---
<div align="center">
  <i>"Have a very safe day."</i>
</div>
