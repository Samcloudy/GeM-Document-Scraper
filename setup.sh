#!/bin/bash
echo "============================================================"
echo "  GeM Document Scraper - Setup"
echo "============================================================"

if ! command -v python3 &> /dev/null; then
    echo "[X] Python 3 not found. Install it first."
    exit 1
fi
echo "[OK] Python detected: $(python3 --version)"

echo ""
echo "Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
echo "[OK] Dependencies installed"

echo ""
if ! command -v tesseract &> /dev/null; then
    echo "[!] Tesseract OCR not installed."
    echo "    Mac:   brew install tesseract"
    echo "    Linux: sudo apt install tesseract-ocr"
else
    echo "[OK] Tesseract found: $(which tesseract)"
fi

echo ""
if ! command -v google-chrome &> /dev/null && ! command -v chromium &> /dev/null; then
    echo "[!] Chrome/Chromium not detected. Install from google.com/chrome"
else
    echo "[OK] Chrome/Chromium found"
fi

echo ""
echo "============================================================"
echo "  Setup complete!"
echo "  Run:  python3 app.py"
echo "  Open: http://127.0.0.1:5000"
echo "============================================================"