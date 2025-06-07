#!/usr/bin/env python3
"""
Debug the scoring calculation issue
"""

print("Starting debug script...")

try:
    import sys
    import os
    print("Imports working...")
    
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    print("Path setup working...")
    
    from assessment.scoring import Scoring
    print("Scoring import working...")
    
    from data.questions import QUESTIONS
    print("Questions import working...")
    
    # Create test data in the format the web app would generate
    test_responses = {
        'pre_infection': {
            'pre_1': {
                'value': 3,
                'weight': 5,
                'text': 'We have regular backups',
                'comments': '',
                'timestamp': '2024-06-07T12:00:00Z',
                'mitre_technique': ''
            }
        }
    }
    
    print("Test data created...")
    print("Testing scoring calculation with converted data format...")
    
    scoring_engine = Scoring(test_responses)
    print("Scoring engine created...")
    
    results = scoring_engine.generate_score_report()
    print("SUCCESS! Score calculation worked.")
    print("Results:", results)
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
