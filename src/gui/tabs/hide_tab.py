from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QTextEdit, QComboBox, QFileDialog, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from ..widgets.audio_player import AudioPlayer

class HideTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Audio Info Section
        info_section = self.create_section("Audio Requirements")
        info_text = QLabel("""
            Recommended audio files:
            • WAV format (uncompressed)
            • Duration: 30s - 2m
            • Complex sounds (orchestral, nature, ambient)
            • Avoid: MP3, simple vocals, very short clips
        """)
        info_text.setStyleSheet("""
            color: #8a8a8a;
            font-size: 12px;
            padding: 5px;
        """)
        info_section.layout().addWidget(info_text)
        layout.addWidget(info_section)

        # Audio Selection Section
        audio_section = self.create_section("Audio File")
        audio_layout = QVBoxLayout()
        
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
        
        # Add audio player
        self.audio_player = AudioPlayer()
        
        audio_layout.addLayout(select_layout)
        audio_layout.addWidget(self.audio_player)
        audio_section.layout().addLayout(audio_layout)
        layout.addWidget(audio_section)

        # Message Section
        message_section = self.create_section("Message")
        self.message_text = QTextEdit()
        self.message_text.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        self.message_text.setPlaceholderText("Enter your message here...")
        message_section.layout().addWidget(self.message_text)
        layout.addWidget(message_section)

        # Method Selection
        method_section = self.create_section("Steganography Method")
        self.method_combo = QComboBox()
        self.method_combo.addItems(["LSB (Least Significant Bit)", "Phase Coding"])
        self.method_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(resources/down-arrow.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #ffffff;
                selection-background-color: #3d3d3d;
            }
        """)
        method_section.layout().addWidget(self.method_combo)
        layout.addWidget(method_section)

        # Action Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.hide_btn = self.create_button("Hide Message")
        self.hide_btn.setStyleSheet(self.hide_btn.styleSheet() + """
            QPushButton {
                background-color: #007acc;
            }
            QPushButton:hover {
                background-color: #0098ff;
            }
        """)
        
        self.save_btn = self.create_button("Save Audio")
        self.save_btn.setEnabled(False)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.hide_btn)
        buttons_layout.addWidget(self.save_btn)
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
            "Open Audio File",
            "",
            "WAV Files (*.wav);;All Files (*.*)"  # Ưu tiên file WAV
        )
        if file_name:
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
