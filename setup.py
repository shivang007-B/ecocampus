#!/usr/bin/env python3
"""
EcoCampus Setup Script
Initializes the application with demo data and dependencies
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command and handle errors"""
    print(f"\n{'='*50}")
    print(f"  {description}")
    print(f"{'='*50}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} failed with code {e.returncode}")
        return False

def main():
    print("\n")
    print("╔" + "="*48 + "╗")
    print("║" + "  EcoCampus - Complete Setup".center(48) + "║")
    print("║" + "  Ready-to-Run Application".center(48) + "║")
    print("╚" + "="*48 + "╝")
    print("\n")
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("ERROR: Python 3.11+ is required")
        return False
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Check if Node.js is available
    try:
        import subprocess
        subprocess.run(['node', '--version'], capture_output=True, check=True)
        print("✓ Node.js detected")
    except:
        print("⚠ WARNING: Node.js not found. Frontend setup will be skipped.")
    
    # Install backend dependencies
    print("\n")
    if not run_command(
        "pip install -r requirements.txt",
        "Installing Backend Dependencies"
    ):
        return False
    
    print("✓ Backend dependencies installed")
    
    # Install frontend dependencies
    try:
        os.chdir("frontend")
        if not run_command("npm install", "Installing Frontend Dependencies"):
            os.chdir("..")
            return False
        os.chdir("..")
        print("✓ Frontend dependencies installed")
    except:
        print("⚠ Frontend setup failed or skipped")
        os.chdir("..")
    
    # Setup database and demo data
    print("\n")
    print("="*50)
    print("  Setting Up Database")
    print("="*50)
    
    try:
        from backend.core.database import create_tables, SessionLocal
        from backend.models.user import User
        from backend.core.security import get_password_hash
        
        print("Creating database tables...")
        create_tables()
        print("✓ Database tables created")
        
        db = SessionLocal()
        try:
            # Check if demo admin already exists
            admin_user = db.query(User).filter(
                User.email == 'admin@ecocampus.com'
            ).first()
            
            if not admin_user:
                print("Creating demo admin user...")
                admin_user = User(
                    email='admin@ecocampus.com',
                    username='admin',
                    full_name='Admin User',
                    hashed_password=get_password_hash('password123'),
                    role='superuser',
                    is_active=True,
                    is_superuser=True
                )
                db.add(admin_user)
                db.commit()
                print("✓ Demo admin user created")
                print("  Email: admin@ecocampus.com")
                print("  Password: password123")
            else:
                print("✓ Demo admin user already exists")
        finally:
            db.close()
    except Exception as e:
        print(f"⚠ Database setup warning: {e}")
    
    # Print summary
    print("\n")
    print("╔" + "="*48 + "╗")
    print("║" + "  ✓ Setup Complete!".center(48) + "║")
    print("╚" + "="*48 + "╝")
    
    print("\n📋 To run the application:\n")
    
    print("1️⃣  Start Backend (in Terminal 1):")
    print("    python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000")
    
    print("\n2️⃣  Start Frontend (in Terminal 2):")
    print("    cd frontend")
    print("    npm run dev")
    
    print("\n3️⃣  Open Browser:")
    print("    → Application: http://localhost:5173")
    print("    → API Docs: http://localhost:8000/docs")
    
    print("\n🔑 Demo Credentials:")
    print("    Email: admin@ecocampus.com")
    print("    Password: password123")
    
    print("\n📖 For more information, see QUICK_START.md\n")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
