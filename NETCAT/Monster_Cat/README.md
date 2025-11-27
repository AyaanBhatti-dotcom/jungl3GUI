# Monster_Cat // Zero Ultra Listener

<div align="center">

<img src="https://github.com/user-attachments/assets/32970064-3f53-434d-bfd2-7fa2ce057003" width="600" alt="Monster Cat GUI Interface">
<br><br>
<img src="https://github.com/user-attachments/assets/8279cb65-ad22-4f51-8a2a-456b4dbdf894" width="200" alt="Monster Zero Ultra Can Inspiration">

</div>

## ⚡ Overview
**Monster_Cat** is a Python-based GUI wrapper for Netcat, heavily inspired by the aesthetics of the *Monster Energy Zero Ultra* can. It replaces the standard command-line listener with a "Hollywood Hacker" style transparent interface, featuring an integrated terminal emulator, threaded socket handling, and custom ASCII art banners.

Built for CTF players and cybersecurity students who want their tools to match their vibe.

## 💎 Features
* **Zero Ultra Aesthetic:** Ice Blue text, Silver accents, and a deep black background.
* **Integrated Terminal:** Type directly into the window. The shell detects "Enter" keys and manages input/output history to prevent overwriting logs.
* **Threaded Listener:** Runs the socket server in the background, keeping the GUI responsive while waiting for connections.
* **Custom Assets:** Supports loading a custom `claw_logo.png` and `background.png` texture.
* **Smart Feedback:** Visual indicators for connection status and error handling.

## 🛠️ Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/AyaanBhatti-dotCom/Monster_Cat.git
    cd Monster_Cat
    ```

2.  **Install Dependencies**
    The only external requirement is `Pillow` for image rendering.
    ```bash
    pip install pillow
    ```

3.  **Run the Tool**
    ```bash
    python3 monstercat.py
    ```

5.  **Pwn:** Once the "UPLINK ESTABLISHED" message appears, type commands directly into the GUI console.

## 📂 Customization
To add the logo seen in the screenshot, place the following files in the root directory of the script:
* `claw_logo.png` (Transparent PNG recommended)

---

> **Disclaimer:** This tool is for educational purposes and CTF challenges only. Do not use this on networks or systems you do not have permission to access.
