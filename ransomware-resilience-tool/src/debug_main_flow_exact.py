#!/usr/bin/env python3
"""
Debug the exact main.py flow to find where the scoring fails.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, '/workspaces/Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool/src')

def test_main_app_flow():
    """Test the exact flow that main.py uses."""
    
    from assessment.questionnaire import Questionnaire
    from assessment.scoring import Scoring
    from utils.validation import InputValidator
    from data.questions import QUESTIONS
    
    print("=== Testing exact main.py flow ===")
    
    # Step 1: Create questionnaire and collect responses (simulate)
    print("Step 1: Collecting responses...")
    questionnaire = Questionnaire()
    
    # Simulate the exact response collection process
    questionnaire.responses = {}
    for stage_key, stage_data in QUESTIONS.items():
        questionnaire.responses[stage_key] = {}
        
        for question in stage_data['questions']:
            question_id = question['id']
            questionnaire.responses[stage_key][question_id] = {
                'value': 3,
                'text': 'Simulated good response',
                'weight': question['weight'],
                'mitre_technique': question['mitre_technique']
            }
    
    responses = questionnaire.responses
    print(f"Responses collected: {len(responses)} stages")
    
    # Step 2: Validate responses (same as main.py)
    print("Step 2: Validating responses...")
    validator = InputValidator()
    
    try:
        # This is the exact validation from main.py
        if not responses or not isinstance(responses, dict):
            raise ValueError("Invalid responses structure")
        
        # Check that we have responses for all expected stages
        expected_stages = ['pre_infection', 'active_infection', 'post_infection']
        for stage in expected_stages:
            if stage not in responses or not responses[stage]:
                raise ValueError(f"Missing or empty responses for stage: {stage}")
        
        print("✓ Validation passed")
        
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return
    
    # Step 3: Create scoring engine (exact same as main.py)
    print("Step 3: Creating scoring engine...")
    try:
        scoring_engine = Scoring(responses=responses)
        print("✓ Scoring engine created")
    except Exception as e:
        print(f"✗ Scoring engine creation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Generate score report (exact same as main.py)
    print("Step 4: Generating score report...")
    try:
        results = scoring_engine.generate_score_report()
        print(f"✓ Score report generated successfully")
        
        if isinstance(results, dict):
            overall_assessment = results.get('overall_assessment', {})
            percentage_score = overall_assessment.get('percentage_score', 'NOT FOUND')
            print(f"Overall percentage score: {percentage_score}")
            
            # Check all keys in the report
            print("Report structure:")
            for key in results.keys():
                print(f"  - {key}")
                
        else:
            print(f"✗ Unexpected results type: {type(results)}")
            
    except Exception as e:
        print(f"✗ Score report generation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n=== Main.py flow test completed successfully ===")

if __name__ == "__main__":
    test_main_app_flow()
