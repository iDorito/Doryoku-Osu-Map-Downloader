import platform
import os
from pathlib import Path

HOME_PATH = Path.home()

# Files
json_file = "db.json"
settings_file = "settings.json"

IS_WINDOWS = platform.system() == 'Windows'
IS_LINUX  = platform.system() == 'Linux'
IS_MAC = platform.system() == "darwin"
IS_ANDROID = platform.system() == "Java"

IS_WSL = IS_LINUX and 'WSL_DISTRO_NAME' in os.environ

if IS_WINDOWS or IS_WSL:
    if IS_WSL:
        import subprocess
        try:
            # Obtenemos APPDATA desde windows y lo convertimos a formato wsl
            appdata_win = subprocess.check_output(['powershell.exe', '-NoProfile', '-Command', '[Console]::Out.Write($env:APPDATA)']).decode().strip()
            appdata_wsl = subprocess.check_output(['wslpath', '-u', appdata_win]).decode().strip()
            APPDATA = Path(appdata_wsl)
            
            userprofile_win = subprocess.check_output(['powershell.exe', '-NoProfile', '-Command', '[Console]::Out.Write($env:USERPROFILE)']).decode().strip()
            userprofile_wsl = subprocess.check_output(['wslpath', '-u', userprofile_win]).decode().strip()
            USERPROFILE = Path(userprofile_wsl)
        except Exception:
            # Fallback en caso de que falle
            APPDATA = Path("/mnt/c/Users/ricardo/AppData/Roaming")
            USERPROFILE = Path("/mnt/c/Users/ricardo")
    else:
        APPDATA = Path(os.environ.get("APPDATA", ""))
        USERPROFILE = Path(os.environ.get("USERPROFILE", ""))

    DOWNLOAD_PATH = USERPROFILE / "Downloads"
    DB_JSON = APPDATA / "domd"
    LASER_FILES_PATH = APPDATA / "osu" / "files"
    SETTINGS_FILE_PATH = APPDATA / "domd"

elif IS_LINUX:
    # Linux paths
    DOWNLOAD_PATH = HOME_PATH / "Downloads"
    DB_JSON = HOME_PATH / ".local" / "share" / "domd"
    LASER_FILES_PATH = HOME_PATH / ".local" / "share" / "osu" / "files"
    SETTINGS_FILE_PATH = HOME_PATH / ".local" / "share" / "domd"
elif IS_MAC:
    # macOS paths
    DOWNLOAD_PATH = HOME_PATH / "Downloads"
    DB_JSON = HOME_PATH / "Library" / "Application Support" / "domd"
    LASER_FILES_PATH = HOME_PATH / "Library" / "Application Support" / "osu" / "files"
    SETTINGS_FILE_PATH = HOME_PATH / "Library" / "Application Support" / "domd"
elif IS_ANDROID:
    # Android (termux / Android filesystem)
    DOWNLOAD_PATH = HOME_PATH / "Downloads"
    DB_JSON = HOME_PATH / ".domd"
    LASER_FILES_PATH = Path("/storage/emulated/0/Android/data/sh.ppy.osulazer/files")
    SETTINGS_FILE_PATH = HOME_PATH / ".domd"
