from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import base64
import re
from PIL import Image
import pytesseract
import time
import os

from config import TESSERACT_PATH

# Auto-detected Tesseract path
if TESSERACT_PATH:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def select_category(driver, category):
    """Select a category from the dropdown. Falls back to fuzzy matching."""
    element = Select(driver.find_element(By.ID, 'buyer_category'))

    for opt in element.options:
        if opt.text.strip() == category.strip():
            element.select_by_visible_text(opt.text)
            print(f'✅ Selected Category (exact): {opt.text}')
            return

    normalized = category.replace(" ", "").lower()
    for opt in element.options:
        if opt.text.replace(" ", "").lower() == normalized:
            element.select_by_visible_text(opt.text)
            print(f'✅ Selected Category (normalized): {opt.text}')
            return

    for opt in element.options:
        if normalized in opt.text.replace(" ", "").lower():
            element.select_by_visible_text(opt.text)
            print(f'✅ Selected Category (substring): {opt.text}')
            return

    print(f"❌ Category not found: {category!r}")
    print("Close matches available on GeM:")
    for opt in element.options:
        t = opt.text.lower()
        if 'label' in t or 'sticker' in t or category.split()[0].lower() in t:
            print(f"   text  = {opt.text!r}")
            print(f"   value = {opt.get_attribute('value')!r}")
    raise ValueError(f"Category not found: {category}")


def select_date_range(driver, from_date, to_date):
    """Select the date range for document extraction."""
    from_date_element = driver.find_element(By.ID, 'from_date_contract_search1')
    to_date_element = driver.find_element(By.ID, 'to_date_contract_search1')

    driver.execute_script("arguments[0].removeAttribute('readonly')", from_date_element)
    driver.execute_script("arguments[0].removeAttribute('readonly')", to_date_element)

    from_date_element.clear()
    from_date_element.send_keys(from_date)
    to_date_element.clear()
    to_date_element.send_keys(to_date)

    print(f'✅ Selected Date Range: {from_date} to {to_date}')


def extract_captcha(driver, img_id):
    """Extract and save the CAPTCHA image from base64 data."""
    captcha_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captcha")
    os.makedirs(captcha_folder, exist_ok=True)
    try:
        captcha_img = driver.find_element(By.ID, img_id)
        img_src = captcha_img.get_attribute("src")
        match = re.search(r'base64,(.*)', img_src)
        if match:
            base64_string = match.group(1)
            image_data = base64.b64decode(base64_string)
            captcha_path = os.path.join(captcha_folder, "captcha.jpg")
            with open(captcha_path, "wb") as img_file:
                img_file.write(image_data)
        else:
            print("⚠️ Failed to read Captcha! Refreshing and Retrying.")
    except Exception as e:
        print(f"⚠️ Error in Extracting the Captcha: {e}")


def read_captcha():
    """Read the CAPTCHA using Tesseract OCR."""
    captcha_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captcha", "captcha.jpg")
    try:
        image = Image.open(captcha_file)
        text = pytesseract.image_to_string(image)
        captcha = text.replace(" ", "").strip()
        return captcha
    except Exception as e:
        print(f"⚠️ Error reading Captcha: {e}")
        return ""


def refresh_captcha(driver, img_id):
    """Refresh the CAPTCHA image."""
    try:
        print("🔄 Refreshing Captcha...")
        refresh_button = driver.find_element(By.XPATH, "//a[contains(@onclick, 'loadCap1')]")
        refresh_button.click()
        time.sleep(2)
        extract_captcha(driver, img_id)
    except Exception as e:
        print(f"⚠️ Error refreshing Captcha: {e}")


def enter_captcha(driver, captcha_code, img_id):
    """Enter the CAPTCHA and submit to load the documents."""
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
                print(f"⚠️ Captcha attempt {attempts} failed, retrying...")
                refresh_captcha(driver, img_id)
            else:
                print("✅ Captcha accepted! Loading the Documents.")
                return True
        except Exception:
            print("✅ Captcha accepted! Loading the Documents.")
            return True

    print(f"❌ Captcha failed after {max_attempts} attempts.")
    return False


def enter_captcha_and_download(driver, captcha_code):
    """Enter and submit the CAPTCHA for downloading the document."""
    h_captcha_value = driver.find_element(By.ID, "h_captcha").get_attribute("value")
    cap_input = driver.find_element(By.ID, captcha_code)
    cap_input.send_keys(h_captcha_value)
    search_button = driver.find_element(By.ID, "modelsbt")
    search_button.click()
    time.sleep(1)
    download_button = driver.find_element(By.ID, "dwnbtn")
    print("✅ Captcha accepted! Proceeding to download Contracts.")
    download_button.click()