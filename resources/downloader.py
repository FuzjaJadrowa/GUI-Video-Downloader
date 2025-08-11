import requests
import shutil
import os
import subprocess

class DependencyManager:
    def __init__(self, notifier):
        self.notifier = notifier

    def internet_available(self):
        try:
            requests.get("https://www.google.com", timeout=3)
            return True
        except requests.RequestException:
            return False

    def handle_dependency(self, name, progress_bar, button):
        if not self.internet_available():
            self.notifier.show_message("Error: No internet connection.", "error")
            return

        url = None
        if name == "ffmpeg":
            url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        elif name == "yt-dlp":
            url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"

        if url:
            self.download_file(url, name, progress_bar, button)

    def download_file(self, url, name, progress_bar, button):
        try:
            r = requests.get(url, stream=True)
            total = int(r.headers.get("content-length", 0))
            downloaded = 0
            path = f"{name}.exe" if name != "ffmpeg" else f"{name}.zip"

            with open(path, "wb") as f:
                for chunk in r.iter_content(1024):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress = int(downloaded * 100 / total)
                        progress_bar.setValue(progress)

            self.notifier.show_message(f"Downloaded {name}", "success")
            button.setText("Check update")
        except Exception:
            self.notifier.show_message(f"Error downloading {name}", "error")
