#!/usr/bin/env python3
"""
Test the main application with corrected interface to see if scoring displays properly.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, '/workspaces/Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool/src')

def test_full_application_fixed():
    """Test the complete application flow with fixed interface."""
    
    from main import RansomwareResilienceApp
    from assessment.questionnaire import Questionnaire
    from data.questions import QUESTIONS
    
    print("=== Testing complete application with fixed interface ===")
    
    # Create app instance
    app = RansomwareResilienceApp()
    
    # Simulate responses
    responses = {}
    for stage_key, stage_data in QUESTIONS.items():
        responses[stage_key] = {}
        for question in stage_data['questions']:
            question_id = question['id']
            responses[stage_key][question_id] = {
                'value': 3,
                'text': 'Simulated good response',
                'weight': question['weight'],
                'mitre_technique': question['mitre_technique']
            }
    
    print(f"Created responses for {len(responses)} stages")
    
    # Test scoring calculation
    print("Testing score calculation...")
    scores = app.calculate_scores(responses)
    
    if scores:
        print("✓ Score calculation successful")
        
        # Check the score structure
        overall_assessment = scores.get('overall_assessment', {})
        percentage_score = overall_assessment.get('percentage_score', 'NOT FOUND')
        print(f"Overall percentage score: {percentage_score}")
        
        # Test recommendations generation
        print("Testing recommendations generation...")
        recommendations = app.generate_recommendations(responses, scores)
        
        if recommendations:
            print("✓ Recommendations generation successful")
            
            # Test display results (but capture output)
            print("Testing results display...")
            try:
                app.display_results(scores, recommendations)
                print("✓ Results display completed successfully")
            except Exception as e:
                print(f"✗ Results display failed: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("✗ Recommendations generation failed")
    else:
        print("✗ Score calculation failed")

if __name__ == "__main__":
    test_full_application_fixed()
