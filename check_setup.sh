#!/bin/bash
# EcoCampus Backend Setup - Final Verification Checklist

echo "======================================"
echo "EcoCampus Backend Setup Verification"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

passed=0
failed=0

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((passed++))
    else
        echo -e "${RED}✗${NC} $1 - NOT FOUND"
        ((failed++))
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        ((passed++))
    else
        echo -e "${RED}✗${NC} $1/ - NOT FOUND"
        ((failed++))
    fi
}

echo "Checking Directories..."
check_dir "app"
check_dir "app/api"
check_dir "app/api/v1"
check_dir "app/api/v1/endpoints"
check_dir "app/core"
check_dir "app/models"
check_dir "app/schemas"
check_dir "app/services"
check_dir "app/utils"
check_dir "tests"

echo ""
echo "Checking Critical Files..."
check_file "app/__init__.py"
check_file "app/main.py"
check_file "app/core/config.py"
check_file "app/core/database.py"
check_file "app/core/security.py"
check_file "app/models/user.py"
check_file "app/models/campus.py"
check_file "app/models/carbon.py"
check_file "app/schemas/user.py"
check_file "app/schemas/campus.py"
check_file "app/schemas/carbon.py"
check_file "app/services/carbon_calculator.py"
check_file "app/services/data_service.py"
check_file "app/services/iot_service.py"
check_file "app/utils/constants.py"
check_file "app/utils/helpers.py"

echo ""
echo "Checking Configuration Files..."
check_file ".env"
check_file "requirements.txt"
check_file "docker-compose.yml"
check_file "dockerfile"
check_file "Procfile"

echo ""
echo "Checking Documentation..."
check_file "README.md"
check_file "QUICKSTART.md"
check_file "CONFIG_GUIDE.md"
check_file "SETUP_COMPLETE.md"
check_file "BACKEND_STATUS.md"

echo ""
echo "Checking Endpoint Files..."
check_file "app/api/v1/endpoints/__init__.py"
check_file "app/api/v1/endpoints/auth.py"
check_file "app/api/v1/endpoints/users.py"
check_file "app/api/v1/endpoints/campus.py"
check_file "app/api/v1/endpoints/carbon.py"
check_file "app/api/v1/endpoints/iot.py"

echo ""
echo "======================================"
echo "Summary:"
echo -e "${GREEN}Passed: $passed${NC}"
echo -e "${RED}Failed: $failed${NC}"
echo "======================================"

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. pip install -r requirements.txt"
    echo "2. docker-compose up -d (or start services locally)"
    echo "3. python -c 'from app.core.database import create_tables; create_tables()'"
    echo "4. Access http://localhost:8000/docs"
    exit 0
else
    echo -e "${RED}✗ Some checks failed!${NC}"
    exit 1
fi
