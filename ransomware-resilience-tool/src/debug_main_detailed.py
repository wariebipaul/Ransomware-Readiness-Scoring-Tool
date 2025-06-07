#!/usr/bin/env python3
"""
Debug Main App Integration

This script tests the main app flow to identify integration issues.
"""

import sys
sys.path.append('/workspaces/Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool/src')

from main import RansomwareResilienceApp


def debug_main_app_detailed():
    """Debug the main app in detail."""
    print("=== DEBUGGING MAIN APP DETAILED ===")
    
    app = RansomwareResilienceApp()
    
    # Initialize session
    print("1. Initializing session...")
    success = app.initialize_session()
    print(f"Session initialization: {success}")
    
    if not success:
        print("Session failed to initialize")
        return
    
    print(f"Session data keys: {list(app.session_data.keys())}")
    print()
    
    # Create mock responses that match questionnaire structure
    print("2. Creating mock responses...")
    mock_responses = {
        'pre_infection': {
            'backup_strategy': {
                'value': 3,
                'text': 'Daily automated backups with offsite storage',
                'weight': 10,
                'mitre_technique': 'T1490'
            },
            'backup_isolation': {
                'value': 2,
                'text': 'Partial isolation of backup systems',
                'weight': 9,
                'mitre_technique': 'T1490'
            },
            'network_segmentation': {
                'value': 4,
                'text': 'Comprehensive network segmentation',
                'weight': 8,
                'mitre_technique': 'T1210'
            },
            'endpoint_protection': {
                'value': 3,
                'text': 'Advanced endpoint protection deployed',
                'weight': 8,
                'mitre_technique': 'T1055'
            },
            'email_security': {
                'value': 2,
                'text': 'Basic email filtering in place',
                'weight': 7,
                'mitre_technique': 'T1566'
            },
            'patch_management': {
                'value': 3,
                'text': 'Regular patching schedule maintained',
                'weight': 8,
                'mitre_technique': 'T1190'
            },
            'access_controls': {
                'value': 4,
                'text': 'Robust access control policies',
                'weight': 9,
                'mitre_technique': 'T1078'
            }
        },
        'active_infection': {
            'incident_response': {
                'value': 3,
                'text': 'Documented incident response procedures',
                'weight': 10,
                'mitre_technique': 'T1486'
            },
            'user_training': {
                'value': 2,
                'text': 'Basic security awareness training',
                'weight': 7,
                'mitre_technique': 'T1566'
            },
            'monitoring_detection': {
                'value': 4,
                'text': 'Advanced monitoring and detection',
                'weight': 9,
                'mitre_technique': 'T1055'
            },
            'communication_plan': {
                'value': 3,
                'text': 'Clear communication protocols',
                'weight': 6,
                'mitre_technique': 'T1486'
            }
        },
        'post_infection': {
            'recovery_plan': {
                'value': 3,
                'text': 'Documented recovery procedures',
                'weight': 9,
                'mitre_technique': 'T1490'
            },
            'business_continuity': {
                'value': 2,
                'text': 'Basic business continuity planning',
                'weight': 8,
                'mitre_technique': 'T1486'
            },
            'legal_compliance': {
                'value': 4,
                'text': 'Strong legal and compliance framework',
                'weight': 7,
                'mitre_technique': 'T1486'
            },
            'lessons_learned': {
                'value': 3,
                'text': 'Post-incident review processes',
                'weight': 6,
                'mitre_technique': 'T1486'
            }
        }
    }
    
    print(f"Mock responses created with {len(mock_responses)} stages")
    for stage, responses in mock_responses.items():
        print(f"   {stage}: {len(responses)} questions")
    print()
    
    # Test scoring directly
    print("3. Testing scoring with mock responses...")
    scores = app.calculate_scores(mock_responses)
    if scores:
        print(f"Scoring successful!")
        print(f"Overall assessment keys: {list(scores.keys())}")
        if 'overall_assessment' in scores:
            print(f"Overall score: {scores['overall_assessment'].get('overall_score', 'N/A')}")
    else:
        print("Scoring failed!")
    print()
    
    # Test recommendations
    print("4. Testing recommendations...")
    if scores:
        recommendations = app.generate_recommendations(mock_responses, scores)
        if recommendations:
            print(f"Recommendations successful!")
            print(f"Recommendation keys: {list(recommendations.keys())}")
        else:
            print("Recommendations failed!")
    print()
    
    # Test display
    print("5. Testing display...")
    if scores and recommendations:
        try:
            app.display_results(scores, recommendations)
            print("Display successful!")
        except Exception as e:
            print(f"Display failed: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    debug_main_app_detailed()
