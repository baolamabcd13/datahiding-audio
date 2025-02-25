from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QSlider, QStyle)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        # Play button
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.clicked.connect(self.play_pause)
        
        # Time labels
        self.current_time = QLabel("0:00")
        self.total_time = QLabel("0:00")
        
        # Time slider
        self.time_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_slider.sliderMoved.connect(self.set_position)
        
        # Audio info
        self.info_label = QLabel()
        self.info_label.setStyleSheet("color: #8a8a8a;")
        
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.current_time)
        controls_layout.addWidget(self.time_slider)
        controls_layout.addWidget(self.total_time)
        
        layout.addLayout(controls_layout)
        layout.addWidget(self.info_label)
        
        # Media player setup
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        
        # Connect signals
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        
        self.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 11px;
            }
            QPushButton {
                background: none;
                border: none;
                padding: 3px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                border-radius: 3px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #3d3d3d;
                height: 3px;
                background: #2d2d2d;
                margin: 1px 0;
            }
            QSlider::handle:horizontal {
                background: #007acc;
                border: none;
                width: 10px;
                margin: -3px 0;
                border-radius: 5px;
            }
        """)

    def load_audio(self, file_path):
        try:
            self.player.setSource(QUrl.fromLocalFile(file_path))
            self.info_label.setText(f"Audio loaded: {file_path.split('/')[-1]}")
        except Exception as e:
            print(f"Error loading audio: {e}")
            self.info_label.setText("Error loading audio file")

    def play_pause(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        else:
            self.player.play()
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))

    def set_position(self, position):
        self.player.setPosition(position)

    def position_changed(self, position):
        self.time_slider.setValue(position)
        self.current_time.setText(self.format_time(position))

    def duration_changed(self, duration):
        self.time_slider.setRange(0, duration)
        self.total_time.setText(self.format_time(duration))

    def format_time(self, ms):
        s = round(ms / 1000)
        m, s = divmod(s, 60)
        return f"{m}:{s:02d}"
