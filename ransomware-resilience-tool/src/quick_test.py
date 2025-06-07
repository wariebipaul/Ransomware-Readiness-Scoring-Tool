#!/usr/bin/env python3
"""
Quick automated test to verify scoring works with fixed interface.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, '/workspaces/Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool/src')

def quick_test():
    """Quick test of the full scoring pipeline."""
    
    from assessment.questionnaire import Questionnaire
    from assessment.scoring import Scoring
    from ui.interface import RansomwareResilienceInterface
    from data.questions import QUESTIONS
    
    # Create responses
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
    
    print("Created test responses")
    
    # Test scoring
    scoring = Scoring(responses)
    score_report = scoring.generate_score_report()
    
    print("Generated score report")
    
    # Test interface display (without clearing screen)
    interface = RansomwareResilienceInterface()
    
    # Override clear_screen to not clear
    interface.clear_screen = lambda: None
    
    print("\n=== Testing Results Display ===")
    interface.display_assessment_results(score_report)
    
    print("\n=== Test Complete ===")
    print(f"Overall score: {score_report['overall_assessment']['percentage_score']}%")

if __name__ == "__main__":
    quick_test()
