@echo off
cd /d "%~dp0"

python -m PyInstaller --version >nul 2>nul
if errorlevel 1 (
    echo PyInstaller is not installed. Installing...
    python -m pip install pyinstaller
)

python -c "import pypandoc" >nul 2>nul
if errorlevel 1 (
    echo pypandoc_binary is not installed. Installing...
    python -m pip install pypandoc_binary
)

python -m PyInstaller --noconfirm --clean --onefile --windowed --collect-all pypandoc --name "latex公式转换器_免安装" latex_to_word_app.py
if exist "dist\latex公式转换器_免安装.exe" (
    echo.
    echo Build complete: dist\latex公式转换器_免安装.exe
)
pause
