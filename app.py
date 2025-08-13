import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout, QProgressBar, QComboBox, QCheckBox
)
from PySide6.QtGui import QIcon

class VideoDownloaderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI Video Downloader")
        self.setFixedSize(500, 400)
        self.setWindowIcon(QIcon("icon.ico"))

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.url_label = QLabel("Video URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste your video URL here")
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        self.cookies_label = QLabel("Cookies from browser:")
        self.cookies_combo = QComboBox()
        self.cookies_combo.addItems([
            "None", "Brave", "Chrome", "Chromium", "Edge",
            "Firefox", "Opera", "Safari", "Vivaldi", "Whale"
        ])
        layout.addWidget(self.cookies_label)
        layout.addWidget(self.cookies_combo)

        self.audio_only_checkbox = QCheckBox("Audio only")
        self.audio_only_checkbox.stateChanged.connect(self.toggle_audio_only)
        layout.addWidget(self.audio_only_checkbox)

        self.video_quality_label = QLabel("Preferred video quality:")
        self.video_quality_combo = QComboBox()
        self.video_quality_combo.addItems(["Default", "1080p", "720p", "480p", "360p"])
        layout.addWidget(self.video_quality_label)
        layout.addWidget(self.video_quality_combo)

        self.video_format_label = QLabel("Preferred video format:")
        self.video_format_combo = QComboBox()
        self.video_format_combo.addItems(["Default", "mp4", "mkv", "webm"])
        layout.addWidget(self.video_format_label)
        layout.addWidget(self.video_format_combo)

        self.audio_quality_label = QLabel("Preferred audio quality:")
        self.audio_quality_combo = QComboBox()
        self.audio_quality_combo.addItems(["Default", "320kbps", "256kbps", "192kbps", "128kbps"])
        layout.addWidget(self.audio_quality_label)
        layout.addWidget(self.audio_quality_combo)

        self.audio_format_label = QLabel("Preferred audio format:")
        self.audio_format_combo = QComboBox()
        self.audio_format_combo.addItems(["Default", "mp3", "aac", "wav", "ogg"])
        layout.addWidget(self.audio_format_label)
        layout.addWidget(self.audio_format_combo)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_download)
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_download)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_download)
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.pause_button)
        buttons_layout.addWidget(self.stop_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def toggle_audio_only(self, state):
        # Placeholder: Disable video options if audio only is checked
        enabled = not bool(state)
        self.video_quality_combo.setEnabled(enabled)
        self.video_format_combo.setEnabled(enabled)

    # Placeholder methods for download controls
    def start_download(self):
        # TODO: implement actual download logic
        print("Start download clicked")

    def pause_download(self):
        # TODO: implement pause/resume logic
        if self.pause_button.text() == "Pause":
            self.pause_button.setText("Continue")
            print("Download paused")
        else:
            self.pause_button.setText("Pause")
            print("Download resumed")

    def stop_download(self):
        # TODO: implement stop logic
        print("Stop download clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoDownloaderGUI()
    window.show()
    sys.exit(app.exec())
