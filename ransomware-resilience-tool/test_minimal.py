#!/usr/bin/env python3
"""
Minimal test to check scoring functionality
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("Testing scoring with minimal data...")
    
    from assessment.scoring import Scoring
    
    # Create minimal test responses
    test_responses = {
        'pre_infection': {
            'test_q1': {'response_index': 2, 'stage': 'pre_infection'}
        }
    }
    
    print(f"Test responses: {test_responses}")
    
    # Create scoring instance
    scoring = Scoring(responses=test_responses)
    print("Scoring instance created")
    
    # Calculate score
    scoring.calculate_score()
    print(f"Score calculated: {scoring.percentage_score}%")
    
    return scoring

if __name__ == "__main__":
    main()
