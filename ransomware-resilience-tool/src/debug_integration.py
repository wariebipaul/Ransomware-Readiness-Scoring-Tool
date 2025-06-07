#!/usr/bin/env python3
"""
Debug Integration Issues

This script debugs the integration between questionnaire, scoring, and recommendations
to identify why the main application shows 0.0% score.
"""

import sys
sys.path.append('/workspaces/Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool/src')

from data.questions import QUESTIONS
from assessment.questionnaire import Questionnaire
from assessment.scoring import Scoring
from assessment.recommendations import Recommendations
from utils.validation import InputValidator


def debug_data_structures():
    """Debug the data structures and their flow."""
    print("=== DEBUGGING DATA STRUCTURES ===")
    
    # 1. Check questionnaire structure
    questionnaire = Questionnaire()
    print(f"1. Questionnaire questions structure:")
    for stage, stage_data in questionnaire.questions.items():
        print(f"   Stage: {stage}")
        print(f"   Questions count: {len(stage_data['questions'])}")
        if stage_data['questions']:
            print(f"   First question structure: {list(stage_data['questions'][0].keys())}")
    print()
    
    # 2. Create sample responses in the format questionnaire produces
    print("2. Creating sample responses...")
    sample_responses = {
        'pre_infection': {
            'backup_strategy': {
                'value': 3,
                'text': 'Daily automated backups with cloud storage',
                'weight': 10,
                'mitre_technique': 'T1490'
            },
            'network_segmentation': {
                'value': 2,
                'text': 'Basic network segmentation implemented',
                'weight': 8,
                'mitre_technique': 'T1210'
            }
        },
        'active_infection': {
            'incident_response': {
                'value': 4,
                'text': 'Comprehensive incident response plan',
                'weight': 10,
                'mitre_technique': 'T1486'
            },
            'user_training': {
                'value': 1,
                'text': 'Minimal security awareness training',
                'weight': 7,
                'mitre_technique': 'T1566'
            }
        },
        'post_infection': {
            'recovery_plan': {
                'value': 3,
                'text': 'Documented recovery procedures',
                'weight': 9,
                'mitre_technique': 'T1490'
            }
        }
    }
    
    print(f"Sample responses structure: {list(sample_responses.keys())}")
    for stage, responses in sample_responses.items():
        print(f"   {stage}: {list(responses.keys())}")
    print()
    
    # 3. Test scoring with sample responses
    print("3. Testing scoring with sample responses...")
    scoring = Scoring(sample_responses)
    try:
        score_report = scoring.calculate_score()
        print(f"Score report: {score_report}")
    except Exception as e:
        print(f"Error in scoring: {e}")
        import traceback
        traceback.print_exc()
    print()
    
    # 4. Test the full scoring report
    print("4. Testing full scoring report...")
    try:
        full_report = scoring.generate_score_report()
        print(f"Full report keys: {list(full_report.keys())}")
        if 'overall_score' in full_report:
            print(f"Overall score: {full_report['overall_score']}")
    except Exception as e:
        print(f"Error in full report: {e}")
        import traceback
        traceback.print_exc()
    print()


def debug_questionnaire_flow():
    """Debug the questionnaire response collection flow."""
    print("=== DEBUGGING QUESTIONNAIRE FLOW ===")
    
    questionnaire = Questionnaire()
    
    # Simulate the questionnaire flow manually
    print("1. Simulating questionnaire responses...")
    
    # Manually populate responses in the expected format
    questionnaire.responses = {
        'pre_infection': {
            'backup_strategy': {
                'value': 3,
                'text': 'Daily automated backups with cloud storage',
                'weight': 10,
                'mitre_technique': 'T1490'
            }
        },
        'active_infection': {
            'incident_response': {
                'value': 4,
                'text': 'Comprehensive incident response plan',
                'weight': 10,
                'mitre_technique': 'T1486'
            }
        },
        'post_infection': {
            'recovery_plan': {
                'value': 3,
                'text': 'Documented recovery procedures',
                'weight': 9,
                'mitre_technique': 'T1490'
            }
        }
    }
    
    print(f"Questionnaire responses: {questionnaire.responses}")
    print()
    
    # Test validation
    print("2. Testing response validation...")
    is_valid, message = questionnaire.validate_responses()
    print(f"Validation result: {is_valid}, Message: {message}")
    print()
    
    # Test scoring with questionnaire responses
    print("3. Testing scoring with questionnaire responses...")
    scoring = Scoring(questionnaire.responses)
    try:
        score_report = scoring.calculate_score()
        print(f"Score from questionnaire responses: {score_report}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    print()


def debug_main_app_flow():
    """Debug the main application flow."""
    print("=== DEBUGGING MAIN APP FLOW ===")
    
    from main import RansomwareResilienceApp
    
    app = RansomwareResilienceApp()
    
    # Check the questionnaire structure
    print("1. Main app questionnaire structure:")
    print(f"   Questionnaire type: {type(app.questionnaire)}")
    print(f"   Questions available: {list(app.questionnaire.questions.keys())}")
    print()
    
    # Check if responses are properly set
    print("2. Current responses in main app:")
    print(f"   Responses: {app.questionnaire.responses}")
    print()
    
    # Manually set responses and test
    print("3. Manually setting responses and testing...")
    app.questionnaire.responses = {
        'pre_infection': {
            'backup_strategy': {
                'value': 3,
                'text': 'Daily automated backups',
                'weight': 10,
                'mitre_technique': 'T1490'
            }
        },
        'active_infection': {
            'incident_response': {
                'value': 4,
                'text': 'Comprehensive incident response plan',
                'weight': 10,
                'mitre_technique': 'T1486'
            }
        },
        'post_infection': {
            'recovery_plan': {
                'value': 3,
                'text': 'Documented recovery procedures',
                'weight': 9,
                'mitre_technique': 'T1490'
            }
        }
    }
    
    # Test scoring
    try:
        scoring = Scoring(app.questionnaire.responses)
        score_report = scoring.calculate_score()
        print(f"Score in main app context: {score_report}")
        
        full_report = scoring.generate_score_report()
        print(f"Full report overall score: {full_report.get('overall_score', 'N/A')}")
    except Exception as e:
        print(f"Error in main app scoring: {e}")
        import traceback
        traceback.print_exc()
    print()


if __name__ == "__main__":
    debug_data_structures()
    debug_questionnaire_flow()
    debug_main_app_flow()
