@echo off
echo ========================================
echo  Advanced Video Merger - Windows Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python tidak ditemukan!
    echo Silakan install Python dari https://python.org/downloads/
    echo PENTING: Centang "Add Python to PATH" saat install
    pause
    exit /b 1
)

echo Python ditemukan:
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip tidak ditemukan!
    echo Silakan reinstall Python dengan pip
    pause
    exit /b 1
)

echo pip ditemukan:
pip --version
echo.

echo Installing dependencies...
echo ========================================

REM Install each package
echo Installing moviepy...
pip install "moviepy>=2.1.2"
if %errorlevel% neq 0 (
    echo ERROR: Gagal install moviepy
    pause
    exit /b 1
)

echo Installing pillow...
pip install "pillow>=9.2.0"
if %errorlevel% neq 0 (
    echo ERROR: Gagal install pillow
    pause
    exit /b 1
)

echo Installing numpy...
pip install "numpy>=1.25.0"
if %errorlevel% neq 0 (
    echo ERROR: Gagal install numpy
    pause
    exit /b 1
)

echo Installing psutil...
pip install "psutil>=5.9.0"
if %errorlevel% neq 0 (
    echo ERROR: Gagal install psutil
    pause
    exit /b 1
)

echo Installing additional dependencies...
pip install pathlib decorator imageio imageio-ffmpeg proglog tqdm python-dotenv

echo.
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo Testing imports...

python -c "import moviepy; print('✓ moviepy OK')" 2>nul
if %errorlevel% neq 0 (
    echo × moviepy FAILED
) else (
    echo ✓ moviepy OK
)

python -c "from PIL import Image; print('✓ pillow OK')" 2>nul
if %errorlevel% neq 0 (
    echo × pillow FAILED
) else (
    echo ✓ pillow OK
)

python -c "import numpy; print('✓ numpy OK')" 2>nul
if %errorlevel% neq 0 (
    echo × numpy FAILED
) else (
    echo ✓ numpy OK
)

python -c "import psutil; print('✓ psutil OK')" 2>nul
if %errorlevel% neq 0 (
    echo × psutil FAILED
) else (
    echo ✓ psutil OK
)

echo.
echo ========================================
echo Setup completed successfully!
echo.
echo Untuk menjalankan script:
echo   python fast.py
echo.
echo File yang diperlukan:
echo   - fast.py (script utama)
echo   - requirements.txt (daftar dependencies)
echo   - README_Windows.md (dokumentasi)
echo ========================================
pause