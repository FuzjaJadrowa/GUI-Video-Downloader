from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class AppMain(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI Video Downloader")
        self.setStyleSheet("background-color: #121212; color: white;")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Main application window"))
        self.setLayout(layout)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    window = AppMain()
    window.show()
    app.exec()
