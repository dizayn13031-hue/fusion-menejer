@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Fusion Menejer Bot
echo ================================================
echo   FUSION MENEJER BOT
echo   Bu oynani YOPMANG - bot shu yerda ishlaydi.
echo ================================================
echo.
where py >nul 2>nul
if %errorlevel%==0 (set PY=py) else (set PY=python)
echo Kutubxonalar o'rnatilmoqda (birinchi marta biroz vaqt oladi)...
%PY% -m pip install --quiet --disable-pip-version-check -r requirements.txt
echo.
echo Bot ishga tushdi. To'xtatish uchun bu oynani yoping.
echo.
%PY% bot.py
echo.
echo Bot to'xtadi. Sababini yuqorida ko'ring.
pause
