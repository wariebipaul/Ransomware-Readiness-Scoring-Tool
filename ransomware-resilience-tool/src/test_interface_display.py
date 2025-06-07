#!/usr/bin/env python3
"""
Test the fixed interface display.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, '/workspaces/Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool/src')

def test_interface_display():
    """Test the interface display with actual score data."""
    
    from assessment.scoring import Scoring
    from ui.interface import RansomwareResilienceInterface
    from data.questions import QUESTIONS
    
    print("=== Testing Interface Display ===")
    
    # Create test responses
    responses = {}
    for stage_key, stage_data in QUESTIONS.items():
        responses[stage_key] = {}
        for question in stage_data['questions']:
            question_id = question['id']
            responses[stage_key][question_id] = {
                'value': 3,
                'text': 'Test response',
                'weight': question['weight'],
                'mitre_technique': question['mitre_technique']
            }
    
    # Generate score report
    scoring = Scoring(responses)
    score_report = scoring.generate_score_report()
    
    print(f"Generated score report with {score_report['overall_assessment']['percentage_score']}% overall score")
    
    # Test interface display
    interface = RansomwareResilienceInterface()
    
    # Override methods that might cause issues
    interface.clear_screen = lambda: print("=== CLEARED SCREEN ===")
    interface.display_banner = lambda: print("=== BANNER ===")
    
    print("\n=== Testing Results Display ===")
    interface.display_assessment_results(score_report)
    
    print("\n=== Interface Test Complete ===")

if __name__ == "__main__":
    test_interface_display()
