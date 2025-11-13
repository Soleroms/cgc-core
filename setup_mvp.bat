@echo off
REM CGC CORE MVP - Final Setup Script
REM OlympusMont Systems LLC

echo ==========================================
echo   CGC CORE MVP - FINAL SETUP
echo   OlympusMont Systems LLC
echo ==========================================
echo.

cd /d C:\Users\soler\OneDrive\Desktop\cgc-core

echo [1/5] Installing Frontend Dependencies...
call npm install
echo.

echo [2/5] Building Frontend for Production...
call npm run build
echo.

echo [3/5] Committing All Changes to Git...
git add .
git commit -m "MVP v2.1.4 - Production Ready with Full Integration"
echo.

echo [4/5] Pushing to GitHub...
git push origin main
echo.

echo [5/5] Testing Backend Locally...
echo.
echo Starting Python API Server...
echo Test URL: http://localhost:8000/api/health
echo.
python api_server_full.py

echo.
echo ==========================================
echo   SETUP COMPLETE!
echo ==========================================
echo.
echo NEXT STEPS:
echo 1. Railway will auto-deploy backend (2-3 min)
echo 2. Deploy frontend to Vercel
echo 3. Configure DNS in Namecheap
echo 4. Test live at app.olympusmont.com
echo.
echo See DEPLOYMENT.md for detailed instructions
echo.
pause
