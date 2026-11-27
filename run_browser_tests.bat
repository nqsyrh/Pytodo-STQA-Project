@echo off
REM =====================================================================
REM  Full Selenium test run of PyTodo Pro in one browser (Windows).
REM  Double-click, or run:  run_browser_tests.bat edge
REM                         run_browser_tests.bat chrome
REM                         run_browser_tests.bat firefox
REM  Results: reports\ui_<browser>.log, reports\ui_<browser>.xml,
REM           reports\browser_<browser>.txt (exact version),
REM           06_Automation_Regression\week 6 evidence\selenium_screenshots\
REM =====================================================================
setlocal
set BROWSER=%1
if "%BROWSER%"=="" set BROWSER=edge
set HEADLESS=0
cd /d "%~dp0"
if not exist reports mkdir reports

echo [1/4] Installing requirements...
python -m pip install -q -r app\requirements.txt -r requirements-test.txt

echo [2/4] Starting PyTodo Pro on http://127.0.0.1:5000 ...
start "PyTodo Pro server" /min cmd /c "cd /d "%~dp0app" && python app.py"
timeout /t 6 /nobreak >nul

echo [3/4] Running the 10 Selenium tests in %BROWSER% (a browser window will open)...
python -m pytest -m ui -v -p no:cacheprovider --junitxml=reports\ui_%BROWSER%.xml > reports\ui_%BROWSER%.log 2>&1

echo [4/4] Compatibility screenshots at desktop, tablet and phone size...
python 03_Special_Testing\scripts\capture_screenshots.py > reports\compat_%BROWSER%.log 2>&1

echo.
echo ===================== RESULT (%BROWSER%) =====================
type reports\browser_%BROWSER%.txt 2>nul
findstr /C:"PASSED" /C:"FAILED" /C:"ERROR" reports\ui_%BROWSER%.log
findstr /R /C:"[0-9]* passed" /C:"[0-9]* failed" reports\ui_%BROWSER%.log
type "03_Special_Testing\week 3 evidence\%BROWSER%\compatibility_result.json" 2>nul
echo ==============================================================
echo Send these to the team / Claude:
echo   reports\ui_%BROWSER%.log
echo   reports\browser_%BROWSER%.txt
echo   06_Automation_Regression\week 6 evidence\selenium_screenshots\
echo   03_Special_Testing\week 3 evidence\%BROWSER%\  (incl. compatibility_result.json)
echo Close the "PyTodo Pro server" window when you are done.
pause
