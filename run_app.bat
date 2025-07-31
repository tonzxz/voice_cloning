@echo off
echo Starting Geria Voice Cloning...
echo.
echo Opening browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

cd /d "c:\Macbook\Others\voicee\XTTS-v2"

REM Start the Streamlit app in the background
start "" "C:\Users\cabai\AppData\Local\Programs\Python\Python312\python.exe" -m streamlit run app.py

REM Wait a moment for the server to start, then open browser
timeout /t 3 /nobreak >nul
start "" http://localhost:8501

REM Keep the command window open
echo.
echo Geria Voice Cloning is running!
echo.
echo Browser should open automatically at: http://localhost:8501
echo.
echo To stop the application:
echo 1. Close this command window, OR
echo 2. Press Ctrl+C in the Streamlit window
echo.
pause
