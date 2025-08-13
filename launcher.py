import subprocess
from pathlib import Path

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar
from PySide6.QtCore import Qt
from resources.notifications import PopupManager
from resources.downloader import DependencyManager

HERE = Path(__file__).parent
DATA_DIR = HERE / "data"
REQUIREMENTS_DIR = DATA_DIR / "requirements"
DATA_DIR.mkdir(exist_ok=True)
REQUIREMENTS_DIR.mkdir(parents=True, exist_ok=True)

class Launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI Video Downloader Launcher")
        self.setFixedSize(680, 300)
        self.setStyleSheet("background-color: #121212;")

        self.popup = PopupManager(self)
        self.deps = DependencyManager(self.popup, requirements_dir=REQUIREMENTS_DIR, json_path=DATA_DIR / "version_info.json")

        top_row = QHBoxLayout()
        icon_label = QLabel()
        icon_path = HERE / "icon.ico"
        if icon_path.exists():
            icon_label.setPixmap(QPixmap(str(icon_path)).scaled(48, 48))
        title_label = QLabel("GUI Video Downloader Launcher")
        title_label.setObjectName("title")
        subtitle_label = QLabel("Version 1.0.0")
        subtitle_label.setObjectName("subtitle")

        title_col = QVBoxLayout()
        title_col.addWidget(title_label, alignment=Qt.AlignCenter)
        title_col.addWidget(subtitle_label, alignment=Qt.AlignCenter)
        top_row.addStretch()
        top_row.addLayout(title_col)
        top_row.addStretch()

        ff_row = QHBoxLayout()
        ff_label = QLabel("ffmpeg")
        ff_label.setMinimumWidth(90)
        self.ff_progress = QProgressBar()
        self.ff_progress.setValue(0)
        self.ff_button = QPushButton("Install")
        self.ff_button.setFixedWidth(140)
        self.ff_button.clicked.connect(lambda: self.on_dep_clicked("ffmpeg"))
        ff_row.addWidget(ff_label)
        ff_row.addWidget(self.ff_progress, stretch=1)
        ff_row.addWidget(self.ff_button)

        yt_row = QHBoxLayout()
        yt_label = QLabel("yt-dlp")
        yt_label.setMinimumWidth(90)
        self.yt_progress = QProgressBar()
        self.yt_progress.setValue(0)
        self.yt_button = QPushButton("Install")
        self.yt_button.setFixedWidth(140)
        self.yt_button.clicked.connect(lambda: self.on_dep_clicked("yt-dlp"))
        yt_row.addWidget(yt_label)
        yt_row.addWidget(self.yt_progress, stretch=1)
        yt_row.addWidget(self.yt_button)

        launch_btn = QPushButton("Launch")
        launch_btn.setFixedWidth(140)
        launch_btn.clicked.connect(self.on_launch)

        layout = QVBoxLayout()
        layout.addLayout(top_row)
        layout.addSpacing(18)
        layout.addLayout(ff_row)
        layout.addLayout(yt_row)
        layout.addStretch()
        layout.addWidget(launch_btn, alignment=Qt.AlignCenter)
        layout.addSpacing(10)

        self.setLayout(layout)

        self.update_buttons_state()

    def update_buttons_state(self):
        states = self.deps.check_existing_requirements()
        if states.get("ffmpeg"):
            self.ff_button.setText("Check Update")
            self.ff_progress.setValue(0)
        else:
            self.ff_button.setText("Install")
            self.ff_progress.setValue(0)
        if states.get("yt-dlp"):
            self.yt_button.setText("Check Update")
            self.yt_progress.setValue(0)
        else:
            self.yt_button.setText("Install")
            self.yt_progress.setValue(0)

    def on_dep_clicked(self, name):
        btn = self.ff_button if name == "ffmpeg" else self.yt_button
        progress = self.ff_progress if name == "ffmpeg" else self.yt_progress
        if btn.text().lower() == "install":
            btn.setEnabled(False)
            self.deps.install_dependency(name, progress, btn, finish_callback=self.on_op_finished)
        else:
            btn.setEnabled(False)
            self.deps.check_update_dependency(name, progress, btn, finish_callback=self.on_op_finished)

    def on_op_finished(self, name, success, message):
        if name == "ffmpeg":
            self.ff_button.setEnabled(True)
        else:
            self.yt_button.setEnabled(True)
        self.update_buttons_state()

    def on_launch(self):
        try:
            subprocess.Popen([sys.executable, str(HERE / "app.py")])
            self.close()
        except Exception as e:
            self.popup.show_error(f"Error: Cannot launch app. {e}")

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Launcher()
    w.show()
    sys.exit(app.exec())