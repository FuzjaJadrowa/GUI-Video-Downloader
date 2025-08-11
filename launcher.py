import sys
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar
from PySide6.QtCore import Qt
from resources.notifications import Notification
from resources.downloader import DependencyManager
import subprocess

class Launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI Video Downloader")
        self.setFixedSize(640, 260)
        self.setStyleSheet("background-color: #121212;")
        
        self.notification = Notification(self)
        self.dependency_manager = DependencyManager(self.notification)

        title = QLabel("GUI Video Downloader")
        title.setObjectName("title")
        subtitle = QLabel("Version 1.0.0")
        subtitle.setObjectName("subtitle")

        title_layout = QVBoxLayout()
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        # ffmpeg
        self.ffmpeg_progress = QProgressBar()
        self.ffmpeg_button = QPushButton("Install")
        self.ffmpeg_button.clicked.connect(lambda: self.dependency_manager.handle_dependency("ffmpeg", self.ffmpeg_progress, self.ffmpeg_button))

        ffmpeg_layout = QHBoxLayout()
        ffmpeg_label = QLabel("ffmpeg")
        ffmpeg_label.setMinimumWidth(80)
        ffmpeg_layout.addWidget(ffmpeg_label)
        ffmpeg_layout.addWidget(self.ffmpeg_progress)
        ffmpeg_layout.addWidget(self.ffmpeg_button)

        # yt-dlp
        self.ytdlp_progress = QProgressBar()
        self.ytdlp_button = QPushButton("Install")
        self.ytdlp_button.clicked.connect(lambda: self.dependency_manager.handle_dependency("yt-dlp", self.ytdlp_progress, self.ytdlp_button))

        ytdlp_layout = QHBoxLayout()
        ytdlp_label = QLabel("yt-dlp")
        ytdlp_label.setMinimumWidth(80)
        ytdlp_layout.addWidget(ytdlp_label)
        ytdlp_layout.addWidget(self.ytdlp_progress)
        ytdlp_layout.addWidget(self.ytdlp_button)

        # Launch button
        launch_button = QPushButton("Launch")
        launch_button.setFixedWidth(100)
        launch_button.clicked.connect(self.launch_app)

        layout = QVBoxLayout()
        layout.addLayout(title_layout)
        layout.addSpacing(15)
        layout.addLayout(ffmpeg_layout)
        layout.addLayout(ytdlp_layout)
        layout.addStretch()
        layout.addWidget(launch_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def launch_app(self):
        try:
            subprocess.Popen([sys.executable, "app.py"])
            self.close()
        except Exception:
            self.notification.show_message("Error: Cannot launch app.", "error")
