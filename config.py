"""Auto-detect paths for Tesseract, ChromeDriver, and download folder.
Works on Windows, macOS, and Linux without hardcoded paths."""

import os
import sys
import shutil
import platform

IS_WINDOWS = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── DOWNLOAD FOLDER ──────────────────────────────────────────────────
# PDFs will be saved to: C:\Users\<you>\Downloads\GeM-PDFs
DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "GeM-PDFs")
# ──────────────────────────────────────────────────────────────────────

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def find_tesseract():
    """Find tesseract.exe across common install locations."""
    found = shutil.which("tesseract")
    if found:
        return found

    candidates = []
    if IS_WINDOWS:
        candidates = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Tesseract-OCR", "tesseract.exe"),
            os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local",
                         "Programs", "Tesseract-OCR", "tesseract.exe"),
        ]
    elif IS_MAC:
        candidates = [
            "/usr/local/bin/tesseract",
            "/opt/homebrew/bin/tesseract",
            "/usr/bin/tesseract",
        ]
    else:  # Linux
        candidates = [
            "/usr/bin/tesseract",
            "/usr/local/bin/tesseract",
            "/snap/bin/tesseract",
        ]

    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return None


def find_chromedriver():
    """Find chromedriver.exe — either bundled with the project or on PATH.
    (No longer required since we use webdriver-manager, but kept for compatibility.)"""
    local_names = ["chromedriver.exe", "chromedriver"] if IS_WINDOWS else ["chromedriver"]
    for name in local_names:
        local = os.path.join(BASE_DIR, name)
        if os.path.isfile(local):
            return local

    found = shutil.which("chromedriver")
    if found:
        return found

    candidates = []
    if IS_WINDOWS:
        candidates = [r"C:\Program Files\chromedriver\chromedriver.exe"]
    elif IS_MAC:
        candidates = ["/usr/local/bin/chromedriver", "/opt/homebrew/bin/chromedriver"]
    else:
        candidates = ["/usr/bin/chromedriver", "/usr/local/bin/chromedriver"]

    for path in candidates:
        if os.path.isfile(path):
            return path
    return None


TESSERACT_PATH = find_tesseract()
CHROMEDRIVER_PATH = find_chromedriver()


def report():
    """Print detection results — called at startup."""
    print("=" * 60)
    print("  GeM Document Scraper — Environment Check")
    print("=" * 60)
    print(f"  OS              : {platform.system()} {platform.release()}")
    print(f"  Python          : {sys.version.split()[0]}")
    print(f"  Project folder  : {BASE_DIR}")
    print(f"  Download folder : {DOWNLOAD_DIR}")
    print(f"  Tesseract OCR   : {TESSERACT_PATH or 'NOT FOUND'}")
    print(f"  ChromeDriver    : {CHROMEDRIVER_PATH or 'auto-managed by webdriver-manager'}")
    print("=" * 60)

    if not TESSERACT_PATH:
        print("\n  Tesseract OCR is not installed.")
        print("  Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  During install, check 'English' language data.\n")


if __name__ == "__main__":
    report()