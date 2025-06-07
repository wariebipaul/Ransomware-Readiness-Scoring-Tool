#!/usr/bin/env python3
"""
Focused debug script to test scoring calculation issue
"""
import sys
sys.path.append('src')

def test_scoring_issue():
    print("=== Testing Scoring Issue ===")
    
    try:
        from assessment.scoring import Scoring
        from data.questions import QUESTIONS
        print("✓ Imports successful")
        
        # Create test responses in the format the questionnaire would generate
        test_responses = {
            'pre_infection': {
                'backup_strategy': {'response_index': 2, 'stage': 'pre_infection'},
                'security_awareness': {'response_index': 3, 'stage': 'pre_infection'},
            },
            'active_infection': {
                'incident_response': {'response_index': 2, 'stage': 'active_infection'},
            },
            'post_infection': {
                'recovery_testing': {'response_index': 1, 'stage': 'post_infection'},
            }
        }
        
        print(f"✓ Test responses created: {list(test_responses.keys())}")
        
        # Test scoring
        scoring = Scoring(responses=test_responses)
        print("✓ Scoring object created")
        
        # Try to calculate score
        print("Calling calculate_score()...")
        result = scoring.calculate_score()
        print(f"Calculate score result: {result}")
        
        print(f"Total score: {scoring.total_score}")
        print(f"Percentage: {scoring.percentage_score}")
        print(f"Readiness level: {scoring.readiness_level}")
        
        # Check individual stage scores
        print(f"Stage scores: {scoring.scores}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scoring_issue()
