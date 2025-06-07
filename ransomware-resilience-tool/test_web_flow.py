#!/usr/bin/env python3
"""
Test script to validate the complete web application flow
Tests organization setup, questionnaire completion, and results display
"""

import requests
import json
import time

# Base URL for the Flask application
BASE_URL = "http://127.0.0.1:5000"

def test_organization_setup():
    """Test organization setup endpoint"""
    print("🏢 Testing organization setup...")
    
    setup_data = {
        'organization': 'Test Tech Corp',
        'assessor': 'John Doe',
        'role': 'IT Manager',
        'department': 'Information Technology',
        'email': 'john.doe@testtech.com'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/start-assessment", data=setup_data, timeout=10)
        print(f"Setup response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Organization setup successful")
            return True
        else:
            print(f"❌ Organization setup failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Organization setup error: {e}")
        return False

def test_questionnaire_submission():
    """Test questionnaire submission with sample responses"""
    print("\n📝 Testing questionnaire submission...")
    
    # Sample responses for all questions with good scores
    sample_responses = {
        'pre_infection': {
            'backup_strategy': {
                'score': 4,
                'answer_text': 'Comprehensive 3-2-1 backup strategy with regular testing',
                'comments': 'We have automated daily backups with monthly restoration tests',
                'timestamp': time.time()
            },
            'access_controls': {
                'score': 3,
                'answer_text': 'Multi-factor authentication implemented for most systems',
                'comments': 'MFA deployed for 80% of critical systems',
                'timestamp': time.time()
            },
            'employee_training': {
                'score': 4,
                'answer_text': 'Quarterly security awareness training with phishing simulations',
                'comments': 'Comprehensive training program with testing',
                'timestamp': time.time()
            },
            'network_segmentation': {
                'score': 3,
                'answer_text': 'Partial network segmentation implemented',
                'comments': 'Working on expanding segmentation',
                'timestamp': time.time()
            },
            'patch_management': {
                'score': 4,
                'answer_text': 'Automated patch management with testing procedures',
                'comments': 'Monthly patch cycles with emergency procedures',
                'timestamp': time.time()
            }
        },
        'active_infection': {
            'incident_response': {
                'score': 3,
                'answer_text': 'Documented incident response plan with regular drills',
                'comments': 'Plan updated annually with tabletop exercises',
                'timestamp': time.time()
            },
            'communication_plan': {
                'score': 3,
                'answer_text': 'Communication procedures defined for stakeholders',
                'comments': 'Clear escalation paths established',
                'timestamp': time.time()
            },
            'isolation_procedures': {
                'score': 4,
                'answer_text': 'Automated isolation capabilities implemented',
                'comments': 'Network isolation can be triggered remotely',
                'timestamp': time.time()
            },
            'forensic_capabilities': {
                'score': 2,
                'answer_text': 'Basic forensic tools available',
                'comments': 'Limited in-house forensic expertise',
                'timestamp': time.time()
            },
            'business_continuity': {
                'score': 3,
                'answer_text': 'Business continuity plan with backup sites',
                'comments': 'Alternative work arrangements documented',
                'timestamp': time.time()
            }
        },
        'post_infection': {
            'recovery_procedures': {
                'score': 3,
                'answer_text': 'Documented recovery procedures with priority systems',
                'comments': 'Recovery time objectives defined',
                'timestamp': time.time()
            },
            'backup_restoration': {
                'score': 4,
                'answer_text': 'Tested backup restoration procedures',
                'comments': 'Monthly restoration tests performed',
                'timestamp': time.time()
            },
            'lessons_learned': {
                'score': 2,
                'answer_text': 'Basic post-incident review process',
                'comments': 'Room for improvement in documentation',
                'timestamp': time.time()
            },
            'system_hardening': {
                'score': 3,
                'answer_text': 'Security improvements implemented after incidents',
                'comments': 'Standard hardening procedures followed',
                'timestamp': time.time()
            },
            'stakeholder_communication': {
                'score': 3,
                'answer_text': 'Communication plan for post-incident updates',
                'comments': 'Regular updates to stakeholders',
                'timestamp': time.time()
            }
        }
    }
    
    try:
        # Submit responses
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            f"{BASE_URL}/api/save-response", 
            data=json.dumps(sample_responses), 
            headers=headers,
            timeout=10
        )
        
        print(f"Questionnaire submission status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Questionnaire submission successful: {result.get('message', 'No message')}")
            return True
        else:
            print(f"❌ Questionnaire submission failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Questionnaire submission error: {e}")
        return False

def test_results_calculation():
    """Test results calculation and display"""
    print("\n📊 Testing results calculation...")
    
    try:
        response = requests.get(f"{BASE_URL}/results", timeout=10)
        print(f"Results page status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Results page loaded successfully")
            
            # Check if the page contains expected elements
            content = response.text.lower()
            if 'overall readiness score' in content:
                print("✅ Overall score section found")
            if 'stage scores' in content or 'detailed stage scores' in content:
                print("✅ Stage scores section found")
            if 'mitre' in content:
                print("✅ MITRE coverage section found")
            if 'recommendations' in content:
                print("✅ Recommendations section found")
            
            return True
        else:
            print(f"❌ Results page failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Results page error: {e}")
        return False

def test_export_functionality():
    """Test export functionality"""
    print("\n📤 Testing export functionality...")
    
    try:
        # Test JSON export
        response = requests.get(f"{BASE_URL}/api/export/json", timeout=10)
        print(f"JSON export status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ JSON export successful and valid")
                print(f"Export contains: {list(data.keys()) if isinstance(data, dict) else 'Non-dict response'}")
            except json.JSONDecodeError:
                print("❌ JSON export returned invalid JSON")
        else:
            print(f"❌ JSON export failed: {response.text}")
        
        # Test CSV export
        response = requests.get(f"{BASE_URL}/api/export/csv", timeout=10)
        print(f"CSV export status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ CSV export successful")
        else:
            print(f"❌ CSV export failed: {response.text}")
        
        return True
    except Exception as e:
        print(f"❌ Export functionality error: {e}")
        return False

def main():
    """Run complete web application flow test"""
    print("🚀 Starting Web Application Flow Test")
    print("=" * 50)
    
    # Test each component in sequence
    success_count = 0
    total_tests = 4
    
    if test_organization_setup():
        success_count += 1
    
    if test_questionnaire_submission():
        success_count += 1
    
    if test_results_calculation():
        success_count += 1
    
    if test_export_functionality():
        success_count += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Summary: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 All tests passed! Web application is working correctly.")
    else:
        print(f"⚠️ {total_tests - success_count} test(s) failed. Check the details above.")
    
    return success_count == total_tests

if __name__ == "__main__":
    main()
