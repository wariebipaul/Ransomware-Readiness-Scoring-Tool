#!/usr/bin/env python3
"""
Final comprehensive test of the complete application flow.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, '/workspaces/Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool/src')

def test_complete_flow():
    """Test the complete application flow."""
    
    from main import RansomwareResilienceApp
    from data.questions import QUESTIONS
    
    print("=== COMPREHENSIVE APPLICATION TEST ===")
    
    # Create application instance
    app = RansomwareResilienceApp()
    
    # Create test responses (simulate complete questionnaire)
    responses = {}
    for stage_key, stage_data in QUESTIONS.items():
        responses[stage_key] = {}
        for question in stage_data['questions']:
            question_id = question['id']
            responses[stage_key][question_id] = {
                'value': 3,  # Good response
                'text': 'Automated test response - good implementation',
                'weight': question['weight'],
                'mitre_technique': question['mitre_technique']
            }
    
    print(f"✓ Created responses for {sum(len(s) for s in responses.values())} questions")
    
    # Test Step 1: Score Calculation
    print("\n1. Testing Score Calculation...")
    scores = app.calculate_scores(responses)
    
    if scores:
        overall = scores.get('overall_assessment', {})
        percentage = overall.get('percentage_score', 'ERROR')
        level = overall.get('readiness_level', 'ERROR')
        print(f"   ✓ Score calculation successful: {percentage}% ({level})")
        
        # Test Step 2: Recommendations Generation
        print("\n2. Testing Recommendations Generation...")
        try:
            recommendations = app.generate_recommendations(responses, scores)
            if recommendations:
                priority_actions = recommendations.get('priority_actions', [])
                exec_summary = recommendations.get('executive_summary', {})
                print(f"   ✓ Recommendations generated successfully")
                print(f"   ✓ Priority actions: {len(priority_actions) if isinstance(priority_actions, list) else 'ERROR'}")
                print(f"   ✓ Executive summary: {'Present' if exec_summary else 'Missing'}")
                
                # Test Step 3: Results Display
                print("\n3. Testing Results Display...")
                try:
                    # Override interface methods to avoid clearing screen
                    app.interface.clear_screen = lambda: print("   [Screen cleared]")
                    app.interface.display_banner = lambda: print("   [Banner displayed]")
                    
                    app.display_results(scores, recommendations)
                    print("   ✓ Results display completed successfully")
                    
                    print("\n=== COMPREHENSIVE TEST PASSED ===")
                    print(f"Final Result: {percentage}% Ransomware Readiness ({level})")
                    
                except Exception as e:
                    print(f"   ✗ Results display failed: {e}")
            else:
                print("   ✗ Recommendations generation returned None")
        except Exception as e:
            print(f"   ✗ Recommendations generation failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("   ✗ Score calculation returned None")
    
    print("\n=== TEST COMPLETE ===")

if __name__ == "__main__":
    test_complete_flow()
