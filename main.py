import sys
from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow

def main():
    # Tạo ứng dụng
    app = QApplication(sys.argv)
    
    # Set style cho toàn bộ ứng dụng
    app.setStyle('Fusion')
    
    # Tạo và hiển thị cửa sổ chính
    window = MainWindow()
    window.show()
    
    # Chạy ứng dụng
    sys.exit(app.exec())

if __name__ == "__main__":
    main()