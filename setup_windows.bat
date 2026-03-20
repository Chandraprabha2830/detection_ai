@echo off
echo ============================================
echo  AI Detection Engine - Windows Setup
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please download and install Python from:
    echo   https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During install, check "Add Python to PATH"
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

REM Upgrade pip
echo [1/5] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo [2/5] Installing dependencies...
python -m pip install -r requirements.txt
echo.

REM Check MySQL
echo [3/5] Checking MySQL...
mysql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] MySQL not found in PATH.
    echo Please install MySQL from https://dev.mysql.com/downloads/installer/
    echo Then run: mysql -u root -p ^< schema.sql
) else (
    echo [OK] MySQL found. To setup DB run:
    echo   mysql -u root -p ^< schema.sql
)
echo.

REM Train ML models
echo [4/5] Training ML models...
python train_model.py
echo.

REM Done
echo [5/5] Setup complete!
echo.
echo ============================================
echo  To start the app, run:  python app.py
echo  Then open: http://localhost:5000
echo  Admin login: admin@aidetection.com / admin123
echo ============================================
echo.
pause
