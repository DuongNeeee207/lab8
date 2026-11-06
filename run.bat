@echo off
title FashionStore - Khoi Chay Website Ban Hang
chcp 65001 > nul
cd /d "%~dp0"

echo =========================================================================
echo               FASHIONSTORE - MAY CHU BAN HANG DJANGO
echo =========================================================================
echo.

:: 1. Uu tien tim kiem Python hop le tren he thong
set "PY_CMD="

if exist "%~dp0venv\Scripts\python.exe" (
    set "PY_CMD=%~dp0venv\Scripts\python.exe"
)

if "%PY_CMD%"=="" if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
)
if "%PY_CMD%"=="" if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
)
if "%PY_CMD%"=="" if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
)
if "%PY_CMD%"=="" if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
)

if "%PY_CMD%"=="" (
    py -3 -c "import sys" >nul 2>nul
    if not errorlevel 1 set "PY_CMD=py -3"
)

if "%PY_CMD%"=="" (
    python -c "import sys" >nul 2>nul
    if not errorlevel 1 set "PY_CMD=python"
)

if "%PY_CMD%"=="" (
    echo [LOI] Khong tim thay Python tren may tinh cua ban!
    echo Vui long cai dat Python tu https://www.python.org/
    pause
    exit /b 1
)

:: 2. Tu dong nhan dien thu muc vendor va site-packages
if exist "%~dp0vendor" (
    set "PYTHONPATH=%~dp0vendor;%PYTHONPATH%"
)
if exist "%~dp0venv\Lib\site-packages" (
    set "PYTHONPATH=%~dp0venv\Lib\site-packages;%PYTHONPATH%"
)

:: 3. Kiem tra va cai dat OFFLINE neu may chua co Django hoac Pillow
%PY_CMD% -c "import django, PIL" >nul 2>nul
if errorlevel 1 (
    echo.
    echo =========================================================================
    echo [THONG BAO] Phat hien may chua cai dat thu vien Django / Pillow!
    if exist "%~dp0wheels" (
        echo [THONG BAO] Dang tu dong cai dat OFFLINE tu thu muc 'wheels' (khong can mang)...
        echo [THONG BAO] Qua trinh nay chi mat khoang 2 - 5 giay, vui long cho...
        %PY_CMD% -m pip install --no-index --find-links="%~dp0wheels" -r "%~dp0requirements.txt" >nul 2>nul
        if errorlevel 1 (
            echo [THONG BAO] Dang thu cai dat che do --user...
            %PY_CMD% -m pip install --user --no-index --find-links="%~dp0wheels" -r "%~dp0requirements.txt"
        )
    ) else (
        echo [THONG BAO] Dang tai va cai dat thu vien tu Internet...
        %PY_CMD% -m pip install -r "%~dp0requirements.txt"
    )
    echo [OK] Cai dat thu vien hoan tat!
    echo =========================================================================
)

:: 4. Thong bao khoi dong
echo.
echo [OK] Dang khoi dong may chu tai: http://127.0.0.1:8000/
echo [OK] Trinh duyet web se tu dong mo ngay bay gio...
echo [OK] Nhan to hop phim Ctrl + C de dung may chu.
echo =========================================================================
echo.

start http://127.0.0.1:8000/
%PY_CMD% manage.py runserver 127.0.0.1:8000
pause
