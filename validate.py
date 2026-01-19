"""
EcoCampus Backend Validation Script
Validates the project setup and identifies any issues
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print("✓ Python version OK:", f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print("✗ Python version too old. Required: 3.11+, Found: Python {version.major}.{version.minor}")
        return False

def check_project_structure():
    """Check project directory structure"""
    required_dirs = [
        "app",
        "app/api",
        "app/api/v1",
        "app/api/v1/endpoints",
        "app/core",
        "app/models",
        "app/schemas",
        "app/services",
        "app/utils",
        "tests",
    ]
    
    required_files = [
        "app/__init__.py",
        "app/main.py",
        "app/core/__init__.py",
        "app/core/config.py",
        "app/core/database.py",
        "app/core/security.py",
        "app/models/__init__.py",
        "app/models/user.py",
        "app/models/campus.py",
        "app/models/carbon.py",
        "app/schemas/__init__.py",
        "app/schemas/user.py",
        "app/schemas/campus.py",
        "app/schemas/carbon.py",
        "app/services/__init__.py",
        "app/services/carbon_calculator.py",
        "app/services/data_service.py",
        "app/services/iot_service.py",
        "app/utils/__init__.py",
        "app/utils/constants.py",
        "app/utils/helpers.py",
        "requirements.txt",
        ".env",
        "docker-compose.yml",
        "dockerfile",
    ]
    
    print("\nChecking directory structure...")
    all_ok = True
    
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"  ✓ {directory}/")
        else:
            print(f"  ✗ {directory}/ - MISSING")
            all_ok = False
    
    print("\nChecking required files...")
    for file in required_files:
        if os.path.isfile(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            all_ok = False
    
    return all_ok

def check_dependencies():
    """Check if key dependencies are installed"""
    print("\nChecking dependencies...")
    
    dependencies = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("sqlalchemy", "SQLAlchemy"),
        ("pydantic", "Pydantic"),
        ("jose", "Python-Jose"),
        ("passlib", "Passlib"),
        ("paho", "Paho MQTT"),
    ]
    
    all_ok = True
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT INSTALLED")
            all_ok = False
    
    return all_ok

def check_imports():
    """Check if core modules can be imported"""
    print("\nChecking imports...")
    
    try:
        from backend.core.config import settings
        print("  ✓ Config module")
    except Exception as e:
        print(f"  ✗ Config module: {e}")
        return False
    
    try:
        from backend.core.database import get_db
        print("  ✓ Database module")
    except Exception as e:
        print(f"  ✗ Database module: {e}")
        return False
    
    try:
        from backend.core.security import create_access_token
        print("  ✓ Security module")
    except Exception as e:
        print(f"  ✗ Security module: {e}")
        return False
    
    try:
        from backend.services.carbon_calculator import CarbonCalculator
        print("  ✓ Carbon Calculator")
    except Exception as e:
        print(f"  ✗ Carbon Calculator: {e}")
        return False
    
    return True

def check_env_file():
    """Check .env file exists and has required variables"""
    print("\nChecking .env file...")
    
    if not os.path.isfile(".env"):
        print("  ✗ .env file not found")
        return False
    
    required_vars = [
        "APP_NAME",
        "DEBUG",
        "SECRET_KEY",
        "DATABASE_URL",
    ]
    
    with open(".env") as f:
        env_content = f.read()
    
    all_ok = True
    for var in required_vars:
        if var in env_content:
            print(f"  ✓ {var}")
        else:
            print(f"  ✗ {var} - Missing in .env")
            all_ok = False
    
    return all_ok

def check_syntax():
    """Check Python syntax of key files"""
    print("\nChecking Python syntax...")
    
    import py_compile
    
    key_files = [
        "app/main.py",
        "app/core/config.py",
        "app/core/database.py",
        "app/api/v1/api.py",
        "app/services/carbon_calculator.py",
    ]
    
    all_ok = True
    for file in key_files:
        try:
            py_compile.compile(file, doraise=True)
            print(f"  ✓ {file}")
        except py_compile.PyCompileError as e:
            print(f"  ✗ {file}: {e}")
            all_ok = False
    
    return all_ok

def print_summary(results):
    """Print validation summary"""
    print("\n" + "="*50)
    print("VALIDATION SUMMARY")
    print("="*50)
    
    all_passed = all(results.values())
    
    for check, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{check}: {status}")
    
    print("="*50)
    
    if all_passed:
        print("\n✓ All checks passed! Your backend is ready to run.")
        print("\nNext steps:")
        print("1. Update .env with your configuration")
        print("2. Start Docker: docker-compose up -d")
        print("3. Create admin user")
        print("4. Access API: http://localhost:8000/docs")
        return 0
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        print("\nFor help, see README.md or CONFIG_GUIDE.md")
        return 1

def main():
    """Run all validation checks"""
    print("="*50)
    print("EcoCampus Backend Validation")
    print("="*50)
    
    results = {
        "Python Version": check_python_version(),
        "Project Structure": check_project_structure(),
        "Dependencies": check_dependencies(),
        "Python Syntax": check_syntax(),
        ".env File": check_env_file(),
        "Imports": check_imports(),
    }
    
    exit_code = print_summary(results)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
