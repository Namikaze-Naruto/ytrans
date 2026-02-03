@echo off
echo ========================================
echo   GitHub Repository Setup
echo ========================================
echo.
echo This script will push your code to GitHub
echo Repository: https://github.com/SenjuSama/ytrans
echo.
echo IMPORTANT: Make sure you have created the repository on GitHub first!
echo Go to: https://github.com/new
echo Repository name: ytrans
echo Make sure it's EMPTY (no README, no .gitignore)
echo.
pause
echo.
echo Adding remote...
git remote add origin https://github.com/SenjuSama/ytrans.git
echo.
echo Pushing to GitHub...
git push -u origin main
echo.
echo ========================================
echo   Done! Check your repository at:
echo   https://github.com/SenjuSama/ytrans
echo ========================================
pause
