#!/usr/bin/env python3
"""
Comprehensive test script for the Agriculture Management System
Tests all major functionality including authentication, CRUD operations, and API endpoints
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8003/api"
FRONTEND_URL = "http://localhost:5173"

# Test credentials
TEST_USERS = {
    "farmer": {"username": "apk", "password": "password123", "role": "farmer"},
    "officer": {"username": "atanas", "password": "password123", "role": "officer"},
    "admin": {"username": "apknation", "password": "password123", "role": "admin"}
}

class AgricultureSystemTester:
    def __init__(self):
        self.session = requests.Session()
        self.tokens = {}
        self.results = []
        
    def log_result(self, test_name, success, message="", data=None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.results.append(result)
        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {message}")
        
    def test_frontend_access(self):
        """Test if frontend is accessible"""
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            self.log_result(
                "Frontend Access", 
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
            return response.status_code == 200
        except Exception as e:
            self.log_result("Frontend Access", False, f"Error: {str(e)}")
            return False
            
    def test_backend_health(self):
        """Test if backend is running"""
        try:
            response = requests.get(f"{BASE_URL}/crops/", timeout=5)
            self.log_result(
                "Backend Health", 
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
            return response.status_code == 200
        except Exception as e:
            self.log_result("Backend Health", False, f"Error: {str(e)}")
            return False
            
    def test_authentication(self):
        """Test authentication for all user types"""
        auth_success = True
        
        for user_type, credentials in TEST_USERS.items():
            try:
                response = requests.post(
                    f"{BASE_URL}/login/",
                    json=credentials,
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "token" in data:
                        self.tokens[user_type] = data["token"]
                        self.log_result(
                            f"Auth - {user_type}",
                            True,
                            f"Login successful for {credentials['username']}"
                        )
                    else:
                        self.log_result(
                            f"Auth - {user_type}",
                            False,
                            "No token in response"
                        )
                        auth_success = False
                else:
                    self.log_result(
                        f"Auth - {user_type}",
                        False,
                        f"Status: {response.status_code}"
                    )
                    auth_success = False
                    
            except Exception as e:
                self.log_result(f"Auth - {user_type}", False, f"Error: {str(e)}")
                auth_success = False
                
        return auth_success
        
    def test_crop_operations(self):
        """Test crop CRUD operations"""
        if "farmer" not in self.tokens:
            self.log_result("Crop Operations", False, "No farmer token available")
            return False
            
        headers = {"Authorization": f"Bearer {self.tokens['farmer']}"}
        crop_id = None
        crop_ops_success = True
        
        # Test crop creation
        try:
            crop_data = {
                "name": "Test Wheat",
                "type": "grains",
                "status": "planted",
                "description": "Test wheat crop for system verification",
                "planting_date": "2024-01-15",
                "expected_harvest_date": "2024-06-15",
                "yield_estimate": 10.5
            }
            
            response = requests.post(
                f"{BASE_URL}/crops/",
                json=crop_data,
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 201:
                crop_data = response.json()
                crop_id = crop_data.get("id")
                self.log_result(
                    "Crop - Create",
                    True,
                    f"Created crop with ID: {crop_id}"
                )
            else:
                self.log_result(
                    "Crop - Create",
                    False,
                    f"Status: {response.status_code}, Response: {response.text}"
                )
                crop_ops_success = False
                
        except Exception as e:
            self.log_result("Crop - Create", False, f"Error: {str(e)}")
            crop_ops_success = False
            
        # Test crop listing
        try:
            response = requests.get(f"{BASE_URL}/crops/", headers=headers, timeout=5)
            self.log_result(
                "Crop - List",
                response.status_code == 200,
                f"Status: {response.status_code}, Crops: {len(response.json())}"
            )
        except Exception as e:
            self.log_result("Crop - List", False, f"Error: {str(e)}")
            crop_ops_success = False
            
        # Test crop update (if we have a crop_id)
        if crop_id:
            try:
                update_data = {"name": "Updated Test Wheat", "status": "growing"}
                response = requests.patch(
                    f"{BASE_URL}/crops/{crop_id}/",
                    json=update_data,
                    headers=headers,
                    timeout=5
                )
                
                self.log_result(
                    "Crop - Update",
                    response.status_code == 200,
                    f"Status: {response.status_code}"
                )
            except Exception as e:
                self.log_result("Crop - Update", False, f"Error: {str(e)}")
                crop_ops_success = False
                
        # Test crop deletion (if we have a crop_id)
        if crop_id:
            try:
                response = requests.delete(
                    f"{BASE_URL}/crops/{crop_id}/",
                    headers=headers,
                    timeout=5
                )
                
                self.log_result(
                    "Crop - Delete",
                    response.status_code == 204,
                    f"Status: {response.status_code}"
                )
            except Exception as e:
                self.log_result("Crop - Delete", False, f"Error: {str(e)}")
                crop_ops_success = False
                
        return crop_ops_success
        
    def test_user_management(self):
        """Test user management endpoints"""
        if "admin" not in self.tokens:
            self.log_result("User Management", False, "No admin token available")
            return False
            
        headers = {"Authorization": f"Bearer {self.tokens['admin']}"}
        user_mgmt_success = True
        
        try:
            response = requests.get(f"{BASE_URL}/users/", headers=headers, timeout=5)
            self.log_result(
                "User - List",
                response.status_code == 200,
                f"Status: {response.status_code}, Users: {len(response.json())}"
            )
        except Exception as e:
            self.log_result("User - List", False, f"Error: {str(e)}")
            user_mgmt_success = False
            
        return user_mgmt_success
        
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🚀 Starting Agriculture Management System Tests")
        print("=" * 60)
        
        # Run all tests
        frontend_ok = self.test_frontend_access()
        backend_ok = self.test_backend_health()
        auth_ok = self.test_authentication()
        crops_ok = self.test_crop_operations()
        users_ok = self.test_user_management()
        
        # Generate summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Overall system status
        all_critical_ok = frontend_ok and backend_ok and auth_ok and crops_ok
        system_status = "🟢 FULLY OPERATIONAL" if all_critical_ok else "🟡 PARTIAL" if backend_ok and auth_ok else "🔴 CRITICAL ISSUES"
        
        print(f"\nSystem Status: {system_status}")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['message']}")
        
        # Save detailed report
        with open("/tmp/agriculture_test_report.json", "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: /tmp/agriculture_test_report.json")
        
        return all_critical_ok

if __name__ == "__main__":
    tester = AgricultureSystemTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)
