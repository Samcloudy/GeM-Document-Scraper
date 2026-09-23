# GeM Document Scraper

A web-based tool that automatically downloads contract PDFs from the
Government e-Marketplace (GeM) portal at https://gem.gov.in/view_contracts

## Features

- Web UI — pick category and date range from a browser
- Automatic CAPTCHA solving (OCR)
- Saves PDFs to `gem_downloads/` inside the project folder
- Auto-detects Tesseract and ChromeDriver
- Cross-platform (Windows / macOS / Linux)

## Requirements

| Tool | Purpose | Download |
|------|---------|----------|
| Python 3.10+ | Runs the app | https://python.org |
| Google Chrome | Browser that Selenium drives | https://google.com/chrome |
| Tesseract OCR | Reads CAPTCHA images | https://github.com/UB-Mannheim/tesseract/wiki |

> ⚠️ During Tesseract installation, check **English** language data.

## Quick Start

### Windows

```bat
git clone https://github.com/YOUR-USERNAME/GeM-Document-Scraper.git
cd GeM-Document-Scraper
setup.bat
python app.py