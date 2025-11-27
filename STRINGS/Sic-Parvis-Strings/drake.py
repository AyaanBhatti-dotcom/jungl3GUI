import sys
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QTextEdit, QFileDialog,
                             QLabel, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtGui import QColor, QFont, QCursor, QPalette, QTextCursor

# --- THEME PALETTE ---
LEATHER_BG_DARK = "#1a120b"
LEATHER_BG_LIGHT = "#3d2b1f"
PAPER_BG = "#fcf5c8"
INK_COLOR = "#2c1e12"

# Text Colors
MENU_TEXT_COLOR = "#f1e9d2" 
RED_MARKER = "#ff4d4d" 
GOLD_FOIL_TEXT = "#d4af37"

class SketchButton(QPushButton):
    """
    Buttons that sit on the Dark Leather Sidebar.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(55)
        
        font = QFont()
        font.setFamily("Segoe Print")
        if not font.exactMatch(): font.setFamily("Bradley Hand ITC")
        if not font.exactMatch(): font.setFamily("URW Chancery L")
        font.setPointSize(13)
        font.setBold(True)
        self.setFont(font)

        self.default_style = f"""
            QPushButton {{
                color: {MENU_TEXT_COLOR};
                background-color: transparent;
                border: none;
                text-align: left;
                padding-left: 20px;
                margin: 2px;
            }}
        """
        
        self.hover_style = f"""
            QPushButton {{
                color: {RED_MARKER};
                background-color: rgba(255, 77, 77, 0.1);
                border: 2px solid {RED_MARKER};
                border-radius: 15px;
                border-top-right-radius: 25px;
                border-bottom-left-radius: 25px;
                text-align: left;
                padding-left: 25px;
                margin: 0px; 
            }}
        """

        self.pressed_style = f"""
             QPushButton {{
                color: {RED_MARKER};
                background-color: rgba(255, 77, 77, 0.15);
                border: 2px solid {RED_MARKER};
                border-radius: 15px;
                border-top-right-radius: 25px;
                border-bottom-left-radius: 25px;
                text-align: left;
                padding-left: 27px;
                padding-top: 2px;
            }}
        """
        self.setStyleSheet(self.default_style)

    def enterEvent(self, event):
        self.setStyleSheet(self.hover_style)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self.default_style)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.setStyleSheet(self.pressed_style)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.rect().contains(event.pos()):
            self.setStyleSheet(self.hover_style)
        else:
            self.setStyleSheet(self.default_style)
        super().mouseReleaseEvent(event)

class JournalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drake's Journal // Decryption Tool")
        # Increased window size slightly
        self.resize(1280, 850)
        
        # Main Background
        self.setStyleSheet(f"""
            QMainWindow {{
                background: qradialgradient(cx:0.5, cy:0.5, radius: 1.0, fx:0.5, fy:0.5, 
                                            stop:0 {LEATHER_BG_LIGHT}, 
                                            stop:1 {LEATHER_BG_DARK});
            }}
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        # Reduced outer margins to give more space to the content
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(20)

        # --- LEFT: The Satchel Menu ---
        self.menu_container = QFrame()
        # Reduced menu width from 280 to 240 to make page wider
        self.menu_container.setFixedWidth(240)
        self.menu_container.setStyleSheet("border-right: 2px solid rgba(0,0,0,0.3);")
        
        self.menu_layout = QVBoxLayout(self.menu_container)
        self.menu_layout.setContentsMargins(5, 60, 15, 20)
        self.menu_layout.setSpacing(20)

        # Title Logo
        title = QLabel("SIC PARVIS\nMAGNA")
        title.setFont(QFont("Times New Roman", 20, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {GOLD_FOIL_TEXT}; letter-spacing: 3px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.menu_layout.addWidget(title)

        subtitle = QLabel("- Explorer's Toolkit -")
        subtitle.setFont(QFont("Segoe Script", 10))
        subtitle.setStyleSheet(f"color: {GOLD_FOIL_TEXT}; opacity: 0.8; margin-bottom: 40px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.menu_layout.addWidget(subtitle)

        # Buttons
        self.btn_load = SketchButton("Found Artifact...")
        self.btn_save = SketchButton("Update Log...")
        self.btn_clear = SketchButton("Scrap Page")
        self.btn_quit = SketchButton("Close Journal")

        self.menu_layout.addWidget(self.btn_load)
        self.menu_layout.addWidget(self.btn_save)
        self.menu_layout.addWidget(self.btn_clear)
        self.menu_layout.addStretch()
        self.menu_layout.addWidget(self.btn_quit)

        # Connecting
        self.btn_load.clicked.connect(self.load_file)
        self.btn_save.clicked.connect(self.save_text)
        self.btn_clear.clicked.connect(self.clear_text)
        self.btn_quit.clicked.connect(self.close)

        # --- RIGHT: The Journal Page ---
        self.page_container = QWidget()
        self.page_stack = QVBoxLayout(self.page_container) 
        self.page_stack.setContentsMargins(0,0,0,0)

        self.paper = QFrame()
        # Drop Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(5)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 200))
        self.paper.setGraphicsEffect(shadow)

        # Paper CSS
        self.paper.setStyleSheet(f"""
            QFrame {{
                background-color: {PAPER_BG};
                border: 1px solid #cbbf9e;
                border-radius: 2px;
                border-bottom-right-radius: 35px;
            }}
        """)

        self.paper_content = QVBoxLayout(self.paper)
        # Reduced internal padding significantly so text area is larger
        self.paper_content.setContentsMargins(30, 40, 30, 30)

        # Header
        header_row = QHBoxLayout()
        self.entry_header = QLabel("Entry #424: Uncharted Data")
        header_font = QFont("Segoe Print", 18, QFont.Weight.Bold)
        if not header_font.exactMatch(): header_font.setFamily("Fantasy")
        self.entry_header.setFont(header_font)
        self.entry_header.setStyleSheet(f"color: {INK_COLOR}; border: none; background: transparent;")
        header_row.addWidget(self.entry_header)
        header_row.addStretch()
        
        # REMOVED THE STAIN LABEL HERE
        
        self.paper_content.addLayout(header_row)

        # Red decorative line
        self.line = QFrame()
        self.line.setFixedHeight(3)
        self.line.setStyleSheet(f"background-color: {RED_MARKER}; border: none; margin-top: 5px; margin-bottom: 15px; opacity: 0.8;")
        self.paper_content.addWidget(self.line)

        # The "Pasted" Text Area
        self.text_area_container = QWidget()
        text_layout = QVBoxLayout(self.text_area_container)
        text_layout.setContentsMargins(0,0,0,0)
        
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setFont(QFont("Courier New", 11))
        self.text_area.setPlaceholderText("Select binary artifact for decryption...")
        
        # Text Area Shadow
        text_shadow = QGraphicsDropShadowEffect()
        text_shadow.setBlurRadius(10)
        text_shadow.setXOffset(3)
        text_shadow.setYOffset(3)
        text_shadow.setColor(QColor(0,0,0, 80))
        self.text_area_container.setGraphicsEffect(text_shadow)

        self.text_area.setStyleSheet(f"""
            QTextEdit {{
                background-color: rgba(250, 250, 250, 0.7);
                color: #111;
                border: 1px dashed #7a6a5a;
                padding: 15px;
                border-radius: 2px;
            }}
        """)
        text_layout.addWidget(self.text_area)
        self.paper_content.addWidget(self.text_area_container)
        
        # Footer
        self.footer_label = QLabel("// PROPERTY OF F. DRAKE //")
        self.footer_label.setFont(QFont("Stencil", 10))
        self.footer_label.setStyleSheet("color: rgba(139, 69, 19, 0.5); margin-top: 10px; letter-spacing: 1px;")
        self.footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.paper_content.addWidget(self.footer_label)

        self.page_stack.addWidget(self.paper)

        # Assemble Main
        self.main_layout.addWidget(self.menu_container)
        self.main_layout.addWidget(self.page_container)

    def get_strings(self, filename, min_len=4):
        result = ""
        try:
            with open(filename, "rb") as f:
                content = f.read()
                pattern = b"[\x20-\x7E]{" + str(min_len).encode() + b",}"
                for i, match in enumerate(re.finditer(pattern, content)):
                    decoded = match.group().decode("ascii", errors="ignore")
                    result += f"[{i:04d}] {decoded}\n"
        except Exception as e:
            return f"[!] ARTIFACT CORRUPTED: {e}"
        return result

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Investigate Artifact")
        if file_name:
            short_name = file_name.split('/')[-1]
            self.entry_header.setText(f"ENTRY: {short_name.upper()}")
            self.text_area.setText("Deciphering runes... please wait.")
            QApplication.processEvents()
            
            output = self.get_strings(file_name)
            self.text_area.setText(output)
            self.text_area.moveCursor(QTextCursor.MoveOperation.Start)

    def clear_text(self):
        self.text_area.clear()
        self.entry_header.setText("Entry #425: Blank Page")

    def save_text(self):
        if not self.text_area.toPlainText():
            return
        file_name, _ = QFileDialog.getSaveFileName(self, "Log Entry", "drakes_journal.txt", "Text Files (*.txt)")
        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.text_area.toPlainText())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JournalWindow()
    window.show()
    sys.exit(app.exec())
