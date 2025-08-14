import subprocess
from pathlib import Path

YT_DLP_PATH = Path(__file__).parent.parent / "data" / "requirements" / "yt-dlp.exe"
FFMPEG_PATH = Path(__file__).parent.parent / "data" / "requirements"

def run_debug_command(cmd_list):
    env = dict(**subprocess.os.environ)
    env["PATH"] = str(FFMPEG_PATH) + ";" + env.get("PATH", "")

    print("DEBUG: Running command:")
    print(" ".join(f'"{c}"' if " " in c else c for c in cmd_list))

    try:
        process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
        for line in process.stdout:
            print(line, end="")
        process.wait()
        if process.returncode == 0:
            print("\nDEBUG: Command finished successfully.")
        else:
            print(f"\nDEBUG: Command exited with code {process.returncode}.")
    except Exception as e:
        print(f"DEBUG: Error while running command: {e}")