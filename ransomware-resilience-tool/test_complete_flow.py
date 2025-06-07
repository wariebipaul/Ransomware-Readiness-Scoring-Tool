#!/usr/bin/env python3
"""
Test the complete questionnaire and scoring flow with simulated responses
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_complete_flow():
    print("=== Testing Complete Assessment Flow ===")
    
    from assessment.questionnaire import Questionnaire
    from assessment.scoring import Scoring
    from data.questions import QUESTIONS
    
    questionnaire = Questionnaire()
    
    # Simulate completing the questionnaire by directly populating responses
    # This bypasses the input() calls and directly creates the expected response structure
    
    simulated_responses = {
        "pre_infection": {},
        "active_infection": {},
        "post_infection": {}
    }
    
    # Fill in responses for each stage using the actual question structure
    for stage_key, stage_data in QUESTIONS.items():
        print(f"Processing stage: {stage_key}")
        
        for question in stage_data['questions']:
            # Simulate choosing option 2 (moderate response) for all questions
            option_index = 1  # 0-based index for option 2
            selected_option = question['options'][option_index]
            
            simulated_responses[stage_key][question['id']] = {
                'value': selected_option['value'],
                'text': selected_option['text'],
                'weight': question['weight'],
                'mitre_technique': question['mitre_technique']
            }
    
    print("✓ Simulated responses created")
    
    # Test scoring with the simulated responses
    scoring = Scoring(responses=simulated_responses)
    
    print("✓ Scoring object created")
    
    # Calculate scores
    scoring.calculate_score()
    
    print(f"✓ Scores calculated:")
    print(f"  Total Score: {scoring.total_score}")
    print(f"  Max Possible: {scoring.max_possible_score}")
    print(f"  Percentage: {scoring.percentage_score}%")
    print(f"  Readiness Level: {scoring.readiness_level}")
    
    # Generate full report
    report = scoring.generate_score_report()
    print(f"✓ Report generated with keys: {list(report.keys())}")
    
    return report

if __name__ == "__main__":
    test_complete_flow()
