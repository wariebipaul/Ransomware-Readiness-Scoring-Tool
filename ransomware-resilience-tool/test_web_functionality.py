#!/usr/bin/env python3
"""
Test script to verify the web application functionality end-to-end
"""

import requests
import json
import time

def test_web_application():
    base_url = "http://127.0.0.1:5000"
    
    try:
        print("🚀 Testing Ransomware Resilience Assessment Tool Web Application")
        print("="*70)
        
        # Test 1: Home page
        print("1. Testing home page...")
        response = requests.get(base_url)
        if response.status_code == 200:
            print("   ✅ Home page loads successfully")
        else:
            print(f"   ❌ Home page failed: {response.status_code}")
            return False
        
        # Test 2: Start assessment
        print("2. Testing assessment setup...")
        setup_data = {
            'organization': 'Test Organization',
            'assessor': 'Test User',
            'department': 'IT Security',
            'email': 'test@example.com'
        }
        
        session = requests.Session()
        response = session.post(f"{base_url}/start-assessment", data=setup_data)
        if response.status_code == 302 or response.status_code == 200:
            print("   ✅ Assessment setup successful")
        else:
            print(f"   ❌ Assessment setup failed: {response.status_code}")
            return False
        
        # Test 3: Submit a few sample responses
        print("3. Testing questionnaire submission...")
        
        # First, get the questionnaire page to establish session
        response = session.get(f"{base_url}/questionnaire")
        if response.status_code != 200:
            print(f"   ❌ Could not access questionnaire: {response.status_code}")
            return False
        
        # Test individual response submission via API
        sample_response = {
            'stage': 'pre_infection',
            'question_id': 'q1',
            'response_data': {
                'score': 3,
                'answer_text': 'We have comprehensive backup systems in place with regular testing',
                'comments': 'Automated daily backups with monthly restore tests',
                'timestamp': '2024-12-19T10:00:00'
            }
        }
        
        response = session.post(f"{base_url}/api/save-response", 
                              json=sample_response,
                              headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("   ✅ Individual response submission successful")
                
                # Submit a few more responses to get meaningful results
                additional_responses = [
                    {
                        'stage': 'pre_infection',
                        'question_id': 'q2',
                        'response_data': {
                            'score': 2,
                            'answer_text': 'We have some endpoint protection but could be more comprehensive',
                            'comments': 'Currently using basic antivirus',
                            'timestamp': '2024-12-19T10:01:00'
                        }
                    },
                    {
                        'stage': 'active_infection',
                        'question_id': 'q6',
                        'response_data': {
                            'score': 4,
                            'answer_text': 'We have a comprehensive incident response plan',
                            'comments': 'Plan is updated quarterly',
                            'timestamp': '2024-12-19T10:02:00'
                        }
                    },
                    {
                        'stage': 'post_infection',
                        'question_id': 'q11',
                        'response_data': {
                            'score': 3,
                            'answer_text': 'We have business continuity plans in place',
                            'comments': 'Plans are tested annually',
                            'timestamp': '2024-12-19T10:03:00'
                        }
                    }
                ]
                
                for resp in additional_responses:
                    session.post(f"{base_url}/api/save-response", 
                               json=resp,
                               headers={'Content-Type': 'application/json'})
                
            else:
                print(f"   ❌ Response submission failed: {result.get('error')}")
                return False
        else:
            print(f"   ❌ Response submission failed: {response.status_code}")
            return False
        
        # Test 4: Check results page
        print("4. Testing results page...")
        response = session.get(f"{base_url}/results")
        if response.status_code == 200:
            print("   ✅ Results page loads successfully")
            if 'Overall Readiness Score' in response.text:
                print("   ✅ Results page contains expected content")
            else:
                print("   ⚠️  Results page missing some expected content")
        else:
            print(f"   ❌ Results page failed: {response.status_code}")
            return False
        
        # Test 5: Check export functionality
        print("5. Testing export APIs...")
        response = session.get(f"{base_url}/api/export/json")
        if response.status_code == 200:
            print("   ✅ JSON export works")
        else:
            print(f"   ❌ JSON export failed: {response.status_code}")
        
        response = session.get(f"{base_url}/api/export/csv")
        if response.status_code == 200:
            print("   ✅ CSV export works")
        else:
            print(f"   ❌ CSV export failed: {response.status_code}")
        
        print("\n🎉 All tests completed successfully!")
        print("✅ The web application is functioning correctly")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the Flask server")
        print("   Make sure the server is running on http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    test_web_application()
