#!/usr/bin/env python3
"""
Test the main application with simple debug output.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, '/workspaces/Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool/src')

def test_simple():
    """Simple test to check imports and basic functionality."""
    
    print("Starting test...")
    
    try:
        print("Testing imports...")
        from main import RansomwareResilienceApp
        print("✓ Main app imported")
        
        from data.questions import QUESTIONS
        print("✓ Questions imported")
        
        print("Creating app...")
        app = RansomwareResilienceApp()
        print("✓ App created")
        
        # Create simple responses
        print("Creating responses...")
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
        print(f"✓ Created {sum(len(s) for s in responses.values())} responses")
        
        # Test scoring
        print("Testing scoring...")
        scores = app.calculate_scores(responses)
        
        if scores and isinstance(scores, dict):
            overall = scores.get('overall_assessment', {})
            score = overall.get('percentage_score', 'NOT FOUND')
            print(f"✓ Scoring successful: {score}%")
        else:
            print(f"✗ Scoring failed or returned unexpected type: {type(scores)}")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()
