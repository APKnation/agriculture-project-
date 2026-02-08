#!/usr/bin/env python3
"""
Deployment readiness check for the Agriculture Management System
Ensures all components are properly configured and working
"""

import os
import sys
import subprocess
import requests
import json
from pathlib import Path

class DeploymentChecker:
    def __init__(self):
        self.project_root = Path("/media/apknation/APKnation/PROJECT/VUE/agriculture")
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.issues = []
        self.fixes = []
        
    def log_issue(self, component, issue, severity="medium", fix=None):
        """Log an issue and its fix"""
        self.issues.append({
            "component": component,
            "issue": issue,
            "severity": severity,
            "fix": fix
        })
        if fix:
            self.fixes.append(fix)
            
    def check_backend_dependencies(self):
        """Check if backend dependencies are installed"""
        print("🔍 Checking backend dependencies...")
        
        required_packages = {
            "django": "django",
            "djangorestframework": "rest_framework", 
            "djangorestframework-simplejwt": "rest_framework_simplejwt",
            "django-cors-headers": "corsheaders",
            "django-filter": "django_filters",
            "pillow": "PIL"
        }
        
        missing_packages = []
        for package_name, import_name in required_packages.items():
            try:
                result = subprocess.run([
                    sys.executable, "-c", f"import {import_name}"
                ], capture_output=True, text=True)
                if result.returncode != 0:
                    missing_packages.append(package_name)
            except ImportError:
                missing_packages.append(package_name)
                
        if missing_packages:
            self.log_issue(
                "Backend Dependencies",
                f"Missing packages: {', '.join(missing_packages)}",
                severity="high",
                fix=f"Install with: pip install {' '.join(missing_packages)}"
            )
        else:
            print("✅ All backend dependencies installed")
            
    def check_backend_configuration(self):
        """Check backend configuration"""
        print("🔍 Checking backend configuration...")
        
        # Check if settings.py exists and has correct configuration
        settings_file = self.backend_dir / "backend" / "settings.py"
        if not settings_file.exists():
            self.log_issue("Backend", "settings.py not found", severity="high")
            return
            
        # Check database
        db_file = self.backend_dir / "db.sqlite3"
        if not db_file.exists():
            self.log_issue("Backend", "Database not found", severity="high", 
                          fix="Run: python manage.py migrate")
        else:
            print("✅ Database exists")
            
    def check_backend_server(self):
        """Check if backend server is running"""
        print("🔍 Checking backend server...")
        
        try:
            response = requests.get("http://127.0.0.1:8003/api/crops/", timeout=5)
            if response.status_code == 200:
                print("✅ Backend server is running")
                return True
            else:
                self.log_issue("Backend Server", f"Server returned {response.status_code}", severity="high")
                return False
        except requests.exceptions.RequestException:
            self.log_issue("Backend Server", "Server not accessible", severity="high",
                          fix="Start server: python manage.py runserver 8003")
            return False
            
    def check_frontend_dependencies(self):
        """Check frontend dependencies"""
        print("🔍 Checking frontend dependencies...")
        
        package_json = self.frontend_dir / "package.json"
        node_modules = self.frontend_dir / "node_modules"
        
        if not package_json.exists():
            self.log_issue("Frontend", "package.json not found", severity="high")
            return
            
        if not node_modules.exists():
            self.log_issue("Frontend", "node_modules not found", severity="high",
                          fix="Run: npm install")
        else:
            print("✅ Frontend dependencies installed")
            
    def check_frontend_server(self):
        """Check if frontend server is running"""
        print("🔍 Checking frontend server...")
        
        try:
            response = requests.get("http://localhost:5173/", timeout=5)
            if response.status_code == 200:
                print("✅ Frontend server is running")
                return True
            else:
                self.log_issue("Frontend Server", f"Server returned {response.status_code}", severity="high")
                return False
        except requests.exceptions.RequestException:
            self.log_issue("Frontend Server", "Server not accessible", severity="high",
                          fix="Start server: npm run dev")
            return False
            
    def check_api_endpoints(self):
        """Check critical API endpoints"""
        print("🔍 Checking API endpoints...")
        
        # Get fresh token first
        try:
            login_response = requests.post(
                "http://127.0.0.1:8003/api/login/",
                json={"username": "apk", "password": "password123"},
                timeout=5
            )
            
            if login_response.status_code == 200:
                token = login_response.json().get("token")
                headers = {"Authorization": f"Bearer {token}"}
            else:
                self.log_issue("API Endpoints", "Failed to get fresh token", severity="high")
                return
                
        except Exception as e:
            self.log_issue("API Endpoints", f"Login error: {str(e)}", severity="high")
            return
        
        endpoints = [
            ("/api/login/", "POST", {"username": "apk", "password": "password123"}),
            ("/api/crops/", "GET", None),
            ("/api/users/", "GET", None),
        ]
        
        for endpoint, method, data in endpoints:
            try:
                url = f"http://127.0.0.1:8003{endpoint}"
                if method == "POST":
                    response = requests.post(url, json=data, timeout=5)
                else:
                    response = requests.get(url, headers=headers, timeout=5)
                    
                if response.status_code in [200, 201]:
                    print(f"✅ {endpoint} - {method}")
                else:
                    self.log_issue("API Endpoints", f"{endpoint} returned {response.status_code}", 
                                  severity="medium")
            except Exception as e:
                self.log_issue("API Endpoints", f"{endpoint} error: {str(e)}", severity="medium")
                
    def check_database_integrity(self):
        """Check database integrity"""
        print("🔍 Checking database integrity...")
        
        try:
            # Check if we can access the database
            result = subprocess.run([
                "python3", "manage.py", "check"
            ], cwd=self.backend_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Database integrity check passed")
            else:
                self.log_issue("Database", f"Check failed: {result.stderr}", severity="high")
        except Exception as e:
            self.log_issue("Database", f"Check error: {str(e)}", severity="high")
            
    def check_file_permissions(self):
        """Check file permissions"""
        print("🔍 Checking file permissions...")
        
        # Check media directory
        media_dir = self.backend_dir / "media"
        if media_dir.exists():
            if not os.access(media_dir, os.W_OK):
                self.log_issue("File Permissions", "Media directory not writable", severity="medium")
            else:
                print("✅ Media directory permissions OK")
        else:
            self.log_issue("File Permissions", "Media directory not found", severity="medium",
                          fix="Create media directory: mkdir media")
            
    def generate_deployment_script(self):
        """Generate a deployment script"""
        script_content = """#!/bin/bash
# Agriculture Management System Deployment Script

echo "🚀 Starting Agriculture Management System Deployment..."

# Backend Setup
echo "📦 Setting up backend..."
cd backend

# Install dependencies
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers django-filter pillow

# Database migrations
python manage.py migrate

# Create superuser if needed
python manage.py shell -c "
from market.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Admin user created')
"

# Start backend server
echo "🖥️ Starting backend server..."
python manage.py runserver 8003 &
BACKEND_PID=$!

# Frontend Setup
echo "📦 Setting up frontend..."
cd ../frontend

# Install dependencies
npm install

# Start frontend server
echo "🌐 Starting frontend server..."
npm run dev &
FRONTEND_PID=$!

echo "✅ Deployment complete!"
echo "🔗 Frontend: http://localhost:5173"
echo "🔗 Backend: http://127.0.0.1:8003"
echo "👤 Admin login: admin / admin123"
echo "👤 Test user: apk / password123"

# Wait for user input to stop
echo "Press Ctrl+C to stop servers"
wait $BACKEND_PID $FRONTEND_PID
"""
        
        script_path = self.project_root / "deploy.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
            
        os.chmod(script_path, 0o755)
        print(f"✅ Deployment script created: {script_path}")
        
    def run_checks(self):
        """Run all checks"""
        print("🔍 Starting Deployment Readiness Check")
        print("=" * 50)
        
        self.check_backend_dependencies()
        self.check_backend_configuration()
        self.check_backend_server()
        self.check_frontend_dependencies()
        self.check_frontend_server()
        self.check_api_endpoints()
        self.check_database_integrity()
        self.check_file_permissions()
        
        print("\n" + "=" * 50)
        print("📊 DEPLOYMENT READINESS SUMMARY")
        print("=" * 50)
        
        if not self.issues:
            print("🎉 ALL CHECKS PASSED - System is ready for deployment!")
            return True
        else:
            print(f"❌ Found {len(self.issues)} issues:")
            
            high_issues = [i for i in self.issues if i["severity"] == "high"]
            medium_issues = [i for i in self.issues if i["severity"] == "medium"]
            
            if high_issues:
                print(f"\n🔴 HIGH PRIORITY ({len(high_issues)}):")
                for issue in high_issues:
                    print(f"  • {issue['component']}: {issue['issue']}")
                    if issue['fix']:
                        print(f"    Fix: {issue['fix']}")
                        
            if medium_issues:
                print(f"\n🟡 MEDIUM PRIORITY ({len(medium_issues)}):")
                for issue in medium_issues:
                    print(f"  • {issue['component']}: {issue['issue']}")
                    if issue['fix']:
                        print(f"    Fix: {issue['fix']}")
            
            # Generate fixes script
            if self.fixes:
                print(f"\n🔧 AUTO-FIXES AVAILABLE:")
                for fix in self.fixes:
                    print(f"  • {fix}")
                    
            # Generate deployment script
            self.generate_deployment_script()
            
            return False

if __name__ == "__main__":
    checker = DeploymentChecker()
    success = checker.run_checks()
    sys.exit(0 if success else 1)
