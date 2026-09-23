1. Purpose & Scope
Purpose
This SOP provides step-by-step instructions for installing, running, and troubleshooting the GeM Document Scraper — a web application that automatically downloads contract PDF documents from the Government e-Marketplace (GeM) portal at https://gem.gov.in/view_contracts.

Scope
This document covers:

First-time installation on a Windows PC

Day-to-day operation

Common errors and fixes

Complete source code for rebuilding the app

Audience
Anyone who needs to download GeM contract documents in bulk — procurement officers, researchers, analysts, or administrators.

2. What This Tool Does
Summary
The app opens a local web page in your browser. You pick:

A category (e.g., "Labels Stickers")

A date range (e.g., 01-09-2026 to 05-09-2026)

It then:

Automatically opens Chrome

Navigates to the GeM portal

Solves the CAPTCHA using OCR

Downloads all matching PDFs

Shows you the files in the web page for download

Key Features
✅ Web UI (no coding needed to use)

✅ Automatic CAPTCHA solving (Tesseract OCR)

✅ Downloads saved locally

✅ Live progress log

✅ One-click PDF download from browser

Limitations
⚠️ Requires Chrome + Tesseract + Python installed

⚠️ OCR is ~80% accurate — CAPTCHA may need retries

⚠️ May not work outside India (GeM blocks some IPs)

⚠️ Runs only on the machine it's installed on

3. System Requirements
Hardware (Minimum)
Component	Requirement
CPU	Any dual-core or better
RAM	4 GB minimum (8 GB recommended)
Disk	500 MB free space
Screen	Any resolution
Software (Must Have)
Software	Version	Purpose	Download
Windows	10 or 11	OS	Pre-installed
Python	3.10 – 3.12	Runs the app	https://python.org
Google Chrome	Latest	Browser for Selenium	https://google.com/chrome
Tesseract OCR	5.x	Reads CAPTCHAs	https://github.com/UB-Mannheim/tesseract/wiki
ChromeDriver	Matches Chrome	Drives Chrome	https://googlechromelabs.github.io/chrome-for-testing/
Network Requirements
Stable internet connection

Access to https://gem.gov.in

No corporate firewall blocking the GeM domain

Optional
VPN with India server — if GeM blocks your location

7-Zip — for extracting downloaded archives

4. One-Time Setup (First Installation)
Follow these steps exactly, in order. Do not skip any step.

Step 4.1: Install Python
Go to https://www.python.org/downloads/

Download Python 3.11 or 3.12 (avoid 3.13+ for now — library compatibility)

Run the installer

⚠️ CRITICAL: On the first screen, check the box:

text
☑ Add python.exe to PATH
Click Install Now

Wait for installation to finish

Verify: Open PowerShell and run:

powershell
python --version
Should print Python 3.11.x or Python 3.12.x

If it says "Python was not found":

Open Settings → Apps → Advanced app settings → App execution aliases

Turn OFF the aliases for python.exe and python3.exe

Restart PowerShell

Step 4.2: Install Google Chrome
Go to https://google.com/chrome

Download and install

Note your Chrome version:

Open Chrome

Go to chrome://settings/help

Write down the version (e.g., 145.0.7632.117)

Step 4.3: Install Tesseract OCR
Go to https://github.com/UB-Mannheim/tesseract/wiki

Download tesseract-ocr-w64-setup-5.x.x.exe

Run the installer

⚠️ CRITICAL: On the "Choose Components" screen:

Expand "Additional language data"

Check ✅ English

Install to the default location: C:\Program Files\Tesseract-OCR\

Verify: Open PowerShell and run:

powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
Should print tesseract v5.x.x

Step 4.4: Download ChromeDriver
Go to https://googlechromelabs.github.io/chrome-for-testing/

Find a Stable release matching your Chrome version

Example: if Chrome is 145.0.7632.117, look for 145.x.x.x

In the chromedriver row, click the win64 link

Extract the ZIP — you get chromedriver.exe

Keep this file handy — you'll place it in the project folder shortly

Step 4.5: Download the Project
Option A: From GitHub

powershell
cd "$env:USERPROFILE\Downloads"
git clone https://github.com/Samcloudy/GeM-Document-Scraper.git
cd GeM-Document-Scraper
Option B: From ZIP

Download the ZIP from GitHub

Extract to C:\Users\<YourName>\Downloads\GeM-Document-Scraper

Step 4.6: Place ChromeDriver in the Project
Copy chromedriver.exe from Step 4.4

Paste it into:

text
C:\Users\<YourName>\Downloads\GeM-Document-Scraper\
It must sit next to app.py

Step 4.7: Install Python Dependencies
Open PowerShell and run:

powershell
cd "C:\Users\<YourName>\Downloads\GeM-Document-Scraper"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Or install individually if there's no requirements.txt:

powershell
python -m pip install flask selenium pytesseract Pillow pandas openpyxl
Verify installation:

powershell
python -m pip list
You should see Flask, selenium, pytesseract, Pillow, pandas, openpyxl.

Step 4.8: Verify Everything Is Ready
Run the environment check:

powershell
python config.py
Expected output:

text
============================================================
  GeM Document Scraper — Environment Check
============================================================
  OS              : Windows 11
  Python          : 3.11.5
  Project folder  : C:\Users\...\GeM-Document-Scraper
  Download folder : C:\Users\...\GeM-Document-Scraper\gem_downloads
  Tesseract OCR   : C:\Program Files\Tesseract-OCR\tesseract.exe
  ChromeDriver    : C:\Users\...\GeM-Document-Scraper\chromedriver.exe
============================================================
If Tesseract shows "NOT FOUND" → reinstall it (Step 4.3)
If ChromeDriver shows "not found" → re-copy it into the project folder (Step 4.6)

Setup is now complete. ✅

5. Running the App
Step 5.1: Start the Server
Open PowerShell and run:

powershell
cd "C:\Users\<YourName>\Downloads\GeM-Document-Scraper"
python app.py
Expected output:

text
============================================================
  GeM Document Scraper — Environment Check
============================================================
  OS              : Windows 11
  ...
  Tesseract OCR   : C:\Program Files\Tesseract-OCR\tesseract.exe
  ChromeDriver    : C:\Users\...\chromedriver.exe
============================================================

Open your browser at: http://127.0.0.1:5000

 * Serving Flask app 'app'
 * Debug mode: off
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
Step 5.2: Open the Web Interface
Open any browser and go to:

text
http://127.0.0.1:5000
You'll see the GeM Document Scraper interface.

⚠️ Important Reminders
Do NOT close the PowerShell window while using the app — it is the server

The window must stay open for the entire session

The app runs only on your computer — no one else can access it

6. Using the Web Interface
Overview of the Screen
Section	Purpose
Category	Type to search GeM categories
From date / To date	Date range to search
Run Scraper	Start the download
Progress	Live log of what's happening
Downloaded Files	Click to download each PDF
Step 6.1: Wait for Categories to Load
When the page opens, the text under the Category field says:

text
Loading categories from GeM...
Wait 10–30 seconds. It will change to:

text
342 categories loaded. Type to search.
If it doesn't change after 60 seconds → see Section 9 (Troubleshooting)

Step 6.2: Select a Category
Click the Category field

Start typing a keyword (e.g., labels, laptop, printer)

A dropdown will show matching categories

Click the one you want

Example:

Type: label

Options shown: Labels Stickers, Labels Stickers(V3), Label Printing

Click: Labels Stickers(V3)

Step 6.3: Set the Date Range
Enter dates in DD-MM-YYYY format:

Field	Example	Means
From date	01-09-2026	1 September 2026
To date	05-09-2026	5 September 2026
⚠️ Common mistakes:

❌ 2026-09-01 (wrong format — that's YYYY-MM-DD)

❌ 1-9-2026 (missing leading zeros)

✅ 01-09-2026 (correct)

Step 6.4: Click "Run Scraper"
A Chrome window will pop up — this is normal. The scraper is driving Chrome.

Step 6.5: Watch the Progress Log
The log box will fill with messages:

text
Opening GeM portal...
Selecting category: Labels Stickers(V3)
Setting date range: 01-09-2026 to 05-09-2026
Solving CAPTCHA (may retry a few times)...
Captcha attempt 1 failed, retrying...
Captcha attempt 2 failed, retrying...
Captcha accepted! Loading the Documents.
Scrolling to load all documents...
   20 documents loaded
   47 documents loaded
   47 documents loaded
Total documents found: 47
Downloading document 1/47...
Captcha accepted! Proceeding to download Contracts.
Downloading document 2/47...
...
Done! 47 files saved to C:\...\gem_downloads
The CAPTCHA retries are normal. Do not worry — the script handles them.

Step 6.6: Download the Files
After the scrape finishes:

Scroll down to Downloaded Files

Each PDF appears as a blue clickable link

Click any link to download that file to your PC

Or click Refresh to see the latest list.

⏱️ Timing Expectations
Number of Documents	Estimated Time
1–10	2–5 minutes
11–50	10–30 minutes
51–200	30 minutes – 2 hours
Do not close the browser or PowerShell during this time.

7. Where Files Are Saved
Default Location
text
C:\Users\<YourName>\Downloads\GeM-Document-Scraper\gem_downloads\
To Open the Folder Quickly
powershell
cd "C:\Users\<YourName>\Downloads\GeM-Document-Scraper\gem_downloads"
ii .
File Naming
Files keep their original GeM names:

text
GEMC-511687755678653-28112024.pdf
GEMC-511687797936727-19122024.pdf
GEM-511687708301996-27022026.pdf
To Change the Download Folder
Edit config.py:

python
DOWNLOAD_DIR = r"C:\Your\Preferred\Folder"
8. Stopping the App
Step 8.1: Stop the Server
In the PowerShell window, press:

text
Ctrl + C
You'll see:

text
Keyboard interrupt received, exiting.
Step 8.2: Close the Browser Tab
Close the tab showing http://127.0.0.1:5000.

Step 8.3: Kill Any Leftover Chrome (if needed)
If Chrome windows remain open after the scrape:

powershell
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force
9. Troubleshooting Guide
Error 1: python command not recognized
Symptom:

text
python : The term 'python' is not recognized
Fix:

Reinstall Python (Step 4.1), making sure to check "Add Python to PATH"

OR use py instead of python:

powershell
py app.py
Error 2: ModuleNotFoundError: No module named 'flask'
Symptom:

text
ModuleNotFoundError: No module named 'flask'
Fix:

powershell
python -m pip install flask selenium pytesseract Pillow pandas openpyxl
If that fails, try with py:

powershell
py -m pip install flask selenium pytesseract Pillow pandas openpyxl
Error 3: Unable to obtain driver for chrome
Symptom:

text
ChromeDriver failed: Message: Unable to obtain driver for chrome
Cause: ChromeDriver version doesn't match Chrome.

Fix:

Check Chrome version at chrome://settings/help

Download matching ChromeDriver (Step 4.4)

Replace chromedriver.exe in the project folder

Restart python app.py

Verify the driver version:

powershell
& ".\chromedriver.exe" --version
Should print the same major version as Chrome.

Error 4: TesseractNotFoundError
Symptom:

text
TesseractNotFoundError: tesseract is not installed
Fix:

Reinstall Tesseract (Step 4.3)

Verify it's at C:\Program Files\Tesseract-OCR\tesseract.exe

Run python config.py to confirm detection

Error 5: Could not locate element with visible text: <category>
Symptom:

text
NoSuchElementException: Could not locate element with visible text: Labels Stickers(V3)
Cause: Category name doesn't match GeM's exact string.

Fix:
Look at the terminal output — the script prints close matches:

text
Close matches available on GeM:
   text  = 'Labels Stickers (V3)'
   value = '12346'
Copy the exact text value (including spaces) into the Category field.

Error 6: Could not get past the first CAPTCHA
Symptom:

text
Captcha attempt 15 failed, retrying...
Captcha failed after 15 attempts.
Cause: OCR can't read the distorted CAPTCHA.

Fix:

Click Run Scraper again — a fresh CAPTCHA may be easier

Check Chrome window — if the CAPTCHA is very distorted, wait and retry

If it consistently fails, GeM may have changed their CAPTCHA style

Error 7: GeM page doesn't load
Symptom: Chrome opens to a blank page or an error page.

Cause: Your IP may be blocked (GeM is India-only in some regions).

Fix:

Enable a VPN with an India server

Retry the scrape

If you're already in India, check your firewall/antivirus

Error 8: Address already in use
Symptom:

text
OSError: [WinError 10048] Only one usage of each socket address
Cause: A previous server is still running on port 5000.

Fix:

powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Then restart python app.py.

Error 9: App starts but page shows "This site can't be reached"
Fix:

Confirm the terminal shows Running on http://127.0.0.1:5000

Try a different browser

Confirm you typed http:// not https://

Error 10: Downloaded files list is empty
Symptom: Scrape finished, but no files appear.

Fix:

Check the log for errors:

"No result found" — no contracts match the date range → widen dates

"Failed on document N" — individual PDF failed → retry

Check the folder directly:

powershell
Get-ChildItem "$env:USERPROFILE\Downloads\GeM-Document-Scraper\gem_downloads"
10. Maintenance & Updates
Weekly
✅ Run python app.py to test the app still works

✅ Check gem_downloads/ folder and archive old PDFs

✅ Delete old CAPTCHA images in captcha/ (safe to remove)

Monthly
✅ Update Chrome (Chrome auto-updates)

✅ Check for a newer ChromeDriver version matching your Chrome

✅ Update Python packages:

powershell
python -m pip install --upgrade flask selenium pytesseract Pillow pandas openpyxl
When Chrome Updates
Note the new Chrome version

Download the matching ChromeDriver from https://googlechromelabs.github.io/chrome-for-testing/

Replace chromedriver.exe in the project folder

Restart the app

Backup Recommendation
Keep a copy of your config.py and .gitignore

The rest can be re-downloaded from GitHub anytime

11. Complete Code Reference
This section contains the full source code for every file in the project. Use it to rebuild the app from scratch or verify a fresh installation.

📁 Project Structure
text
GeM-Document-Scraper/
├── app.py                  ← Flask web server
├── actions.py              ← Scraper actions (Selenium)
├── config.py               ← Auto-detection of paths
├── requirements.txt        ← Python dependencies
├── setup.bat               ← Windows installer script
├── setup.sh                ← Mac/Linux installer script
├── README.md               ← GitHub readme
├── .gitignore              ← Git ignore rules
├── chromedriver.exe        ← (You download this)
├── templates/
│   └── index.html          ← Web UI page
└── static/
    └── style.css           ← UI styling
📄 config.py
python
"""Auto-detect paths for Tesseract, ChromeDriver, and download folder."""
import os
import sys
import shutil
import platform

IS_WINDOWS = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "gem_downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def find_tesseract():
    found = shutil.which("tesseract")
    if found:
        return found
    candidates = []
    if IS_WINDOWS:
        candidates = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Tesseract-OCR", "tesseract.exe"),
            os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local", "Programs", "Tesseract-OCR", "tesseract.exe"),
        ]
    elif IS_MAC:
        candidates = ["/usr/local/bin/tesseract", "/opt/homebrew/bin/tesseract", "/usr/bin/tesseract"]
    else:
        candidates = ["/usr/bin/tesseract", "/usr/local/bin/tesseract", "/snap/bin/tesseract"]
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return None


def find_chromedriver():
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
    print("=" * 60)
    print("  GeM Document Scraper — Environment Check")
    print("=" * 60)
    print(f"  OS              : {platform.system()} {platform.release()}")
    print(f"  Python          : {sys.version.split()[0]}")
    print(f"  Project folder  : {BASE_DIR}")
    print(f"  Download folder : {DOWNLOAD_DIR}")
    print(f"  Tesseract OCR   : {TESSERACT_PATH or 'NOT FOUND'}")
    print(f"  ChromeDriver    : {CHROMEDRIVER_PATH or 'not found (Selenium will auto-download)'}")
    print("=" * 60)
    if not TESSERACT_PATH:
        print("\n  Tesseract OCR is not installed.")
        print("  Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  During install, check 'English' language data.\n")


if __name__ == "__main__":
    report()
📄 actions.py
python
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import base64
import re
from PIL import Image
import pytesseract
import time
import os

from config import TESSERACT_PATH

if TESSERACT_PATH:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def select_category(driver, category):
    element = Select(driver.find_element(By.ID, "buyer_category"))
    for opt in element.options:
        if opt.text.strip() == category.strip():
            element.select_by_visible_text(opt.text)
            print(f"Selected Category (exact): {opt.text}")
            return
    normalized = category.replace(" ", "").lower()
    for opt in element.options:
        if opt.text.replace(" ", "").lower() == normalized:
            element.select_by_visible_text(opt.text)
            print(f"Selected Category (normalized): {opt.text}")
            return
    for opt in element.options:
        if normalized in opt.text.replace(" ", "").lower():
            element.select_by_visible_text(opt.text)
            print(f"Selected Category (substring): {opt.text}")
            return
    print(f"Category not found: {category!r}")
    print("Close matches available on GeM:")
    for opt in element.options:
        t = opt.text.lower()
        if "label" in t or "sticker" in t or category.split()[0].lower() in t:
            print(f"   text  = {opt.text!r}")
            print(f"   value = {opt.get_attribute('value')!r}")
    raise ValueError(f"Category not found: {category}")


def select_date_range(driver, from_date, to_date):
    from_date_element = driver.find_element(By.ID, "from_date_contract_search1")
    to_date_element = driver.find_element(By.ID, "to_date_contract_search1")
    driver.execute_script("arguments[0].removeAttribute('readonly')", from_date_element)
    driver.execute_script("arguments[0].removeAttribute('readonly')", to_date_element)
    from_date_element.clear()
    from_date_element.send_keys(from_date)
    to_date_element.clear()
    to_date_element.send_keys(to_date)
    print(f"Selected Date Range: {from_date} to {to_date}")


def extract_captcha(driver, img_id):
    captcha_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captcha")
    os.makedirs(captcha_folder, exist_ok=True)
    try:
        captcha_img = driver.find_element(By.ID, img_id)
        img_src = captcha_img.get_attribute("src")
        match = re.search(r"base64,(.*)", img_src)
        if match:
            image_data = base64.b64decode(match.group(1))
            with open(os.path.join(captcha_folder, "captcha.jpg"), "wb") as f:
                f.write(image_data)
        else:
            print("Failed to read Captcha! Refreshing and Retrying.")
    except Exception as e:
        print(f"Error in Extracting the Captcha: {e}")


def read_captcha():
    captcha_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captcha", "captcha.jpg")
    try:
        image = Image.open(captcha_file)
        text = pytesseract.image_to_string(image)
        return text.replace(" ", "").strip()
    except Exception as e:
        print(f"Error reading Captcha: {e}")
        return ""


def refresh_captcha(driver, img_id):
    try:
        print("Refreshing Captcha...")
        refresh_button = driver.find_element(By.XPATH, "//a[contains(@onclick, 'loadCap1')]")
        refresh_button.click()
        time.sleep(2)
        extract_captcha(driver, img_id)
    except Exception as e:
        print(f"Error refreshing Captcha: {e}")


def enter_captcha(driver, captcha_code, img_id):
    attempts = 0
    max_attempts = 15
    while attempts < max_attempts:
        attempts += 1
        extract_captcha(driver, img_id)
        captcha = read_captcha()
        if not captcha:
            refresh_captcha(driver, img_id)
            continue
        cap_input = driver.find_element(By.ID, captcha_code)
        cap_input.clear()
        cap_input.send_keys(captcha)
        search_button = driver.find_element(By.ID, "searchlocation1")
        driver.execute_script("arguments[0].click();", search_button)
        time.sleep(2)
        try:
            error = driver.find_element(By.ID, "pcaptcha_code1").text.strip()
            if error:
                print(f"Captcha attempt {attempts} failed, retrying...")
                refresh_captcha(driver, img_id)
            else:
                print("Captcha accepted! Loading the Documents.")
                return True
        except Exception:
            print("Captcha accepted! Loading the Documents.")
            return True
    print(f"Captcha failed after {max_attempts} attempts.")
    return False


def enter_captcha_and_download(driver, captcha_code):
    h_captcha_value = driver.find_element(By.ID, "h_captcha").get_attribute("value")
    cap_input = driver.find_element(By.ID, captcha_code)
    cap_input.send_keys(h_captcha_value)
    driver.find_element(By.ID, "modelsbt").click()
    time.sleep(1)
    download_button = driver.find_element(By.ID, "dwnbtn")
    print("Captcha accepted! Proceeding to download Contracts.")
    download_button.click()
📄 app.py
python
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import tempfile
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from actions import enter_captcha, select_category, select_date_range, enter_captcha_and_download
from config import DOWNLOAD_DIR, CHROMEDRIVER_PATH, report

app = Flask(__name__)


def build_chrome_options(headless=False, download_dir=None):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
    else:
        opts.add_argument("--start-maximized")
    opts.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")
    opts.add_argument("--no-first-run")
    opts.add_argument("--no-default-browser-check")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-popup-blocking")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--remote-allow-origins=*")
    if download_dir:
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
        }
        opts.add_experimental_option("prefs", prefs)
    return opts


def make_driver(headless=False, download_dir=None):
    opts = build_chrome_options(headless=headless, download_dir=download_dir)
    if CHROMEDRIVER_PATH:
        service = Service(executable_path=CHROMEDRIVER_PATH)
        return webdriver.Chrome(service=service, options=opts)
    return webdriver.Chrome(options=opts)


state = {
    "running": False,
    "log": [],
    "downloaded": 0,
    "total": 0,
    "done": False,
    "error": None,
}


def log(msg):
    print(msg)
    state["log"].append(msg)


def run_scraper(category, from_date, to_date):
    state.update({"running": True, "log": [], "downloaded": 0,
                  "total": 0, "done": False, "error": None})
    try:
        driver = make_driver(headless=False, download_dir=DOWNLOAD_DIR)
    except Exception as e:
        log(f"ChromeDriver failed to start: {e}")
        state["error"] = f"ChromeDriver failed: {e}"
        state["running"] = False
        return
    try:
        log("Opening GeM portal...")
        driver.get("https://gem.gov.in/view_contracts")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "buyer_category")))
        time.sleep(2)
        log(f"Selecting category: {category}")
        select_category(driver=driver, category=category)
        log(f"Setting date range: {from_date} to {to_date}")
        select_date_range(driver=driver, from_date=from_date, to_date=to_date)
        log("Solving CAPTCHA (may retry a few times)...")
        if not enter_captcha(driver=driver, captcha_code="captcha_code1", img_id="captchaimg1"):
            state["error"] = "Could not get past the first CAPTCHA."
            log("First CAPTCHA failed.")
            return
        log("Scrolling to load all documents...")
        last_count, stable = 0, 0
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            count = len(driver.find_elements(By.CLASS_NAME, "border.block"))
            log(f"   {count} documents loaded")
            if count == last_count:
                stable += 1
                if stable >= 2:
                    break
            else:
                stable = 0
            last_count = count
        documents = driver.find_elements(By.CLASS_NAME, "border.block")
        state["total"] = len(documents)
        log(f"Total documents found: {len(documents)}")
        for i, doc in enumerate(documents, 1):
            log(f"Downloading document {i}/{len(documents)}...")
            try:
                link = doc.find_element(By.TAG_NAME, "a")
                driver.execute_script("arguments[0].click();", link)
                time.sleep(2)
                enter_captcha_and_download(driver=driver, captcha_code="captcha_code")
                state["downloaded"] = i
                time.sleep(5)
                documents = driver.find_elements(By.CLASS_NAME, "border.block")
            except Exception as e:
                log(f"   Failed on document {i}: {e}")
                continue
        log(f"Done! {state['downloaded']} files saved to {DOWNLOAD_DIR}")
        state["done"] = True
    except Exception as e:
        state["error"] = str(e)
        log(f"ERROR: {e}")
    finally:
        time.sleep(2)
        try:
            driver.quit()
        except Exception:
            pass
        state["running"] = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/categories")
def categories():
    try:
        driver = make_driver(headless=True)
    except Exception as e:
        return jsonify({"error": f"ChromeDriver failed: {e}"}), 500
    try:
        driver.get("https://gem.gov.in/view_contracts")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "buyer_category")))
        time.sleep(2)
        dropdown = Select(driver.find_element(By.ID, "buyer_category"))
        cats = [o.text.strip() for o in dropdown.options
                if o.text.strip() and not o.text.strip().startswith("--")]
        return jsonify(cats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            driver.quit()
        except Exception:
            pass


@app.route("/start", methods=["POST"])
def start():
    if state["running"]:
        return jsonify({"error": "Already running"}), 400
    data = request.json
    category = data.get("category", "").strip()
    from_date = data.get("from_date", "").strip()
    to_date = data.get("to_date", "").strip()
    if not category or not from_date or not to_date:
        return jsonify({"error": "Missing fields"}), 400
    threading.Thread(target=run_scraper, args=(category, from_date, to_date)).start()
    return jsonify({"ok": True})


@app.route("/status")
def status():
    return jsonify(state)


@app.route("/files")
def files():
    try:
        items = []
        for f in os.listdir(DOWNLOAD_DIR):
            path = os.path.join(DOWNLOAD_DIR, f)
            if os.path.isfile(path):
                items.append({"name": f, "size": os.path.getsize(path)})
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    report()
    print("\nOpen your browser at: http://127.0.0.1:5000\n")
    app.run(host="127.0.0.1", port=5000, debug=False)
📄 requirements.txt
text
flask>=3.0
selenium>=4.20
pytesseract>=0.3.10
Pillow>=10.0
pandas>=2.0
openpyxl>=3.1
📄 templates/index.html
html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GeM Document Scraper</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
<div class="container">
    <h1>GeM Document Scraper</h1>
    <div class="card">
        <label>Category</label>
        <input id="category" list="catlist" placeholder="Type to search...">
        <datalist id="catlist"></datalist>
        <small id="catstatus">Loading categories from GeM...</small>
        <label>From date (DD-MM-YYYY)</label>
        <input id="from_date" value="01-09-2026">
        <label>To date (DD-MM-YYYY)</label>
        <input id="to_date" value="05-09-2026">
        <button id="runBtn">Run Scraper</button>
        <div id="runstatus"></div>
    </div>
    <div class="card">
        <h3>Progress</h3>
        <div id="progress">0 / 0</div>
        <pre id="log"></pre>
    </div>
    <div class="card">
        <h3>Downloaded Files</h3>
        <ul id="files"></ul>
        <button id="refreshFiles">Refresh</button>
    </div>
</div>
<script>
async function loadCategories() {
    const res = await fetch('/categories');
    const data = await res.json();
    const list = document.getElementById('catlist');
    list.innerHTML = '';
    if (Array.isArray(data)) {
        data.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            list.appendChild(opt);
        });
        document.getElementById('catstatus').textContent =
            `${data.length} categories loaded. Type to search.`;
    } else {
        document.getElementById('catstatus').textContent =
            'Could not load categories: ' + (data.error || 'unknown error');
    }
}
async function startScraper() {
    const category = document.getElementById('category').value.trim();
    const from_date = document.getElementById('from_date').value.trim();
    const to_date = document.getElementById('to_date').value.trim();
    if (!category || !from_date || !to_date) {
        alert('Please fill all fields');
        return;
    }
    const res = await fetch('/start', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({category, from_date, to_date})
    });
    const data = await res.json();
    if (data.error) {
        alert(data.error);
    } else {
        document.getElementById('runstatus').textContent = 'Running...';
        pollStatus();
    }
}
async function pollStatus() {
    const res = await fetch('/status');
    const s = await res.json();
    document.getElementById('log').textContent = s.log.join('\n');
    document.getElementById('log').scrollTop = document.getElementById('log').scrollHeight;
    document.getElementById('progress').textContent = `${s.downloaded} / ${s.total}`;
    if (s.error) {
        document.getElementById('runstatus').textContent = 'Error: ' + s.error;
    } else if (s.done) {
        document.getElementById('runstatus').textContent = 'Finished!';
    }
    if (s.running) {
        setTimeout(pollStatus, 1500);
    } else {
        loadFiles();
    }
}
async function loadFiles() {
    const res = await fetch('/files');
    const items = await res.json();
    const ul = document.getElementById('files');
    ul.innerHTML = '';
    if (Array.isArray(items)) {
        items.forEach(f => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '/download/' + encodeURIComponent(f.name);
            a.textContent = f.name;
            li.appendChild(a);
            li.append(` (${(f.size/1024).toFixed(1)} KB)`);
            ul.appendChild(li);
        });
    }
}
document.getElementById('runBtn').addEventListener('click', startScraper);
document.getElementById('refreshFiles').addEventListener('click', loadFiles);
loadCategories();
loadFiles();
</script>
</body>
</html>
📄 static/style.css
css
* { box-sizing: border-box; }
body {
    font-family: system-ui, -apple-system, Segoe UI, sans-serif;
    background: #f0f4f8;
    margin: 0;
    padding: 20px;
    color: #1f2937;
}
.container { max-width: 900px; margin: 0 auto; }
h1 { text-align: center; color: #0b3d91; }
.card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
label { display: block; margin-top: 12px; font-weight: 600; font-size: 14px; }
input {
    width: 100%;
    padding: 10px;
    margin-top: 4px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 14px;
}
button {
    margin-top: 16px;
    padding: 10px 20px;
    background: #0b3d91;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 15px;
    cursor: pointer;
}
button:hover { background: #082d6e; }
small { color: #64748b; display: block; margin-top: 4px; }
#log {
    background: #0f172a;
    color: #7dd3fc;
    padding: 12px;
    border-radius: 6px;
    max-height: 300px;
    overflow-y: auto;
    font-size: 12px;
    white-space: pre-wrap;
}
#files { list-style: none; padding: 0; }
#files li { padding: 6px 0; border-bottom: 1px solid #e5e7eb; font-size: 14px; }
#files a { color: #0b3d91; text-decoration: none; }
#files a:hover { text-decoration: underline; }
📄 .gitignore
text
__pycache__/
*.pyc
gem_downloads/
captcha/
chromedriver.exe
chromedriver
chromedriver-win64/
.venv/
venv/
.vscode/
.idea/
*.log
📄 setup.bat (Windows)
bat
@echo off
echo ============================================================
echo   GeM Document Scraper - Setup
echo ============================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python not found. Install from https://python.org
    echo     Check "Add Python to PATH" during install.
    pause
    exit /b 1
)
echo [OK] Python detected

echo.
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo [X] Dependency install failed.
    pause
    exit /b 1
)
echo [OK] Dependencies installed

echo.
where tesseract >nul 2>&1
if errorlevel 1 (
    if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
        echo [OK] Tesseract found
    ) else (
        echo [!] Tesseract OCR not found.
        echo     Download: https://github.com/UB-Mannheim/tesseract/wiki
    )
) else (
    echo [OK] Tesseract is on PATH
)

echo.
where chrome >nul 2>&1
if errorlevel 1 (
    if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
        echo [OK] Chrome found
    ) else (
        echo [!] Chrome not detected. Install from https://google.com/chrome
    )
) else (
    echo [OK] Chrome is on PATH
)

echo.
echo ============================================================
echo   Setup complete!
echo   Run:   python app.py
echo   Open:  http://127.0.0.1:5000
echo ============================================================
pause
📄 setup.sh (Mac/Linux)
bash
#!/bin/bash
echo "============================================================"
echo "  GeM Document Scraper - Setup"
echo "============================================================"

if ! command -v python3 &> /dev/null; then
    echo "[X] Python 3 not found."
    exit 1
fi
echo "[OK] Python: $(python3 --version)"

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
echo "[OK] Dependencies installed"

if ! command -v tesseract &> /dev/null; then
    echo "[!] Tesseract not installed. Mac: brew install tesseract"
    echo "    Linux: sudo apt install tesseract-ocr"
else
    echo "[OK] Tesseract: $(which tesseract)"
fi

echo "============================================================"
echo "  Setup complete!  Run:  python3 app.py"
echo "  Open: http://127.0.0.1:5000"
echo "============================================================"
12. FAQ
Q1: Can I run this on my phone?
No. Selenium needs Chrome on a desktop OS. Mobile browsers can't drive other browsers.

Q2: Can I host this online for free?
Not reliably. GeM may block non-Indian server IPs, and free hosts don't always allow Chrome. Local run is the most reliable path.

Q3: Can I schedule this to run automatically?
Yes — use Windows Task Scheduler to run python app.py at a fixed time, or write a small script that calls the scraper directly without the web UI.

Q4: How do I update when Chrome updates?
Download the new ChromeDriver version from https://googlechromelabs.github.io/chrome-for-testing/ and replace chromedriver.exe in the project folder.

Q5: Where are the PDFs saved?
gem_downloads/ inside the project folder. You can change this in config.py.

Q6: Can I scrape multiple categories at once?
Not in the current version — one category per run. Repeat the process for each category.

Q7: What if the CAPTCHA keeps failing?
Try again — some CAPTCHAs are more distorted than others. If it never works, GeM may have changed their CAPTCHA style.

Q8: Can I share this with a colleague?
Yes. They need Python, Chrome, and Tesseract installed. Send them the GitHub link and this SOP.

Q9: Is it legal to scrape GeM?
Scraping public government data is generally allowed for personal use, but respect GeM's terms of service. Don't hammer the server — that's why the scraper adds delays between actions.

Q10: Can I contribute improvements?
Yes — fork the repo on GitHub, make changes, and submit a pull request.

End of SOP

For issues not covered here, check the terminal output — it usually tells you exactly what went wrong.
