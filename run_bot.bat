@echo off
echo Starting English Learning Bot...

REM Проверка наличия Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Проверка наличия необходимых файлов
if not exist ".env" (
    echo Error: .env file not found!
    echo Please create .env file with your bot token and admin ID.
    pause
    exit /b 1
)

if not exist "google_sheets.json" (
    echo Warning: google_sheets.json file not found!
    echo Make sure to add it if you want to use Google Sheets functionality.
    timeout /t 5
)

REM Запуск бота
cd /d "%~dp0"
python main.py
pause
