@echo off
REM Railway Deployment Script - Windows
REM Railway'e timeout fix ile deployment yapar

echo ==========================================
echo Railway Timeout Fix Deployment
echo ==========================================
echo.

echo [1/5] Git status kontrol ediliyor...
git status
echo.

echo [2/5] Degisiklikler commit ediliyor...
git add .
git commit -m "Railway timeout fix: connection pool optimization + retry mechanism + health check"
echo.

echo [3/5] Railway'e push ediliyor...
git push
echo.

echo [4/5] Railway logs izleniyor (CTRL+C ile cikabilirsiniz)...
echo.
timeout /t 5 /nobreak
railway logs --tail 50
echo.

echo ==========================================
echo Deployment tamamlandi!
echo ==========================================
echo.
echo Sonraki adimlar:
echo 1. Railway Dashboard'dan deployment durumunu kontrol et
echo 2. Uygulama URL'ini ac ve test et
echo 3. Setup sayfasini kontrol et
echo.

pause
