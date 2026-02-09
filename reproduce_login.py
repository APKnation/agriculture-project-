import requests
import json
import random
import string

BASE_URL = "https://agriculture-project-9-nvhd.onrender.com/api"

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def test_login_flow():
    username = f"testuser_{generate_random_string()}"
    password = "testpassword123"
    email = f"{username}@example.com"
    
    print(f"Testing with user: {username}")
    
    # 1. Register
    register_url = f"{BASE_URL}/register/"
    register_data = {
        "username": username,
        "password": password,
        "email": email,
        "role": "farmer",
        "region": "North"
    }
    
    print(f"Registering at {register_url}...")
    try:
        response = requests.post(register_url, json=register_data, timeout=60)
        print(f"Register Status: {response.status_code}")
        print(f"Register Response: {response.text}")
        
        if response.status_code != 201:
            print("Registration failed, aborting.")
            return

    except Exception as e:
        print(f"Registration request failed: {e}")
        return

    # 2. Login
    login_url = f"{BASE_URL}/login/"
    login_data = {
        "username": username,
        "password": password
    }
    
    print(f"Logging in at {login_url}...")
    try:
        response = requests.post(login_url, json=login_data, timeout=60)
        print(f"Login Status: {response.status_code}")
        print(f"Login Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if 'token' in data:
                print("Login SUCCESS! Token received.")
            else:
                print("Login FAILED! No token in response.")
        else:
            print("Login FAILED! Status code not 200.")
            
    except Exception as e:
        print(f"Login request failed: {e}")

def check_health():
    # Check root health endpoint
    root_url = BASE_URL.replace("/api", "")
    health_url = f"{root_url}/health/"
    print(f"Checking health at {health_url}...")
    try:
        response = requests.get(health_url, timeout=60)
        print(f"Health Check Status: {response.status_code}")
        print(f"Health Check Response: {response.text}")
        if response.status_code == 200:
            print("Server is UP.")
            return True
        else:
            print("Server returned unexpected status.")
            return False
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

if __name__ == "__main__":
    if check_health():
        test_login_flow()
    else:
        print("Server is down or unreachable. Skipping login test.")
