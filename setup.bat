@echo off
REM EcoCampus Backend Setup Script for Windows

echo ================================
echo EcoCampus Backend Setup
echo ================================

REM Check Python version
python --version

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env 2>nul || (
        echo APP_NAME=EcoCampus Backend > .env
        echo DEBUG=True >> .env
    )
    echo .env file created. Please update it with your settings.
)

REM Create database
echo Setting up PostgreSQL database...
REM Requires psql to be in PATH
REM createdb ecocampus -U postgres 2>nul

REM Create tables
echo Creating database tables...
python -c "from app.core.database import create_tables; create_tables()"

echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next steps:
echo 1. Update .env file with your API keys and configuration
echo 2. Start Redis: redis-server
echo 3. Start MQTT: mosquitto
echo 4. Run: uvicorn app.main:app --reload
echo.
echo API Documentation: http://localhost:8000/docs
pause
