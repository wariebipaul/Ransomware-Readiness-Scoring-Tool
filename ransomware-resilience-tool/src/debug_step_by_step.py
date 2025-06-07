#!/usr/bin/env python3
"""
Step-by-step debug script to identify scoring calculation issue.
"""

import sys
import os
import traceback

# Add the src directory to the path
sys.path.insert(0, '/workspaces/Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool/src')

def debug_step_by_step():
    """Debug each step of the scoring process."""
    
    print("=== STEP 1: Import modules ===")
    try:
        from assessment.questionnaire import Questionnaire
        from assessment.scoring import Scoring
        from data.questions import QUESTIONS
        print("✓ Imports successful")
    except Exception as e:
        print(f"✗ Import error: {e}")
        traceback.print_exc()
        return
    
    print("\n=== STEP 2: Create sample responses ===")
    try:
        # Create sample responses that match the exact structure from questionnaire
        responses = {}
        
        # Check questions structure
        print(f"Questions structure type: {type(QUESTIONS)}")
        print(f"Questions keys: {list(QUESTIONS.keys()) if isinstance(QUESTIONS, dict) else 'Not a dict'}")
        
        if isinstance(QUESTIONS, dict):
            for stage_key, stage_data in QUESTIONS.items():
                print(f"Stage: {stage_key}")
                responses[stage_key] = {}
                
                if isinstance(stage_data, dict) and 'questions' in stage_data:
                    for q_id, question_data in stage_data['questions'].items():
                        print(f"  Question ID: {q_id}")
                        responses[stage_key][q_id] = 3  # Good score
                        
        print(f"✓ Sample responses created: {responses}")
                        
    except Exception as e:
        print(f"✗ Response creation error: {e}")
        traceback.print_exc()
        return
    
    print("\n=== STEP 3: Validate responses structure ===")
    try:
        total_responses = sum(len(stage_responses) for stage_responses in responses.values())
        print(f"Total responses collected: {total_responses}")
        
        # Check if all required questions are answered
        for stage_key, stage_data in QUESTIONS.items():
            if isinstance(stage_data, dict) and 'questions' in stage_data:
                stage_questions = list(stage_data['questions'].keys())
                stage_responses = list(responses.get(stage_key, {}).keys())
                print(f"Stage {stage_key}: Expected {len(stage_questions)}, Got {len(stage_responses)}")
                
        print("✓ Response structure validated")
        
    except Exception as e:
        print(f"✗ Response validation error: {e}")
        traceback.print_exc()
        return
    
    print("\n=== STEP 4: Create Scoring instance ===")
    try:
        print("Creating Scoring instance...")
        scoring = Scoring(responses)
        print("✓ Scoring instance created successfully")
        
    except Exception as e:
        print(f"✗ Scoring creation error: {e}")
        traceback.print_exc()
        return
    
    print("\n=== STEP 5: Test individual scoring methods ===")
    try:
        print("Testing calculate_overall_score...")
        overall_score = scoring.calculate_overall_score()
        print(f"Overall score: {overall_score}")
        
        print("Testing calculate_stage_scores...")
        stage_scores = scoring.calculate_stage_scores()
        print(f"Stage scores: {stage_scores}")
        
        print("Testing get_readiness_level...")
        readiness_level = scoring.get_readiness_level()
        print(f"Readiness level: {readiness_level}")
        
        print("✓ Individual methods work")
        
    except Exception as e:
        print(f"✗ Individual method error: {e}")
        traceback.print_exc()
        return
    
    print("\n=== STEP 6: Generate score report ===")
    try:
        print("Calling generate_score_report...")
        score_report = scoring.generate_score_report()
        print(f"Score report type: {type(score_report)}")
        print(f"Score report keys: {list(score_report.keys()) if isinstance(score_report, dict) else 'Not a dict'}")
        
        if isinstance(score_report, dict):
            print(f"Overall percentage: {score_report.get('overall_percentage', 'NOT FOUND')}")
            
        print("✓ Score report generated successfully")
        
    except Exception as e:
        print(f"✗ Score report generation error: {e}")
        traceback.print_exc()
        return
    
    print("\n=== STEP 7: Test with empty responses ===")
    try:
        print("Testing with empty responses...")
        empty_scoring = Scoring({})
        empty_score = empty_scoring.calculate_overall_score()
        print(f"Empty responses score: {empty_score}")
        
    except Exception as e:
        print(f"✗ Empty responses error: {e}")
        traceback.print_exc()
    
    print("\n=== DEBUG COMPLETE ===")

if __name__ == "__main__":
    debug_step_by_step()
