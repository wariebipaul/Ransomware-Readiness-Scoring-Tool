#!/usr/bin/env python3
"""
Debug script to test the complete flow from questionnaire to scoring
"""
import sys
sys.path.append('src')

from assessment.questionnaire import Questionnaire
from assessment.scoring import Scoring

def simulate_responses():
    """Simulate user responses for testing"""
    questionnaire = Questionnaire()
    
    print("=== Simulating Questionnaire Responses ===")
    
    # Simulate responses for each stage
    simulated_responses = {}
    
    for stage_key, stage_data in questionnaire.questions.items():
        print(f"\nStage: {stage_key} - {stage_data['title']}")
        simulated_responses[stage_key] = {}
        
        for question in stage_data['questions']:
            # Simulate choosing option 2 (index 1) for all questions (moderate readiness)
            response_index = 2  # Usually corresponds to "Partially" or "Sometimes"
            simulated_responses[stage_key][question['id']] = {
                'response_index': response_index,
                'stage': stage_key
            }
            print(f"  {question['id']}: Option {response_index} ({question['options'][response_index]})")
    
    return simulated_responses

def test_scoring_with_responses(responses):
    """Test scoring system with simulated responses"""
    print("\n=== Testing Scoring System ===")
    
    scoring = Scoring(responses=responses)
    
    # Calculate scores
    result = scoring.calculate_score()
    print(f"Calculate score result: {result}")
    
    print(f"Total score: {scoring.total_score}")
    print(f"Max possible score: {scoring.max_possible_score}")
    print(f"Percentage score: {scoring.percentage_score}%")
    print(f"Readiness level: {scoring.readiness_level}")
    
    # Test score report generation
    report = scoring.generate_score_report()
    print(f"\nScore report keys: {list(report.keys())}")
    
    return report

def main():
    print("=== Full Flow Debug Test ===")
    
    # Step 1: Simulate responses
    responses = simulate_responses()
    
    print(f"\nGenerated responses structure:")
    for stage, stage_responses in responses.items():
        print(f"  {stage}: {len(stage_responses)} responses")
    
    # Step 2: Test scoring
    report = test_scoring_with_responses(responses)
    
    print("\n=== Final Report ===")
    for key, value in report.items():
        if isinstance(value, dict):
            print(f"{key}: {list(value.keys())}")
        else:
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
