@echo off
:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and rerun this script.
    pause
    exit /b
)

:: Install PyInstaller if not already installed
pip show pyinstaller >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)


:: Install watchdog if not already installed
pip show watchdog >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Installing watchdog...
    pip install watchdog
)


:: Install Tkinter if not already installed
pip show tkinter >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Installing tkinter...
    pip install tkinter
)


:: Convert the Python script to an executable without a console window
echo Converting main.py to a background executable...
pyinstaller --onefile --noconsole main.py

:: Move into the 'dist' directory where the .exe is generated
cd dist

:: Run the generated executable
echo Running the executable in the background...
start main.exe

pause
