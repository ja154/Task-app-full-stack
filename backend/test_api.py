"""
API Testing Script for Task Manager
Run this after starting the Flask server to test all endpoints
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:5000"

def print_response(title, response):
    """Helper to print formatted responses"""
    print(f"\n{'='*60}")
    print(f"TEST: {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")

def test_api():
    """Run comprehensive API tests"""
    
    print("\n" + "🚀 STARTING API TESTS ".center(60, "="))
    
    # Test 1: Register User
    print("\n[1/10] Testing User Registration...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    print_response("User Registration", response)
    
    if response.status_code == 201:
        token = response.json().get("access_token")
        print(f"✅ Registration successful! Token: {token[:20]}...")
    else:
        print("❌ Registration failed!")
        # Try login instead (user might already exist)
        print("\n[1b] Trying to login instead...")
        login_data = {
            "username": "testuser",
            "password": "TestPass123"
        }
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        print_response("User Login (Fallback)", response)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"✅ Login successful! Token: {token[:20]}...")
        else:
            print("❌ Both registration and login failed! Exiting...")
            return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 2: Get Current User
    print("\n[2/10] Testing Get Current User...")
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print_response("Get Current User", response)
    
    # Test 3: Create Task
    print("\n[3/10] Testing Create Task...")
    task_data = {
        "title": "Complete API Testing",
        "description": "Test all endpoints thoroughly",
        "priority": "high",
        "due_date": (datetime.now() + timedelta(days=7)).isoformat()
    }
    response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers)
    print_response("Create Task", response)
    
    if response.status_code == 201:
        task_id = response.json().get("task", {}).get("id")
        print(f"✅ Task created with ID: {task_id}")
    else:
        print("❌ Task creation failed!")
        return
    
    # Test 4: Create Multiple Tasks
    print("\n[4/10] Testing Create Multiple Tasks...")
    tasks_to_create = [
        {"title": "Low Priority Task", "priority": "low"},
        {"title": "Medium Priority Task", "priority": "medium"},
        {"title": "Another High Priority", "priority": "high"},
    ]
    
    created_ids = [task_id]
    for task in tasks_to_create:
        response = requests.post(f"{BASE_URL}/tasks", json=task, headers=headers)
        if response.status_code == 201:
            created_ids.append(response.json().get("task", {}).get("id"))
            print(f"✅ Created: {task['title']}")
    
    # Test 5: Get All Tasks
    print("\n[5/10] Testing Get All Tasks...")
    response = requests.get(f"{BASE_URL}/tasks", headers=headers)
    print_response("Get All Tasks", response)
    
    # Test 6: Get Specific Task
    print("\n[6/10] Testing Get Specific Task...")
    response = requests.get(f"{BASE_URL}/tasks/{task_id}", headers=headers)
    print_response(f"Get Task {task_id}", response)
    
    # Test 7: Update Task
    print("\n[7/10] Testing Update Task...")
    update_data = {
        "title": "Updated: Complete API Testing",
        "description": "Testing is going great!",
        "priority": "medium"
    }
    response = requests.patch(f"{BASE_URL}/tasks/{task_id}", json=update_data, headers=headers)
    print_response("Update Task", response)
    
    # Test 8: Toggle Task Completion
    print("\n[8/10] Testing Toggle Task Completion...")
    response = requests.patch(f"{BASE_URL}/tasks/{task_id}/toggle", headers=headers)
    print_response("Toggle Task Completion", response)
    
    # Test 9: Get Task Statistics
    print("\n[9/10] Testing Get Task Statistics...")
    response = requests.get(f"{BASE_URL}/tasks/stats", headers=headers)
    print_response("Get Task Statistics", response)
    
    # Test 10: Delete Task
    print("\n[10/10] Testing Delete Task...")
    if len(created_ids) > 1:
        delete_id = created_ids[1]
        response = requests.delete(f"{BASE_URL}/tasks/{delete_id}", headers=headers)
        print_response(f"Delete Task {delete_id}", response)
    
    # Test 11: Test Filters
    print("\n[BONUS] Testing Task Filters...")
    response = requests.get(f"{BASE_URL}/tasks?completed=false", headers=headers)
    print_response("Get Pending Tasks", response)
    
    response = requests.get(f"{BASE_URL}/tasks?completed=true", headers=headers)
    print_response("Get Completed Tasks", response)
    
    response = requests.get(f"{BASE_URL}/tasks?priority=high", headers=headers)
    print_response("Get High Priority Tasks", response)
    
    # Test 12: Test Validation Errors
    print("\n[BONUS] Testing Validation Errors...")
    
    # Test empty title
    response = requests.post(f"{BASE_URL}/tasks", json={"title": ""}, headers=headers)
    print_response("Empty Title (should fail)", response)
    
    # Test invalid priority
    response = requests.post(
        f"{BASE_URL}/tasks", 
        json={"title": "Test", "priority": "invalid"}, 
        headers=headers
    )
    print_response("Invalid Priority (should fail)", response)
    
    # Test without authentication
    print("\n[BONUS] Testing Without Authentication...")
    response = requests.get(f"{BASE_URL}/tasks")
    print_response("Get Tasks Without Token (should fail)", response)
    
    print("\n" + "✅ ALL TESTS COMPLETED! ".center(60, "="))
    print("\nCheck the results above to verify all endpoints are working correctly.")
    print(f"\nYour JWT Token (save for manual testing):\n{token}\n")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to Flask server!")
        print("Make sure the Flask server is running on http://127.0.0.1:5000")
        print("\nStart it with: python main.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        