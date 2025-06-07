#!/usr/bin/env python3
"""
Debug script to test scoring functionality
"""
import sys
sys.path.append('src')

from assessment.questionnaire import Questionnaire
from assessment.scoring import Scoring

def test_scoring():
    print("=== Testing Scoring System ===")
    
    # Create sample responses structure that matches what the questionnaire produces
    sample_responses = {
        'pre_infection': {
            'backup_strategy': {
                'value': 3,
                'text': 'Daily automated backups',
                'weight': 10,
                'mitre_technique': 'T1490'
            },
            'backup_isolation': {
                'value': 2,
                'text': 'Partially isolated (network segmented)',
                'weight': 9,
                'mitre_technique': 'T1490'
            }
        },
        'active_infection': {
            'monitoring_logging': {
                'value': 2,
                'text': 'Basic logging and monitoring',
                'weight': 9,
                'mitre_technique': 'T1083'
            }
        },
        'post_infection': {
            'recovery_procedures': {
                'value': 2,
                'text': 'Basic recovery procedures',
                'weight': 10,
                'mitre_technique': 'T1490'
            }
        }
    }
    
    print("Sample responses structure:")
    for stage, responses in sample_responses.items():
        print(f"  {stage}: {len(responses)} responses")
    
    # Test scoring
    scoring = Scoring(responses=sample_responses)
    print(f"\nInitial state:")
    print(f"  Total score: {scoring.total_score}")
    print(f"  Percentage: {scoring.percentage_score}%")
    
    # Call calculate_score
    result = scoring.calculate_score()
    print(f"\nAfter calculate_score():")
    print(f"  Total score: {scoring.total_score}")
    print(f"  Max possible: {scoring.max_possible_score}")
    print(f"  Percentage: {scoring.percentage_score}%")
    print(f"  Readiness level: {scoring.readiness_level}")
    
    print(f"\nStage scores:")
    for stage, scores in scoring.scores.items():
        print(f"  {stage}: {scores}")
    
    # Test generate_score_report
    report = scoring.generate_score_report()
    print(f"\nScore report:")
    print(f"  Overall percentage: {report['overall_assessment']['percentage_score']}%")
    print(f"  Readiness level: {report['overall_assessment']['readiness_level']}")

if __name__ == "__main__":
    test_scoring()
