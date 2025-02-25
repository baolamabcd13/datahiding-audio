from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QTabWidget, QLabel, QStatusBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
from .tabs.hide_tab import HideTab
from .tabs.extract_tab import ExtractTab
from .tabs.analysis_tab import AnalysisTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Thiết lập cửa sổ chính
        self.setWindowTitle("Audio Steganography")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
        """)

        # Widget chính
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Header
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-bottom: 1px solid #3d3d3d;
            }
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 10, 20, 10)

        # Tiêu đề
        title = QLabel("Audio Steganography")
        title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        header_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("LSB & Phase Coding Implementation")
        subtitle.setStyleSheet("""
            QLabel {
                color: #8a8a8a;
                font-size: 14px;
            }
        """)
        header_layout.addWidget(subtitle)
        layout.addWidget(header)

        # Tab Widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #8a8a8a;
                padding: 10px 20px;
                border: none;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background-color: #1e1e1e;
                color: #ffffff;
                border-top: 2px solid #007acc;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3d3d3d;
                color: #ffffff;
            }
        """)

        # Thêm các tabs
        self.hide_tab = HideTab()
        self.extract_tab = ExtractTab()
        self.analysis_tab = AnalysisTab()

        self.tab_widget.addTab(self.hide_tab, "Hide Message")
        self.tab_widget.addTab(self.extract_tab, "Extract Message")
        self.tab_widget.addTab(self.analysis_tab, "Analysis")

        layout.addWidget(self.tab_widget)

        # Status Bar
        status_bar = QStatusBar()
        status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #2d2d2d;
                color: #8a8a8a;
            }
        """)
        self.setStatusBar(status_bar)
        status_bar.showMessage("Ready")

        # Version label in status bar
        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet("color: #8a8a8a; padding-right: 10px;")
        status_bar.addPermanentWidget(version_label)