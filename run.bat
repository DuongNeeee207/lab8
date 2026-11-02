@echo off
title FashionStore Django Server
chcp 65001 > nul
cd /d "%~dp0"
set "PYTHONPATH=%~dp0venv\Lib\site-packages"
echo ========================================================
echo        FASHIONSTORE - MÁY CHỦ BÁN HÀNG DJANGO
echo ========================================================
echo.
echo [1] Đang khởi chạy máy chủ tại: http://127.0.0.1:8000/
echo [2] Nhấn Ctrl + C để dừng máy chủ.
echo.
"C:\Users\ThinkPad\AppData\Local\Programs\Python\Python313\python.exe" manage.py runserver
pause
