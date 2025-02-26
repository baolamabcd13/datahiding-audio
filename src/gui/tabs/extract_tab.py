from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QTextEdit, QFileDialog, QFrame, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt
from ..widgets.audio_player import AudioPlayer
from ..steganography.lsb import LSBAudio
from ..steganography.phase_coding import PhaseCoding

class ExtractTab(QWidget):
    def __init__(self):
        super().__init__()
        self.lsb = LSBAudio()
        self.phase = PhaseCoding()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Audio File Section
        audio_section = self.create_section("Stego Audio File")
        audio_layout = QVBoxLayout()
        audio_layout.setSpacing(10)
        
        # File selection
        select_layout = QHBoxLayout()
        self.audio_path_label = QLabel("No file selected")
        self.audio_path_label.setStyleSheet("""
            QLabel {
                color: #8a8a8a;
                padding: 8px;
                background: #2d2d2d;
                border-radius: 4px;
            }
        """)
        
        self.load_audio_btn = self.create_button("Load Audio")
        self.load_audio_btn.clicked.connect(self.load_audio)
        
        select_layout.addWidget(self.audio_path_label, stretch=1)
        select_layout.addWidget(self.load_audio_btn)
        
        # Audio player
        self.audio_player = AudioPlayer()
        
        audio_layout.addLayout(select_layout)
        audio_layout.addWidget(self.audio_player)
        audio_section.layout().addLayout(audio_layout)
        layout.addWidget(audio_section)

        # Steganography Method Section
        method_section = self.create_section("Steganography Method")
        self.method_combo = QComboBox()
        self.method_combo.addItems(["LSB (Least Significant Bit)", "Phase Coding"])
        self.method_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 6px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(resources/down-arrow.png);
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #ffffff;
                selection-background-color: #3d3d3d;
            }
        """)
        method_section.layout().addWidget(self.method_combo)
        layout.addWidget(method_section)

        # Extracted Message Section
        message_section = self.create_section("Extracted Message")
        self.message_text = QTextEdit()
        self.message_text.setReadOnly(True)
        self.message_text.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        self.message_text.setPlaceholderText("Extracted message will appear here...")
        message_section.layout().addWidget(self.message_text)
        layout.addWidget(message_section)

        # Extract Button
        buttons_layout = QHBoxLayout()
        self.extract_btn = self.create_button("Extract Message")
        self.extract_btn.clicked.connect(self.extract_message)
        self.extract_btn.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0098ff;
            }
            QPushButton:disabled {
                background-color: #252525;
                color: #666666;
            }
        """)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.extract_btn)
        layout.addLayout(buttons_layout)

        # Add stretch to push everything up
        layout.addStretch()

    def create_section(self, title):
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 6px;
            }
        """)
        layout = QVBoxLayout(section)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 13px;
                font-weight: bold;
            }
        """)
        layout.addWidget(title_label)
        return section

    def create_button(self, text):
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QPushButton:disabled {
                background-color: #252525;
                color: #666666;
            }
        """)
        return btn

    def load_audio(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Stego Audio File",
            "",
            "WAV Files (*.wav)"
        )
        if file_name:
            self.audio_path = file_name
            self.audio_path_label.setText(file_name)
            self.audio_path_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    padding: 8px;
                    background: #2d2d2d;
                    border-radius: 4px;
                }
            """)
            self.audio_player.load_audio(file_name)

    def extract_message(self):
        if not hasattr(self, 'audio_path') or not self.audio_path:
            QMessageBox.warning(self, "Warning", "Please load an audio file first")
            return

        # Chọn phương pháp extract dựa trên selection
        method = self.method_combo.currentText()
        if "LSB" in method:
            success, message = self.lsb.extract_message(self.audio_path)
        else:  # Phase Coding
            success, message = self.phase.extract_message(self.audio_path)
            
        if success:
            self.message_text.setText(message)
            QMessageBox.information(self, "Success", "Message extracted successfully!")
        else:
            self.message_text.clear()
            QMessageBox.warning(self, "Warning", message)
