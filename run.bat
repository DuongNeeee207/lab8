@echo off
title FashionStore - Khởi Chạy Website Bán Hàng
chcp 65001 > nul
cd /d "%~dp0"

echo =========================================================================
echo               FASHIONSTORE - MÁY CHỦ BÁN HÀNG DJANGO
echo =========================================================================
echo.

:: 1. Tự động tìm Python trên máy
set "PY_CMD="

where python >nul 2>nul
if not errorlevel 1 (
    set "PY_CMD=python"
)

if "%PY_CMD%"=="" (
    where py >nul 2>nul
    if not errorlevel 1 (
        set "PY_CMD=py"
    )
)

if "%PY_CMD%"=="" (
    if exist "C:\Users\ThinkPad\AppData\Local\Programs\Python\Python313\python.exe" (
        set "PY_CMD=C:\Users\ThinkPad\AppData\Local\Programs\Python\Python313\python.exe"
    )
)

if "%PY_CMD%"=="" (
    echo [LỖI] Không tìm thấy Python trên máy tính của bạn!
    echo Vui lòng cài đặt Python từ https://www.python.org/ (nhớ tích chọn 'Add Python to PATH').
    pause
    exit /b 1
)

:: 2. Tự động nhận diện thư viện trong venv đi kèm nếu có
if exist "%~dp0venv\Lib\site-packages" (
    set "PYTHONPATH=%~dp0venv\Lib\site-packages;%PYTHONPATH%"
)

:: 3. Kiểm tra xem Django đã có chưa, nếu máy mới chưa có thì tự động cài đặt
%PY_CMD% -c "import django" >nul 2>nul
if errorlevel 1 (
    echo [THÔNG BÁO] Đang tự động cài đặt các thư viện cần thiết (Django, Pillow, DRF)...
    %PY_CMD% -m pip install -r requirements.txt
)

:: 4. Mở trình duyệt và chạy server
echo.
echo [✓] Đang khởi động máy chủ tại: http://127.0.0.1:8000/
echo [✓] Trình duyệt web sẽ tự động mở...
echo [✓] Nhấn tổ hợp phím Ctrl + C để dừng máy chủ.
echo =========================================================================
echo.

start http://127.0.0.1:8000/
%PY_CMD% manage.py runserver 127.0.0.1:8000
pause
