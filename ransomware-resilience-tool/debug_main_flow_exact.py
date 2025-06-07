#!/usr/bin/env python3
"""
Debug script to test the exact flow from main.py with real questionnaire responses
"""

import sys
import os
print("🔍 Starting main flow debug...")
sys.path.append('src')

print("🔍 Importing questionnaire...")
from assessment.questionnaire import Questionnaire
print("🔍 Importing scoring...")
from assessment.scoring import Scoring

def test_main_flow():
    """Test the exact flow that main.py uses"""
    print("=== MAIN FLOW DEBUG ===\n")
    
    # Step 1: Initialize questionnaire (same as main.py)
    print("1. Initializing questionnaire...")
    questionnaire = Questionnaire()
    print(f"✅ Questionnaire initialized with {len(questionnaire.questions)} stages")
    
    # Step 2: Simulate automated responses (instead of user input)
    print("\n2. Simulating questionnaire responses...")
    
    # Create responses in the exact format that questionnaire produces
    questionnaire.responses = {
        'pre_infection': {},
        'active_infection': {},
        'post_infection': {}
    }
    
    # Simulate responses for pre_infection stage
    for question in questionnaire.questions['pre_infection']['questions']:
        questionnaire.responses['pre_infection'][question['id']] = {
            'value': 3,  # Good response
            'text': question['options'][3]['text'],  # Get the text for value 3
            'weight': question['weight'],
            'mitre_technique': question['mitre_technique']
        }
    
    # Simulate responses for active_infection stage
    for question in questionnaire.questions['active_infection']['questions']:
        questionnaire.responses['active_infection'][question['id']] = {
            'value': 2,  # Moderate response
            'text': question['options'][2]['text'],  # Get the text for value 2
            'weight': question['weight'],
            'mitre_technique': question['mitre_technique']
        }
    
    # Simulate responses for post_infection stage
    for question in questionnaire.questions['post_infection']['questions']:
        questionnaire.responses['post_infection'][question['id']] = {
            'value': 1,  # Poor response
            'text': question['options'][1]['text'],  # Get the text for value 1
            'weight': question['weight'],
            'mitre_technique': question['mitre_technique']
        }
    
    # Verify responses structure
    print("   Response structure verification:")
    for stage, responses in questionnaire.responses.items():
        print(f"     {stage}: {len(responses)} responses")
        for q_id, response in responses.items():
            print(f"       {q_id}: value={response['value']}, weight={response['weight']}")
    
    # Step 3: Validate responses (same as main.py)
    print("\n3. Validating responses...")
    is_valid, message = questionnaire.validate_responses()
    print(f"   Validation result: {is_valid} - {message}")
    
    if not is_valid:
        print("❌ Validation failed!")
        return
    
    # Step 4: Extract responses (same as main.py)
    print("\n4. Extracting responses...")
    responses = questionnaire.responses
    print(f"   Extracted responses type: {type(responses)}")
    print(f"   Stages in responses: {list(responses.keys())}")
    
    # Step 5: Initialize scoring (same as main.py)
    print("\n5. Initializing scoring engine...")
    try:
        scoring_engine = Scoring(responses=responses)
        print("✅ Scoring engine initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize scoring engine: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 6: Generate score report (same as main.py)
    print("\n6. Generating score report...")
    try:
        results = scoring_engine.generate_score_report()
        print(f"   Score report type: {type(results)}")
        
        if results and 'overall_assessment' in results:
            overall = results['overall_assessment']
            print(f"   Overall percentage: {overall.get('percentage_score', 'MISSING')}")
            print(f"   Readiness level: {overall.get('readiness_level', 'MISSING')}")
            print(f"   Total score: {overall.get('total_score', 'MISSING')} / {overall.get('max_possible_score', 'MISSING')}")
            
            if overall.get('percentage_score', 0) == 0.0:
                print("❌ PROBLEM FOUND: Score is 0.0%!")
                
                # Debug the internal scoring state
                print("\n   DEBUGGING INTERNAL STATE:")
                print(f"     scoring_engine.responses keys: {list(scoring_engine.responses.keys()) if scoring_engine.responses else 'None'}")
                print(f"     scoring_engine.total_score: {scoring_engine.total_score}")
                print(f"     scoring_engine.max_possible_score: {scoring_engine.max_possible_score}")
                print(f"     scoring_engine.percentage_score: {scoring_engine.percentage_score}")
                
                # Try calling calculate_score directly
                print("\n   TESTING calculate_score() directly:")
                direct_result = scoring_engine.calculate_score()
                print(f"     Direct result: {direct_result}")
                
            else:
                print("✅ Score calculation successful!")
        else:
            print("❌ Invalid score report structure")
            print(f"   Report keys: {list(results.keys()) if results else 'None'}")
            
    except Exception as e:
        print(f"❌ Failed to generate score report: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == "__main__":
    test_main_flow()
