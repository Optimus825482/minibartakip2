@echo off
echo ============================================
echo RAILWAY ENVIRONMENT VARIABLES SETUP
echo ============================================
echo.

REM Railway CLI kurulu mu kontrol et
where railway >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Railway CLI bulunamadi!
    echo.
    echo Kurulum icin:
    echo npm install -g @railway/cli
    echo.
    pause
    exit /b 1
)

echo Railway'e baglaniliyor...
railway login

echo.
echo Environment variables ayarlaniyor...
echo.

REM DATABASE_URL (Railway'den al)
echo [1/4] DATABASE_URL ayarlaniyor...
railway variables set DATABASE_URL="postgresql://postgres:NEOcbkYOOSzROELtJEuVZxdPphGLIXnx@shinkansen.proxy.rlwy.net:36747/railway"

REM SECRET_KEY
echo [2/4] SECRET_KEY ayarlaniyor...
railway variables set SECRET_KEY="8f3a9b2c7d1e6f4a5b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a"

REM FLASK_ENV
echo [3/4] FLASK_ENV ayarlaniyor...
railway variables set FLASK_ENV="production"
railway variables set ENV="production"

REM DB_TYPE
echo [4/4] DB_TYPE ayarlaniyor...
railway variables set DB_TYPE="postgresql"

echo.
echo ============================================
echo TAMAMLANDI!
echo ============================================
echo.
echo Kontrol et:
echo railway variables
echo.
echo Deploy et:
echo railway up
echo.
pause
