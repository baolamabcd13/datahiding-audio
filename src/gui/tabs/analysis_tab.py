from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QFrame, QFileDialog, QGridLayout)
from PyQt6.QtCore import Qt
import numpy as np
import wave
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy import signal

class AnalysisTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # File Selection Section
        file_section = self.create_section("Audio Files")
        file_layout = QGridLayout()
        file_layout.setSpacing(5)
        
        # Original Audio
        self.orig_path_label = QLabel("No file selected")
        self.orig_path_label.setStyleSheet("""
            QLabel {
                color: #8a8a8a;
                padding: 5px;
                background: #2d2d2d;
                border-radius: 3px;
                font-size: 11px;
            }
        """)
        
        self.load_orig_btn = self.create_button("Load Original")
        self.load_orig_btn.clicked.connect(self.load_original)
        
        # Stego Audio
        self.stego_path_label = QLabel("No file selected")
        self.stego_path_label.setStyleSheet("""
            QLabel {
                color: #8a8a8a;
                padding: 5px;
                background: #2d2d2d;
                border-radius: 3px;
                font-size: 11px;
            }
        """)
        
        self.load_stego_btn = self.create_button("Load Stego")
        self.load_stego_btn.clicked.connect(self.load_stego)
        
        file_layout.addWidget(QLabel("Original:"), 0, 0)
        file_layout.addWidget(self.orig_path_label, 0, 1)
        file_layout.addWidget(self.load_orig_btn, 0, 2)
        file_layout.addWidget(QLabel("Stego:"), 1, 0)
        file_layout.addWidget(self.stego_path_label, 1, 1)
        file_layout.addWidget(self.load_stego_btn, 1, 2)
        
        file_section.layout().addLayout(file_layout)
        layout.addWidget(file_section)

        # Analysis Results Section
        results_section = self.create_section("Analysis Results")
        results_layout = QGridLayout()
        results_layout.setSpacing(5)
        
        # File Info
        self.file_info = QLabel("Load both files to see analysis")
        self.file_info.setStyleSheet("color: #ffffff; font-size: 11px;")
        results_layout.addWidget(self.file_info, 0, 0)
        
        # SNR & PSNR
        self.quality_metrics = QLabel("")
        self.quality_metrics.setStyleSheet("color: #ffffff; font-size: 11px;")
        results_layout.addWidget(self.quality_metrics, 1, 0)
        
        results_section.layout().addLayout(results_layout)
        layout.addWidget(results_section)

        # Visualization Section
        viz_section = self.create_section("Visualization")
        viz_layout = QVBoxLayout()
        viz_layout.setSpacing(5)
        
        # Create matplotlib figure
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 6))
        self.figure.patch.set_facecolor('#252525')
        self.canvas = FigureCanvas(self.figure)
        
        viz_layout.addWidget(self.canvas)
        viz_section.layout().addLayout(viz_layout)
        layout.addWidget(viz_section)

        # Analyze Button
        self.analyze_btn = self.create_button("Analyze")
        self.analyze_btn.clicked.connect(self.analyze_files)
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                padding: 5px 10px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #0098ff;
            }
        """)
        
        layout.addWidget(self.analyze_btn, alignment=Qt.AlignmentFlag.AlignRight)

    def create_section(self, title):
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 4px;
            }
        """)
        layout = QVBoxLayout(section)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 12px;
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
                border-radius: 3px;
                padding: 4px 8px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)
        return btn

    def load_original(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Original Audio File",
            "",
            "WAV Files (*.wav)"
        )
        if file_name:
            self.orig_path = file_name
            self.orig_path_label.setText(file_name)
            self.orig_path_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    padding: 8px;
                    background: #2d2d2d;
                    border-radius: 4px;
                }
            """)

    def load_stego(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Stego Audio File",
            "",
            "WAV Files (*.wav)"
        )
        if file_name:
            self.stego_path = file_name
            self.stego_path_label.setText(file_name)
            self.stego_path_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    padding: 8px;
                    background: #2d2d2d;
                    border-radius: 4px;
                }
            """)

    def analyze_files(self):
        if not hasattr(self, 'orig_path') or not hasattr(self, 'stego_path'):
            return
            
        # Đọc files
        with wave.open(self.orig_path, 'rb') as wav:
            orig_params = wav.getparams()
            orig_frames = wav.readframes(wav.getnframes())
        orig_audio = np.frombuffer(orig_frames, dtype=np.int16)
            
        with wave.open(self.stego_path, 'rb') as wav:
            stego_params = wav.getparams()
            stego_frames = wav.readframes(wav.getnframes())
        stego_audio = np.frombuffer(stego_frames, dtype=np.int16)

        # File info
        info_text = f"""
        Original Audio:
        - Sample rate: {orig_params.framerate} Hz
        - Channels: {orig_params.nchannels}
        - Duration: {orig_params.nframes/orig_params.framerate:.2f} seconds
        - Bit depth: {orig_params.sampwidth * 8} bits
        - File size: {len(orig_frames)/1024:.2f} KB
        """
        self.file_info.setText(info_text)

        # Tính SNR và PSNR
        noise = stego_audio - orig_audio
        snr = 10 * np.log10(np.sum(orig_audio**2) / np.sum(noise**2))
        psnr = 20 * np.log10(32767 / np.sqrt(np.mean(noise**2)))  # 32767 là max value cho int16
        
        metrics_text = f"""
        Quality Metrics:
        - SNR: {snr:.2f} dB
        - PSNR: {psnr:.2f} dB
        """
        self.quality_metrics.setText(metrics_text)

        # Clear axes
        self.ax1.clear()
        self.ax2.clear()
        
        # Điều chỉnh font size cho plots
        plt.rcParams.update({'font.size': 8})
        
        # Plot waveforms với ít chi tiết hơn
        time = np.arange(len(orig_audio)) / orig_params.framerate
        self.ax1.plot(time, orig_audio, label='Original', alpha=0.7, linewidth=0.5)
        self.ax1.plot(time, stego_audio, label='Stego', alpha=0.7, linewidth=0.5)
        self.ax1.set_title('Waveform Comparison', color='white', fontsize=9)
        self.ax1.set_xlabel('Time (s)', color='white', fontsize=8)
        self.ax1.set_ylabel('Amplitude', color='white', fontsize=8)
        self.ax1.legend(fontsize=8)
        self.ax1.grid(True, alpha=0.2)
        self.ax1.tick_params(colors='white', labelsize=7)
        
        # Plot spectrograms với ít chi tiết hơn
        f, t, Sxx = signal.spectrogram(orig_audio, orig_params.framerate, nperseg=256)
        self.ax2.pcolormesh(t, f, 10 * np.log10(Sxx))
        self.ax2.set_title('Spectrogram (Original)', color='white', fontsize=9)
        self.ax2.set_xlabel('Time (s)', color='white', fontsize=8)
        self.ax2.set_ylabel('Frequency (Hz)', color='white', fontsize=8)
        self.ax2.tick_params(colors='white', labelsize=7)
        
        # Tăng khoảng cách giữa subplots
        self.figure.tight_layout(pad=2.0)
        self.canvas.draw()
