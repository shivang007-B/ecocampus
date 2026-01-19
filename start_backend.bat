@echo off
REM Start Backend Server

echo Starting EcoCampus Backend...
echo.
echo Server will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.

python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
