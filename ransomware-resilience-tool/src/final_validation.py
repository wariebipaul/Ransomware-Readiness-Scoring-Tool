#!/usr/bin/env python3
"""
Final validation: Create a simple script that proves the application is working.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, '/workspaces/Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool/src')

def validate_app_components():
    """Validate each component works individually."""
    
    print("=== FINAL VALIDATION OF APPLICATION COMPONENTS ===\n")
    
    # Test 1: Scoring Engine
    print("1. Testing Scoring Engine...")
    try:
        from assessment.scoring import Scoring
        from data.questions import QUESTIONS
        
        # Create test responses
        responses = {}
        for stage_key, stage_data in QUESTIONS.items():
            responses[stage_key] = {}
            for question in stage_data['questions']:
                responses[stage_key][question['id']] = {
                    'value': 3, 'text': 'Test', 'weight': question['weight'], 'mitre_technique': question['mitre_technique']
                }
        
        scoring = Scoring(responses)
        report = scoring.generate_score_report()
        score = report['overall_assessment']['percentage_score']
        
        print(f"   ✓ Scoring Engine: {score}% (WORKING)")
        
    except Exception as e:
        print(f"   ✗ Scoring Engine: ERROR - {e}")
        return False
    
    # Test 2: Interface Display
    print("\n2. Testing Interface Display...")
    try:
        from ui.interface import RansomwareResilienceInterface
        
        interface = RansomwareResilienceInterface()
        interface.clear_screen = lambda: None  # Disable clearing
        interface.display_banner = lambda: None  # Disable banner
        
        # Test with the score report from above
        interface.display_assessment_results(report)
        
        print("   ✓ Interface Display: WORKING")
        
    except Exception as e:
        print(f"   ✗ Interface Display: ERROR - {e}")
        return False
    
    # Test 3: Main Application Class
    print("\n3. Testing Main Application Class...")
    try:
        from main import RansomwareResilienceApp
        
        app = RansomwareResilienceApp()
        scores = app.calculate_scores(responses)
        
        if scores and scores.get('overall_assessment', {}).get('percentage_score'):
            percentage = scores['overall_assessment']['percentage_score']
            print(f"   ✓ Main Application: {percentage}% (WORKING)")
        else:
            print("   ✗ Main Application: Score calculation failed")
            return False
            
    except Exception as e:
        print(f"   ✗ Main Application: ERROR - {e}")
        return False
    
    print("\n" + "="*60)
    print("🎉 VALIDATION COMPLETE: ALL COMPONENTS WORKING!")
    print("🎯 Ransomware Resilience Assessment Tool is OPERATIONAL")
    print(f"📊 Sample Assessment Score: {score}%")
    print("="*60)
    
    return True

if __name__ == "__main__":
    validate_app_components()
