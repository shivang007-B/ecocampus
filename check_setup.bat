@echo off
REM EcoCampus Backend Setup - Final Verification Checklist (Windows)

setlocal enabledelayedexpansion

cls
echo ======================================
echo EcoCampus Backend Setup Verification
echo ======================================
echo.

set passed=0
set failed=0

REM Check directories
echo Checking Directories...
for %%D in (app "app\api" "app\api\v1" "app\api\v1\endpoints" "app\core" "app\models" "app\schemas" "app\services" "app\utils" tests) do (
    if exist "%%D\" (
        echo [OK] %%D\
        set /a passed+=1
    ) else (
        echo [FAIL] %%D\ - NOT FOUND
        set /a failed+=1
    )
)

echo.
echo Checking Critical Files...
for %%F in (
    "app\__init__.py"
    "app\main.py"
    "app\core\config.py"
    "app\core\database.py"
    "app\core\security.py"
    "app\models\user.py"
    "app\models\campus.py"
    "app\models\carbon.py"
    "app\schemas\user.py"
    "app\schemas\campus.py"
    "app\schemas\carbon.py"
    "app\services\carbon_calculator.py"
    "app\services\data_service.py"
    "app\services\iot_service.py"
    "app\utils\constants.py"
    "app\utils\helpers.py"
) do (
    if exist "%%F" (
        echo [OK] %%F
        set /a passed+=1
    ) else (
        echo [FAIL] %%F - NOT FOUND
        set /a failed+=1
    )
)

echo.
echo Checking Configuration Files...
for %%F in (.env requirements.txt docker-compose.yml dockerfile Procfile) do (
    if exist "%%F" (
        echo [OK] %%F
        set /a passed+=1
    ) else (
        echo [FAIL] %%F - NOT FOUND
        set /a failed+=1
    )
)

echo.
echo Checking Documentation...
for %%F in (README.md QUICKSTART.md CONFIG_GUIDE.md SETUP_COMPLETE.md BACKEND_STATUS.md) do (
    if exist "%%F" (
        echo [OK] %%F
        set /a passed+=1
    ) else (
        echo [FAIL] %%F - NOT FOUND
        set /a failed+=1
    )
)

echo.
echo Checking Endpoint Files...
for %%F in (
    "app\api\v1\endpoints\__init__.py"
    "app\api\v1\endpoints\auth.py"
    "app\api\v1\endpoints\users.py"
    "app\api\v1\endpoints\campus.py"
    "app\api\v1\endpoints\carbon.py"
    "app\api\v1\endpoints\iot.py"
) do (
    if exist "%%F" (
        echo [OK] %%F
        set /a passed+=1
    ) else (
        echo [FAIL] %%F - NOT FOUND
        set /a failed+=1
    )
)

echo.
echo ======================================
echo Summary:
echo Passed: %passed%
echo Failed: %failed%
echo ======================================

if %failed% equ 0 (
    echo.
    echo [SUCCESS] All checks passed!
    echo.
    echo Next steps:
    echo 1. pip install -r requirements.txt
    echo 2. docker-compose up -d
    echo 3. python -c "from app.core.database import create_tables; create_tables()"
    echo 4. Access http://localhost:8000/docs
    echo.
    echo For more details, see README.md
    pause
    exit /b 0
) else (
    echo.
    echo [ERROR] Some checks failed!
    pause
    exit /b 1
)
