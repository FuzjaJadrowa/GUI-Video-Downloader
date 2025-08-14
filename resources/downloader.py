import subprocess
import threading
from pathlib import Path
import validators
import requests

from resources.debug import run_debug_command

YT_DLP_PATH = Path(__file__).parent.parent / "data" / "requirements" / "yt-dlp.exe"
FFMPEG_PATH = Path(__file__).parent.parent / "data" / "requirements"

class Downloader:
    def __init__(self, popup_manager, progress_callback=None):
        self.popup = popup_manager
        self.process = None
        self.progress_callback = progress_callback

    def check_internet(self):
        try:
            requests.get("https://www.google.com", timeout=5)
            return True
        except requests.RequestException:
            return False

    def validate_input(self, url: str, download_path: str) -> bool:
        if not url:
            self.popup.show_error("No link provided.")
            return False
        if not validators.url(url):
            self.popup.show_error("The link provided is not valid.")
            return False
        if not download_path:
            self.popup.show_error("No download path provided.")
            return False
        if not self.check_internet():
            self.popup.show_error("No internet connection.")
            return False
        return True

    def download_video(
            self, url: str, download_path: str,
            cookies=None, audio_only=False,
            audio_format="Default", audio_quality="Default",
            video_format="Default", video_quality="Default",
            on_finished=None
    ):
        if not self.validate_input(url, download_path):
            if on_finished:
                on_finished()
            return

        download_path = Path(download_path)
        download_path.mkdir(parents=True, exist_ok=True)

        env = dict(**subprocess.os.environ)
        env["PATH"] = str(FFMPEG_PATH) + ";" + env.get("PATH", "")

        cmd = [
            str(YT_DLP_PATH),
            "--no-playlist",
            "-P", str(download_path),
            "--ffmpeg-location", str(FFMPEG_PATH / "ffmpeg.exe")
        ]

        if cookies and cookies.lower() != "none":
            cmd += ["--cookies-from-browser", cookies.lower()]

        if audio_only:
            cmd.append("-x")
            if audio_format.lower() != "default":
                cmd += ["--audio-format", audio_format.lower()]
            if audio_quality.lower() != "default":
                quality_value = audio_quality.replace("kbps", "K")
                cmd += ["--audio-quality", quality_value]
        else:
            if video_format.lower() != "default":
                cmd += ["-f", video_format.lower()]
            if video_quality.lower() != "default":
                res_value = video_quality.replace("p", "")
                cmd += ["-S", f"res:{res_value}"]

        cmd.append(url)
        run_debug_command(cmd)

        def run():
            try:
                self.process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env
                )

                # czytanie stdout w tle
                while True:
                    line = self.process.stdout.readline()
                    if not line:
                        break
                    # parsowanie postępu
                    if self.progress_callback and "[" in line and "%" in line:
                        percent = line.strip().strip("[]").replace("%", "")
                        try:
                            self.progress_callback(float(percent))
                        except:
                            pass
                    # debug
                    print(line, end="")

                self.process.wait()
                if self.process.returncode == 0:
                    self.popup.show_info("Download completed successfully!")
                else:
                    self.popup.show_error("Download failed or was stopped.")
            except Exception as e:
                self.popup.show_error(f"Error during download: {e}")
            finally:
                self.process = None
                if on_finished:
                    on_finished()

        threading.Thread(target=run, daemon=True).start()

    def stop_download(self):
        if self.process:
            self.process.terminate()
            self.process = None
            self.popup.show_info("Download stopped by user.")
            if self.progress_callback:
                self.progress_callback(0)