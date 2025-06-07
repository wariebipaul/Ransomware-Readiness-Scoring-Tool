#!/usr/bin/env python3
"""
Debug script to test questionnaire response structure
"""
import sys
sys.path.append('src')

from assessment.questionnaire import Questionnaire

def test_questionnaire_structure():
    print("=== Testing Questionnaire Structure ===")
    
    questionnaire = Questionnaire()
    
    print("Question keys:")
    for key, data in questionnaire.questions.items():
        print(f"  {key}: {data['title']}")
        print(f"    {len(data['questions'])} questions")
    
    print("\nResponse structure (initially empty):")
    print(f"  Response keys: {list(questionnaire.responses.keys())}")

if __name__ == "__main__":
    test_questionnaire_structure()
