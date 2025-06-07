#!/usr/bin/env python3
"""
Isolated debug script to test scoring calculation with controlled test data
"""

import sys
import os
print("Starting debug script...")
sys.path.append('src')

print("Importing scoring module...")
try:
    from assessment.scoring import Scoring
    print("✅ Successfully imported Scoring")
except Exception as e:
    print(f"❌ Failed to import Scoring: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def create_test_responses():
    """Create test responses that should produce a known score"""
    return {
        'pre_infection': {
            'q1': {
                'value': 3,
                'weight': 1.5,
                'text': 'We have comprehensive endpoint protection',
                'mitre_technique': 'T1566.001'
            },
            'q2': {
                'value': 2,
                'weight': 1.2,
                'text': 'We have some backup procedures',
                'mitre_technique': 'T1490'
            }
        },
        'active_infection': {
            'q3': {
                'value': 4,
                'weight': 2.0,
                'text': 'We have excellent incident response',
                'mitre_technique': 'T1486'
            }
        },
        'post_infection': {
            'q4': {
                'value': 1,
                'weight': 1.0,
                'text': 'We have limited recovery capabilities',
                'mitre_technique': 'T1490'
            }
        }
    }

def manual_calculation(responses):
    """Manually calculate expected score for verification"""
    total_weighted_score = 0
    total_max_weighted_score = 0
    
    for stage_key, stage_responses in responses.items():
        print(f"\n--- {stage_key.upper()} ---")
        stage_total = 0
        stage_max = 0
        
        for question_id, response in stage_responses.items():
            weighted_score = response['value'] * response['weight']
            max_weighted_score = 4 * response['weight']
            percentage = (weighted_score / max_weighted_score) * 100
            
            print(f"{question_id}: value={response['value']}, weight={response['weight']}")
            print(f"  Weighted score: {weighted_score} / {max_weighted_score} ({percentage:.1f}%)")
            
            stage_total += weighted_score
            stage_max += max_weighted_score
            
        stage_percentage = (stage_total / stage_max) * 100 if stage_max > 0 else 0
        print(f"Stage total: {stage_total} / {stage_max} ({stage_percentage:.1f}%)")
        
        total_weighted_score += stage_total
        total_max_weighted_score += stage_max
    
    overall_percentage = (total_weighted_score / total_max_weighted_score) * 100 if total_max_weighted_score > 0 else 0
    print(f"\n=== OVERALL ===")
    print(f"Total: {total_weighted_score} / {total_max_weighted_score} ({overall_percentage:.1f}%)")
    
    return overall_percentage

def test_scoring_engine():
    """Test the scoring engine with controlled data"""
    print("=== SCORING ENGINE DEBUG ===\n")
    
    # Create test responses
    responses = create_test_responses()
    print("Test responses created:")
    print(f"Stages: {list(responses.keys())}")
    for stage, questions in responses.items():
        print(f"  {stage}: {len(questions)} questions")
    
    # Manual calculation
    print("\n1. MANUAL CALCULATION:")
    expected_percentage = manual_calculation(responses)
    
    # Test scoring engine
    print("\n2. SCORING ENGINE TEST:")
    try:
        scoring = Scoring(responses)
        print("Scoring object created successfully")
        
        # Test calculate_score method
        print("\nTesting calculate_score()...")
        score_result = scoring.calculate_score()
        print(f"calculate_score() returned: {type(score_result)}")
        if score_result:
            print(f"  Percentage: {score_result.get('percentage_score', 'MISSING')}")
            print(f"  Level: {score_result.get('readiness_level', 'MISSING')}")
            print(f"  Total: {score_result.get('total_score', 'MISSING')} / {score_result.get('max_possible_score', 'MISSING')}")
        
        # Test generate_score_report method
        print("\nTesting generate_score_report()...")
        report = scoring.generate_score_report()
        print(f"generate_score_report() returned: {type(report)}")
        if report and 'overall_assessment' in report:
            overall = report['overall_assessment']
            print(f"  Percentage: {overall.get('percentage_score', 'MISSING')}")
            print(f"  Level: {overall.get('readiness_level', 'MISSING')}")
            print(f"  Total: {overall.get('total_score', 'MISSING')} / {overall.get('max_possible_score', 'MISSING')}")
        else:
            print(f"  Report structure: {list(report.keys()) if report else 'None'}")
        
        # Compare results
        if score_result and report:
            engine_percentage = score_result.get('percentage_score', 0)
            report_percentage = report.get('overall_assessment', {}).get('percentage_score', 0)
            
            print(f"\n3. COMPARISON:")
            print(f"  Expected (manual): {expected_percentage:.1f}%")
            print(f"  Engine result: {engine_percentage:.1f}%")
            print(f"  Report result: {report_percentage:.1f}%")
            
            if abs(expected_percentage - engine_percentage) < 0.1:
                print("  ✅ Engine calculation matches expected result")
            else:
                print("  ❌ Engine calculation does NOT match expected result")
                
            if abs(engine_percentage - report_percentage) < 0.1:
                print("  ✅ Report matches engine calculation")
            else:
                print("  ❌ Report does NOT match engine calculation")
        
    except Exception as e:
        print(f"ERROR in scoring engine: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scoring_engine()
