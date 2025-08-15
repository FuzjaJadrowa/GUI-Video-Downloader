import requests
import os
import stat
import threading
import json
import zipfile
from pathlib import Path
from PySide6.QtCore import QObject, Signal

GITHUB_API = "https://api.github.com"

class DependencySignals(QObject):
    progress = Signal(str, int)
    finished = Signal(str, bool, str)
    info = Signal(str)
    error = Signal(str)

class DependencyManager:
    def __init__(self, popup_manager, requirements_dir: Path, json_path: Path):
        self.popup = popup_manager
        self.req_dir = Path(requirements_dir)
        self.req_dir.mkdir(parents=True, exist_ok=True)
        self.json_path = Path(json_path)
        if not self.json_path.exists():
            self._save_json({})
        self.signals = DependencySignals()

    def _load_json(self):
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_json(self, data):
        try:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception:
            pass

    def _json_get(self, app_name):
        data = self._load_json()
        return data.get(app_name)

    def _json_set(self, app_name, published_at_iso):
        data = self._load_json()
        data[app_name] = published_at_iso
        self._save_json(data)

    def check_existing_requirements(self):
        result = {}
        ff_name = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
        ffprobe_name = "ffprobe.exe" if os.name == "nt" else "ffprobe"
        ffplay_name = "ffplay.exe" if os.name == "nt" else "ffplay"
        ytd_name = "yt-dlp.exe" if os.name == "nt" else "yt-dlp"

        ffmpeg_files = [self.req_dir / ff_name, self.req_dir / ffprobe_name, self.req_dir / ffplay_name]
        ffmpeg_exists = all(f.exists() for f in ffmpeg_files)
        ytd_exists = (self.req_dir / ytd_name).exists()

        result["ffmpeg"] = ffmpeg_exists
        result["yt-dlp"] = ytd_exists
        return result

    def _is_online(self):
        try:
            requests.get("https://api.github.com", timeout=5)
            return True
        except requests.RequestException:
            return False

    def install_dependency(self, name, progress_bar, button, finish_callback=None):
        thread = threading.Thread(target=self._install_thread, args=(name, progress_bar, button, finish_callback), daemon=True)
        thread.start()

    def check_update_dependency(self, name, progress_bar, button, finish_callback=None):
        thread = threading.Thread(target=self._check_update_thread, args=(name, progress_bar, button, finish_callback), daemon=True)
        thread.start()

    def _install_thread(self, name, progress_bar, button, finish_callback):
        try:
            if not self._is_online():
                self.signals.error.emit("Error: No internet connection.")
                if finish_callback:
                    finish_callback(name, False, "no-internet")
                return

            if name == "yt-dlp":
                release = self._github_latest_release("yt-dlp/yt-dlp")
                asset = self._choose_asset(release.get("assets", []), want_keyword="yt-dlp")
                if not asset:
                    raise RuntimeError("yt-dlp asset not found")
                url = asset["browser_download_url"]
                published_at = release.get("published_at")
                dest = self.req_dir / ("yt-dlp.exe" if os.name == "nt" else "yt-dlp")
                self._download_file(url, dest, name)
                if published_at:
                    self._json_set("yt-dlp", published_at)
                self.signals.finished.emit(name, True, "downloaded")
                if finish_callback:
                    finish_callback(name, True, "downloaded")
                return

            if name == "ffmpeg":
                release = self._github_latest_release("GyanD/codexffmpeg")
                asset = self._choose_asset(release.get("assets", []), want_keyword="essentials_build")
                if not asset:
                    raise RuntimeError("ffmpeg essentials asset not found")
                url = asset["browser_download_url"]
                tmp_zip = self.req_dir / "ffmpeg_download.zip"
                self._download_file(url, tmp_zip, name)
                self._extract_and_copy_ffmpeg(tmp_zip)
                try:
                    tmp_zip.unlink()
                except Exception:
                    pass
                published_at = release.get("published_at") or release.get("tag_name")
                if published_at:
                    self._json_set("ffmpeg", published_at)
                self.signals.finished.emit(name, True, "downloaded")
                if finish_callback:
                    finish_callback(name, True, "downloaded")
                return

        except Exception as e:
            self.signals.error.emit(f"Error: {e}")
            if finish_callback:
                finish_callback(name, False, str(e))

    def _check_update_thread(self, name, progress_bar, button, finish_callback):
        try:
            if not self._is_online():
                self.signals.error.emit("Error: No internet connection.")
                if finish_callback:
                    finish_callback(name, False, "no-internet")
                return

            if name == "yt-dlp":
                release = self._github_latest_release("yt-dlp/yt-dlp")
                published_at = release.get("published_at")
                stored = self._json_get("yt-dlp")
                if stored and published_at and stored == published_at:
                    self.signals.info.emit("No updates found")
                    if finish_callback:
                        finish_callback(name, True, "no-updates")
                else:
                    asset = self._choose_asset(release.get("assets", []), want_keyword="yt-dlp")
                    if not asset:
                        raise RuntimeError("yt-dlp asset not found")
                    url = asset["browser_download_url"]
                    dest = self.req_dir / ("yt-dlp.exe" if os.name == "nt" else "yt-dlp")
                    self._download_file(url, dest, name)
                    if published_at:
                        self._json_set("yt-dlp", published_at)
                    self.signals.finished.emit(name, True, "updated")
                    if finish_callback:
                        finish_callback(name, True, "updated")
                return

            if name == "ffmpeg":
                release = self._github_latest_release("GyanD/codexffmpeg")
                published_at = release.get("published_at") or release.get("tag_name")
                stored = self._json_get("ffmpeg")
                if stored and published_at and stored == published_at:
                    self.signals.info.emit("No updates found")
                    if finish_callback:
                        finish_callback(name, True, "no-updates")
                else:
                    asset = self._choose_asset(release.get("assets", []), want_keyword="essentials_build")
                    if not asset:
                        raise RuntimeError("ffmpeg essentials asset not found")
                    url = asset["browser_download_url"]
                    tmp_zip = self.req_dir / "ffmpeg_download.zip"
                    self._download_file(url, tmp_zip, name)
                    self._extract_and_copy_ffmpeg(tmp_zip)
                    try:
                        tmp_zip.unlink()
                    except Exception:
                        pass
                    if published_at:
                        self._json_set("ffmpeg", published_at)
                    self.signals.finished.emit(name, True, "updated")
                    if finish_callback:
                        finish_callback(name, True, "updated")
                return

        except Exception as e:
            self.signals.error.emit(f"Error: {e}")
            if finish_callback:
                finish_callback(name, False, str(e))

    def _github_latest_release(self, owner_repo):
        url = f"{GITHUB_API}/repos/{owner_repo}/releases/latest"
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        return r.json()

    def _choose_asset(self, assets, want_keyword="ffmpeg"):
        for a in assets:
            name = a.get("name", "").lower()
            if want_keyword in name and (name.endswith(".zip") or (os.name=="nt" and name.endswith(".exe"))):
                return a
        return None

    def _download_file(self, url, dest_path: Path, name):
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            total = int(r.headers.get("Content-Length", 0) or 0)
            downloaded = 0
            tmp = dest_path.with_suffix(dest_path.suffix + ".part")
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if not chunk:
                        continue
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        pct = int(downloaded * 100 / total)
                        try:
                            self.signals.progress.emit(name, pct)
                        except Exception:
                            pass
            tmp.replace(dest_path)

    def _extract_and_copy_ffmpeg(self, zip_path: Path):
        with zipfile.ZipFile(zip_path, "r") as z:
            bin_files = [f for f in z.namelist() if "/bin/" in f]
            wanted = ["ffmpeg.exe", "ffprobe.exe", "ffplay.exe"] if os.name == "nt" else ["ffmpeg", "ffprobe", "ffplay"]

            for f in bin_files:
                fname = os.path.basename(f)
                if fname in wanted:
                    dest = self.req_dir / fname
                    with z.open(f) as src, open(dest, "wb") as dst:
                        dst.write(src.read())
                    try:
                        dest.chmod(dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                    except Exception:
                        pass