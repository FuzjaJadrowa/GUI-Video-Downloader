from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QProgressBar, QComboBox, QCheckBox, QFileDialog
from PySide6.QtGui import QIcon, Qt

from resources.downloader import Downloader
from resources.notifications import PopupManager


class VideoDownloaderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI Video Downloader")
        self.setFixedSize(500, 500)
        self.setWindowIcon(QIcon("icon.ico"))

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("GUI Video Downloader")
        self.title_label.setObjectName("title")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.url_label = QLabel("Video URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste your video URL here")
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        self.path_label = QLabel("Download path:")
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select download folder")
        self.path_button = QPushButton("Browse")
        self.path_button.clicked.connect(self.select_download_path)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.path_button)
        layout.addWidget(self.path_label)
        layout.addLayout(path_layout)

        self.cookies_label = QLabel("Cookies from browser:")
        self.cookies_combo = QComboBox()
        self.cookies_combo.addItems(["None", "Brave", "Chrome", "Chromium", "Edge", "Firefox", "Opera", "Safari", "Vivaldi", "Whale"])
        layout.addWidget(self.cookies_label)
        layout.addWidget(self.cookies_combo)

        self.audio_only_checkbox = QCheckBox("Audio only")
        self.audio_only_checkbox.stateChanged.connect(self.toggle_audio_only)
        layout.addWidget(self.audio_only_checkbox)

        self.video_quality_label = QLabel("Video quality:")
        self.video_quality_combo = QComboBox()
        self.video_quality_combo.addItems(["Default", "2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"])
        layout.addWidget(self.video_quality_label)
        layout.addWidget(self.video_quality_combo)

        self.video_format_label = QLabel("Video format:")
        self.video_format_combo = QComboBox()
        self.video_format_combo.addItems(["Default", "3gp", "flv", "mp4", "webm"])
        layout.addWidget(self.video_format_label)
        layout.addWidget(self.video_format_combo)

        self.audio_quality_label = QLabel("Audio quality:")
        self.audio_quality_combo = QComboBox()
        self.audio_quality_combo.addItems(["Default", "320kbps", "256kbps", "192kbps", "128kbps"])
        layout.addWidget(self.audio_quality_label)
        layout.addWidget(self.audio_quality_combo)

        self.audio_format_label = QLabel("Audio format:")
        self.audio_format_combo = QComboBox()
        self.audio_format_combo.addItems(["Default", "mp3", "m4a", "aac", "wav", "ogg"])
        layout.addWidget(self.audio_format_label)
        layout.addWidget(self.audio_format_combo)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_download)
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_download)
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.stop_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.toggle_audio_only(False)

    def toggle_audio_only(self, state):
        audio_only = bool(state)

        self.video_quality_combo.setEnabled(not audio_only)
        self.video_format_combo.setEnabled(not audio_only)

        self.audio_quality_combo.setEnabled(audio_only)
        self.audio_format_combo.setEnabled(audio_only)

    def select_download_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.path_input.setText(folder)

    def start_download(self):
        popup = PopupManager(self)
        self.downloader = Downloader(popup, progress_callback=self.update_progress)

        url = self.url_input.text().strip()
        path = self.path_input.text().strip()
        cookies = self.cookies_combo.currentText()
        audio_only = self.audio_only_checkbox.isChecked()

        audio_format = self.audio_format_combo.currentText()
        audio_quality = self.audio_quality_combo.currentText()
        video_format = self.video_format_combo.currentText()
        video_quality = self.video_quality_combo.currentText()

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.downloader.download_video(
            url, path,
            cookies=cookies,
            audio_only=audio_only,
            audio_format=audio_format,
            audio_quality=audio_quality,
            video_format=video_format,
            video_quality=video_quality,
            on_finished=self.on_download_finished
        )

    def on_download_finished(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setValue(0)

    def stop_download(self):
        if hasattr(self, "downloader") and self.downloader:
            self.downloader.stop_download()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_progress(self, percent):
        self.progress_bar.setValue(int(percent))