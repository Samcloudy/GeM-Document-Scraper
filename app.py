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

# ─── Auto-managed ChromeDriver ──────────────────────────────
from webdriver_manager.chrome import ChromeDriverManager

from actions import enter_captcha, select_category, select_date_range, enter_captcha_and_download
from config import DOWNLOAD_DIR, report

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
    """Create a Chrome driver with the auto-managed correct version."""
    opts = build_chrome_options(headless=headless, download_dir=download_dir)
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)


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
        log(f"❌ ChromeDriver failed to start: {e}")
        state["error"] = f"ChromeDriver failed: {e}"
        state["running"] = False
        return

    try:
        log("Opening GeM portal...")
        driver.get('https://gem.gov.in/view_contracts')
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "buyer_category"))
        )
        time.sleep(2)

        log(f"Selecting category: {category}")
        select_category(driver=driver, category=category)

        log(f"Setting date range: {from_date} to {to_date}")
        select_date_range(driver=driver, from_date=from_date, to_date=to_date)

        log("Solving CAPTCHA (may retry a few times)...")
        if not enter_captcha(driver=driver, captcha_code='captcha_code1', img_id='captchaimg1'):
            state["error"] = "Could not get past the first CAPTCHA."
            log("❌ First CAPTCHA failed.")
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
        driver.get('https://gem.gov.in/view_contracts')
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "buyer_category"))
        )
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
    print("\n🌐 Open your browser at: http://127.0.0.1:5000\n")
    app.run(host="127.0.0.1", port=5000, debug=False)