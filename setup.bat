@echo off
echo ============================================================
echo   GeM Document Scraper - Setup
echo ============================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python not found. Install it from https://python.org
    echo     IMPORTANT: Check "Add Python to PATH" during install.
    pause
    exit /b 1
)
echo [OK] Python detected

REM Upgrade pip
echo.
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [X] Dependency install failed.
    pause
    exit /b 1
)
echo [OK] Dependencies installed

REM Check Tesseract
echo.
where tesseract >nul 2>&1
if errorlevel 1 (
    if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
        echo [OK] Tesseract found at C:\Program Files\Tesseract-OCR
    ) else (
        echo [!] Tesseract OCR not found.
        echo     Download it from:
        echo     https://github.com/UB-Mannheim/tesseract/wiki
        echo     Install with "English" language data checked.
        echo.
    )
) else (
    echo [OK] Tesseract is on PATH
)

REM Check Chrome
echo.
where chrome >nul 2>&1
if errorlevel 1 (
    if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
        echo [OK] Chrome found
    ) else (
        echo [!] Google Chrome not detected. Install from https://google.com/chrome
    )
) else (
    echo [OK] Chrome is on PATH
)

echo.
echo ============================================================
echo   Setup complete!
echo.
echo   Run the app with:   python app.py
echo   Then open:          http://127.0.0.1:5000
echo ============================================================
pause