#!/bin/bash
# EcoCampus Backend Setup Script

echo "================================"
echo "EcoCampus Backend Setup"
echo "================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env 2>/dev/null || cp docker-compose.yml .env
    echo ".env file created. Please update it with your settings."
fi

# Create database
echo "Setting up PostgreSQL database..."
createdb ecocampus -U postgres 2>/dev/null || echo "Database might already exist"

# Create tables
echo "Creating database tables..."
python -c "from app.core.database import create_tables; create_tables()"

echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Update .env file with your API keys and configuration"
echo "2. Start Redis: redis-server"
echo "3. Start MQTT: mosquitto"
echo "4. Run: uvicorn app.main:app --reload"
echo ""
echo "API Documentation: http://localhost:8000/docs"
