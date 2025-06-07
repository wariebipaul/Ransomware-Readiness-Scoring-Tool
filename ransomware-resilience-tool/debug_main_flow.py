#!/usr/bin/env python3
"""
Debug script to test the exact same flow as the main application
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from assessment.questionnaire import Questionnaire
from assessment.scoring import Scoring
from assessment.recommendations import Recommendations

def debug_main_flow():
    print("=== Debug Main Application Flow ===")
    
    # Step 1: Create questionnaire and simulate responses (like the automated test)
    questionnaire = Questionnaire()
    
    # Simulate the same responses as the automated test (all option 2)
    for stage_key, stage_data in questionnaire.questions.items():
        questionnaire.responses[stage_key] = {}
        for question in stage_data['questions']:
            # Choose option 2 (index 1)
            selected_option = question['options'][1]
            questionnaire.responses[stage_key][question['id']] = {
                'value': selected_option['value'],
                'text': selected_option['text'],
                'weight': question['weight'],
                'mitre_technique': question['mitre_technique']
            }
    
    responses = questionnaire.responses
    print(f"✓ Created responses for {len(responses)} stages")
    for stage, stage_responses in responses.items():
        print(f"  {stage}: {len(stage_responses)} responses")
    
    # Step 2: Validate responses (like main.py does)
    is_valid, validation_message = questionnaire.validate_responses()
    print(f"✓ Validation: {is_valid} - {validation_message}")
    
    if not is_valid:
        print("❌ Validation failed!")
        return
    
    # Step 3: Calculate scores (exactly like main.py)
    try:
        # Validate responses structure before scoring (like main.py)
        if not responses or not isinstance(responses, dict):
            raise ValueError("Invalid responses structure")
        
        # Check that we have responses for all expected stages
        expected_stages = ['pre_infection', 'active_infection', 'post_infection']
        for stage in expected_stages:
            if stage not in responses or not responses[stage]:
                raise ValueError(f"Missing or empty responses for stage: {stage}")
        
        print("✓ Pre-scoring validation passed")
        
        # Initialize scoring engine (like main.py)
        scoring_engine = Scoring(responses=responses)
        print("✓ Scoring engine created")
        
        # Generate score report (like main.py)
        results = scoring_engine.generate_score_report()
        print(f"✓ Score report generated: {type(results)}")
        print(f"Report keys: {list(results.keys()) if isinstance(results, dict) else 'Not a dict'}")
        
        # Print some details
        print(f"Scoring engine state:")
        print(f"  Total score: {scoring_engine.total_score}")
        print(f"  Max possible: {scoring_engine.max_possible_score}")
        print(f"  Percentage: {scoring_engine.percentage_score}%")
        print(f"  Readiness level: {scoring_engine.readiness_level}")
        
        return results
        
    except Exception as e:
        print(f"❌ Scoring failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    debug_main_flow()
