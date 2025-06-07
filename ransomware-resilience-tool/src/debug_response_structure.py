#!/usr/bin/env python3
"""
Debug the actual response structure from questionnaire.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, '/workspaces/Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool/src')

def test_questionnaire_structure():
    """Test the actual questionnaire response structure."""
    
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
            print(f"  Adding response for question: {question_id}")
            
            # Simulate a good response (value 3)
            questionnaire.responses[stage_key][question_id] = {
                'value': 3,
                'text': 'Simulated good response',
                'weight': question['weight'],
                'mitre_technique': question['mitre_technique']
            }
    
    print(f"\nFinal response structure:")
    for stage, responses in questionnaire.responses.items():
        print(f"  {stage}: {len(responses)} responses")
        for q_id, response in responses.items():
            print(f"    {q_id}: value={response['value']}, weight={response['weight']}")
    
    print(f"\nTotal responses across all stages: {sum(len(responses) for responses in questionnaire.responses.values())}")
    
    # Test scoring with this structure
    print("\n=== Testing scoring with simulated responses ===")
    try:
        scoring = Scoring(questionnaire.responses)
        overall_score = scoring.calculate_overall_score()
        stage_scores = scoring.calculate_stage_scores()
        
        print(f"Overall score: {overall_score}")
        print(f"Stage scores: {stage_scores}")
        
        # Generate full report
        score_report = scoring.generate_score_report()
        print(f"Score report overall percentage: {score_report.get('overall_percentage', 'NOT FOUND')}")
        
    except Exception as e:
        print(f"Error in scoring: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_questionnaire_structure()
