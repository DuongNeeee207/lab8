@echo off
title FashionStore - Khoi Chay Website Ban Hang
chcp 65001 > nul
cd /d "%~dp0"

echo =========================================================================
echo               FASHIONSTORE - MAY CHU BAN HANG DJANGO
echo =========================================================================
echo.

:: 1. Uu tien dung duong dan Python 3.13 tren may hoac python trong PATH
set "PY_CMD="

if exist "C:\Users\ThinkPad\AppData\Local\Programs\Python\Python313\python.exe" (
    set "PY_CMD=C:\Users\ThinkPad\AppData\Local\Programs\Python\Python313\python.exe"
)

if "%PY_CMD%"=="" (
    where python >nul 2>nul
    if not errorlevel 1 set "PY_CMD=python"
)

if "%PY_CMD%"=="" (
    where py >nul 2>nul
    if not errorlevel 1 set "PY_CMD=py"
)

if "%PY_CMD%"=="" (
    echo [LOI] Khong tim thay Python tren may tinh cua ban!
    echo Vui long cai dat Python tu https://www.python.org/
    pause
    exit /b 1
)

:: 2. Tu dong nhan dien site-packages
if exist "%~dp0venv\Lib\site-packages" (
    set "PYTHONPATH=%~dp0venv\Lib\site-packages;%PYTHONPATH%"
)

:: 3. Kiem tra va cai dat neu may chua co Django
"%PY_CMD%" -c "import django" >nul 2>nul
if errorlevel 1 (
    echo [THONG BAO] Dang tu dong cai dat thu vien can thiet...
    "%PY_CMD%" -m pip install -r requirements.txt
)

:: 4. Thong bao khoi dong
echo.
echo [OK] Dang khoi dong may chu tai: http://127.0.0.1:8000/
echo [OK] Trinh duyet web se tu dong mo ngay bay gio...
echo [OK] Nhan to hop phim Ctrl + C de dung may chu.
echo =========================================================================
echo.

start http://127.0.0.1:8000/
"%PY_CMD%" manage.py runserver 127.0.0.1:8000
pause
