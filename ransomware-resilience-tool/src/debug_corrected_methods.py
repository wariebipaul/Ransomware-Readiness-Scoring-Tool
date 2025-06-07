#!/usr/bin/env python3
"""
Debug the actual response structure from questionnaire using correct method names.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, '/workspaces/Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool/src')

def test_questionnaire_structure_corrected():
    """Test the actual questionnaire response structure with correct methods."""
    
    from assessment.questionnaire import Questionnaire
    from assessment.scoring import Scoring
    from data.questions import QUESTIONS
    
    print("=== Testing questionnaire response structure ===")
    
    # Create questionnaire instance
    questionnaire = Questionnaire()
    
    # Manually simulate responses (skip user input)
    questionnaire.responses = {}
    
    # Build responses based on actual questions structure
    for stage_key, stage_data in QUESTIONS.items():
        print(f"Processing stage: {stage_key}")
        questionnaire.responses[stage_key] = {}
        
        for question in stage_data['questions']:
            question_id = question['id']
            
            # Simulate a good response (value 3)
            questionnaire.responses[stage_key][question_id] = {
                'value': 3,
                'text': 'Simulated good response',
                'weight': question['weight'],
                'mitre_technique': question['mitre_technique']
            }
    
    print(f"\nTotal responses across all stages: {sum(len(responses) for responses in questionnaire.responses.values())}")
    
    # Test scoring with this structure
    print("\n=== Testing scoring with correct methods ===")
    try:
        scoring = Scoring(questionnaire.responses)
        
        # Check available methods
        print("Available scoring methods:")
        methods = [method for method in dir(scoring) if not method.startswith('_') and callable(getattr(scoring, method))]
        for method in methods:
            print(f"  - {method}")
        
        # Test calculate_score method
        print(f"\nTesting calculate_score()...")
        overall_score = scoring.calculate_score()
        print(f"Overall score: {overall_score}")
        
        # Test generate_score_report method  
        print(f"\nTesting generate_score_report()...")
        score_report = scoring.generate_score_report()
        print(f"Score report type: {type(score_report)}")
        
        if isinstance(score_report, dict):
            print("Score report contents:")
            for key, value in score_report.items():
                print(f"  {key}: {value}")
        
    except Exception as e:
        print(f"Error in scoring: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_questionnaire_structure_corrected()
