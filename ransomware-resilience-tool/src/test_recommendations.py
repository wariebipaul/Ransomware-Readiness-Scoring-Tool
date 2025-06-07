#!/usr/bin/env python3
"""
Test the recommendations system.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, '/workspaces/Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool/src')

def test_recommendations():
    """Test the recommendations system with score data."""
    
    from assessment.scoring import Scoring
    from assessment.recommendations import Recommendations
    from data.questions import QUESTIONS
    
    print("=== Testing Recommendations System ===")
    
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
    
    # Test recommendations
    print("\nTesting recommendations generation...")
    recommendations_engine = Recommendations(score_report)
    
    try:
        # Test available methods
        print("Available recommendation methods:")
        methods = [method for method in dir(recommendations_engine) if not method.startswith('_') and callable(getattr(recommendations_engine, method))]
        for method in methods:
            print(f"  - {method}")
        
        # Test priority actions
        print("\nTesting get_prioritized_action_plan()...")
        action_plan = recommendations_engine.get_prioritized_action_plan()
        print(f"Action plan type: {type(action_plan)}")
        if isinstance(action_plan, list):
            print(f"Number of actions: {len(action_plan)}")
            if action_plan:
                print(f"First action: {action_plan[0] if action_plan else 'None'}")
        
        # Test executive summary
        print("\nTesting generate_executive_summary()...")
        exec_summary = recommendations_engine.generate_executive_summary()
        print(f"Executive summary type: {type(exec_summary)}")
        if isinstance(exec_summary, dict):
            print(f"Summary keys: {list(exec_summary.keys())}")
        
        print("\n✓ Recommendations system working correctly")
        
    except Exception as e:
        print(f"✗ Recommendations error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_recommendations()
