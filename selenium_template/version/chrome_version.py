import re
import shutil
import subprocess
import sys

from logging_config import logger

_VERSION_RE = re.compile(r"(\d+)\.\d+\.\d+\.\d+")


def _from_windows_registry() -> str | None:
    for hive in ("HKCU", "HKLM"):
        try:
            return subprocess.check_output(
                ["reg", "query", rf"{hive}\Software\Google\Chrome\BLBeacon", "/v", "version"],
                text=True,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            continue
    return None


def _from_binary() -> str | None:
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            try:
                return subprocess.check_output([path, "--version"], text=True)
            except Exception:
                continue
    return None


def get_chrome_major_version() -> int | None:
    """Major version of the installed Chrome, or None to let uc decide."""
    out = _from_windows_registry() if sys.platform == "win32" else _from_binary()
    match = _VERSION_RE.search(out or "")
    if match:
        return int(match.group(1))
    logger.warning("Could not detect Chrome version, letting uc decide")
    return None
