@echo off
setlocal
title Push to Fork & Create Pull Request

echo ======================================================================
echo   Step 1: Check Fork on GitHub
echo ======================================================================
echo If you have not created your fork yet, opening the fork page now...
start https://github.com/subhashreevitala/skillproj/fork
echo.
echo Please click "Create fork" on GitHub if you haven't already.
echo Once the fork is created on your GitHub account, press any key to continue.
pause >nul

echo.
echo ======================================================================
echo   Step 2: Configuring Remote Fork (futuretonight/skillproj)
echo ======================================================================
git remote remove myfork >nul 2>&1
git remote add myfork https://github.com/futuretonight/skillproj.git

echo Remote configured:
git remote -v

echo.
echo ======================================================================
echo   Step 3: Pushing Commits to Your Fork
echo ======================================================================
git push -u myfork feature/skillbridge-platform
if errorlevel 1 (
    echo.
    echo Pushing feature branch failed. Trying master branch...
    git push -u myfork master
)

echo.
echo ======================================================================
echo   Step 4: Opening Pull Request on GitHub
echo ======================================================================
echo Opening PR page in your browser...
start https://github.com/subhashreevitala/skillproj/compare/master...futuretonight:skillproj:feature/skillbridge-platform?expand=1

echo.
echo Done! Review your changes on GitHub and click "Create pull request".
echo.
pause
