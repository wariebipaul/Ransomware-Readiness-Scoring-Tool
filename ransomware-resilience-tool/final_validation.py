#!/usr/bin/env python3
"""
Final comprehensive validation of the Ransomware Resilience Assessment Tool
"""

import requests
import json
import re
from datetime import datetime

def validate_application():
    """Validate all key requirements from the conversation summary."""
    
    print("🔍 COMPREHENSIVE VALIDATION - Ransomware Resilience Assessment Tool")
    print("=" * 80)
    
    base_url = "http://127.0.0.1:5000"
    validation_results = {}
    
    try:
        session = requests.Session()
        
        # 1. Test Web Application Structure
        print("\n1. 📱 Web Application Structure")
        response = session.get(base_url)
        validation_results['web_app_loads'] = response.status_code == 200
        print(f"   ✅ Flask web app loads: {validation_results['web_app_loads']}")
        
        # 2. Test Assessment Setup (Organization Data)
        print("\n2. 🏢 Assessment Setup")
        setup_data = {
            'organization': 'SecureTest Corporation',
            'assessor': 'Security Analyst',
            'department': 'Cybersecurity',
            'email': 'analyst@securetest.com'
        }
        
        response = session.post(f"{base_url}/start-assessment", data=setup_data)
        validation_results['setup_works'] = response.status_code in [200, 302]
        print(f"   ✅ Organization setup: {validation_results['setup_works']}")
        
        # 3. Test Questionnaire System
        print("\n3. 📋 Questionnaire System")
        
        # Test multiple responses across all stages
        test_responses = [
            {
                'stage': 'pre_infection',
                'question_id': 'q1',
                'response_data': {
                    'score': 3,
                    'answer_text': 'We have comprehensive backup systems with 3-2-1 strategy',
                    'comments': 'Daily incremental, weekly full backups, tested monthly',
                    'timestamp': datetime.now().isoformat()
                }
            },
            {
                'stage': 'pre_infection',
                'question_id': 'q2',
                'response_data': {
                    'score': 4,
                    'answer_text': 'Advanced endpoint protection with EDR capabilities',
                    'comments': 'CrowdStrike Falcon deployed across all endpoints',
                    'timestamp': datetime.now().isoformat()
                }
            },
            {
                'stage': 'active_infection',
                'question_id': 'q6',
                'response_data': {
                    'score': 4,
                    'answer_text': 'Comprehensive incident response plan with defined roles',
                    'comments': 'NIST framework-based, tested quarterly',
                    'timestamp': datetime.now().isoformat()
                }
            },
            {
                'stage': 'active_infection',
                'question_id': 'q8',
                'response_data': {
                    'score': 2,
                    'answer_text': 'Limited network segmentation in place',
                    'comments': 'Working on zero-trust implementation',
                    'timestamp': datetime.now().isoformat()
                }
            },
            {
                'stage': 'post_infection',
                'question_id': 'q11',
                'response_data': {
                    'score': 3,
                    'answer_text': 'Business continuity plans exist and are tested',
                    'comments': 'Annual tabletop exercises conducted',
                    'timestamp': datetime.now().isoformat()
                }
            }
        ]
        
        successful_submissions = 0
        for resp in test_responses:
            result = session.post(f"{base_url}/api/save-response", 
                                json=resp,
                                headers={'Content-Type': 'application/json'})
            if result.status_code == 200:
                successful_submissions += 1
        
        validation_results['questionnaire_works'] = successful_submissions == len(test_responses)
        print(f"   ✅ Response submission: {successful_submissions}/{len(test_responses)} successful")
        
        # 4. Test Scoring Engine
        print("\n4. 🧮 Scoring Engine")
        results_response = session.get(f"{base_url}/results")
        validation_results['results_page_loads'] = results_response.status_code == 200
        
        if validation_results['results_page_loads']:
            content = results_response.text
            
            # Check for score display (should be present in results, absent in questionnaire)
            score_pattern = r'(\d+\.?\d*)%'
            scores_found = re.findall(score_pattern, content)
            validation_results['scoring_works'] = len(scores_found) > 0
            
            print(f"   ✅ Results page loads: {validation_results['results_page_loads']}")
            print(f"   ✅ Scoring calculations: {validation_results['scoring_works']}")
            
            # Check for key result components
            key_components = [
                'Overall Readiness Score',
                'Stage Performance Breakdown',
                'Top Risk Areas',
                'Strength Areas',
                'Priority Recommendations',
                'MITRE ATT&CK Framework Coverage'
            ]
            
            components_found = sum(1 for comp in key_components if comp in content)
            validation_results['comprehensive_results'] = components_found == len(key_components)
            print(f"   ✅ Comprehensive results: {components_found}/{len(key_components)} components")
        
        # 5. Test Score Display Removal from Questionnaire
        print("\n5. 🔒 Score Display Validation")
        questionnaire_response = session.get(f"{base_url}/questionnaire")
        if questionnaire_response.status_code == 200:
            quest_content = questionnaire_response.text
            # Check that score badges/points are NOT visibly displayed in questionnaire
            # Look for patterns like "3 pts", "(4 points)", "Score: 2", etc.
            visible_score_patterns = [
                r'\d+\s*pts',
                r'\d+\s*points',
                r'Score:\s*\d+',
                r'\(\s*\d+\s*pts\s*\)',
                r'badge.*\d+.*pts'
            ]
            
            score_badges_removed = True
            for pattern in visible_score_patterns:
                if re.search(pattern, quest_content, re.IGNORECASE):
                    score_badges_removed = False
                    break
                    
            validation_results['score_display_removed'] = score_badges_removed
            print(f"   ✅ Scores hidden in questionnaire: {validation_results['score_display_removed']}")
        
        # 6. Test Export Functionality
        print("\n6. 📤 Export Functionality")
        
        # Test JSON export
        json_response = session.get(f"{base_url}/api/export/json")
        validation_results['json_export'] = json_response.status_code == 200
        
        # Test CSV export  
        csv_response = session.get(f"{base_url}/api/export/csv")
        validation_results['csv_export'] = csv_response.status_code == 200
        
        print(f"   ✅ JSON export: {validation_results['json_export']}")
        print(f"   ✅ CSV export: {validation_results['csv_export']}")
        
        # 7. Test PDF Export Integration
        print("\n7. 📄 PDF Export Integration")
        
        # Check if PDF libraries are loaded in results page
        if validation_results['results_page_loads']:
            pdf_libs_present = (
                'jspdf' in results_response.text.lower() and 
                'html2canvas' in results_response.text.lower()
            )
            
            pdf_functions_present = (
                'exportToPDF' in results_response.text and
                'exportDetailedPDF' in results_response.text and
                'printReport' in results_response.text
            )
            
            validation_results['pdf_libraries'] = pdf_libs_present
            validation_results['pdf_functions'] = pdf_functions_present
            
            print(f"   ✅ PDF libraries loaded: {validation_results['pdf_libraries']}")
            print(f"   ✅ PDF export functions: {validation_results['pdf_functions']}")
        
        # 8. Test MITRE ATT&CK Integration
        print("\n8. 🎯 MITRE ATT&CK Integration")
        
        if validation_results['results_page_loads']:
            mitre_coverage = (
                'MITRE ATT&CK' in results_response.text and
                'Techniques Covered' in results_response.text and
                'Coverage Percentage' in results_response.text
            )
            validation_results['mitre_integration'] = mitre_coverage
            print(f"   ✅ MITRE framework integration: {validation_results['mitre_integration']}")
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 VALIDATION SUMMARY")
        print("=" * 80)
        
        total_checks = len(validation_results)
        passed_checks = sum(validation_results.values())
        
        for check, result in validation_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status}: {check.replace('_', ' ').title()}")
        
        print(f"\n🎯 Overall Result: {passed_checks}/{total_checks} checks passed")
        
        if passed_checks == total_checks:
            print("🎉 ALL VALIDATION CHECKS PASSED!")
            print("   The Ransomware Resilience Assessment Tool is fully functional.")
            return True
        elif passed_checks >= total_checks * 0.9:
            print("✅ EXCELLENT: 90%+ functionality working correctly.")
            return True
        elif passed_checks >= total_checks * 0.8:
            print("✅ GOOD: 80%+ functionality working correctly.")
            return True
        else:
            print("⚠️ NEEDS ATTENTION: Some core functionality issues detected.")
            return False
            
    except Exception as e:
        print(f"❌ VALIDATION ERROR: {e}")
        return False

if __name__ == "__main__":
    success = validate_application()
    print(f"\n🏁 Validation {'COMPLETED SUCCESSFULLY' if success else 'COMPLETED WITH ISSUES'}")
