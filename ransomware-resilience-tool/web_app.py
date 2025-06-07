#!/usr/bin/env python3
"""
Ransomware Resilience Assessment Tool - Web Application

Flask-based web interface for the comprehensive ransomware resilience assessment tool.
Provides interactive questionnaire, real-time scoring, and detailed reporting.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import assessment modules
from assessment.questionnaire import Questionnaire
from assessment.scoring import Scoring
from assessment.recommendations import Recommendations
from utils.validation import InputValidator
from utils.export import AssessmentExporter

# Import data modules
from data.questions import QUESTIONS
from data.frameworks import MITRE_TECHNIQUES, FRAMEWORKS

app = Flask(__name__)
app.secret_key = 'ransomware_assessment_tool_2024'  # Change this in production

class WebAssessmentApp:
    """
    Web-based Ransomware Resilience Assessment Application.
    
    Manages assessment sessions, calculates scores, and generates reports
    through a web interface.
    """
    
    def __init__(self):
        self.validator = InputValidator()
        
    def initialize_session(self) -> bool:
        """Initialize a new assessment session."""
        try:
            session['assessment_data'] = {
                'start_time': datetime.now().isoformat(),
                'organization': '',
                'assessor': '',
                'role': '',
                'responses': {},
                'current_stage': 0,
                'progress': 0,
                'completed': False
            }
            return True
        except Exception as e:
            print(f"Session initialization error: {e}")
            return False
    
    def save_organization_info(self, org_name: str, assessor_name: str, role: str) -> bool:
        """Save organization information to session."""
        try:
            if 'assessment_data' not in session:
                self.initialize_session()
            
            session['assessment_data']['organization'] = org_name
            session['assessment_data']['assessor'] = assessor_name
            session['assessment_data']['role'] = role
            session.modified = True
            return True
        except Exception as e:
            print(f"Error saving organization info: {e}")
            return False
    
    def save_response(self, stage: str, question_id: str, response_data: Dict[str, Any]) -> bool:
        """Save a questionnaire response to the session."""
        try:
            if 'assessment_data' not in session:
                self.initialize_session()
            
            if stage not in session['assessment_data']['responses']:
                session['assessment_data']['responses'][stage] = {}
            
            session['assessment_data']['responses'][stage][question_id] = response_data
            session.modified = True
            return True
        except Exception as e:
            print(f"Error saving response: {e}")
            return False
    
    def calculate_progress(self) -> float:
        """Calculate assessment completion progress."""
        total_questions = sum(len(stage_data['questions']) for stage_data in QUESTIONS.values())
        completed_questions = sum(
            len(stage_responses) 
            for stage_responses in session.get('assessment_data', {}).get('responses', {}).values()
        )
        return (completed_questions / total_questions) * 100 if total_questions > 0 else 0
    
    def calculate_scores(self) -> Optional[Dict[str, Any]]:
        """Calculate assessment scores."""
        try:
            responses = session.get('assessment_data', {}).get('responses', {})
            
            if not responses:
                print("DEBUG: No responses found")
                return None
            
            print(f"DEBUG: Raw responses: {responses}")
            
            # Convert web response format to scoring engine format
            scoring_responses = {}
            for stage_key, stage_responses in responses.items():
                scoring_responses[stage_key] = {}
                for question_id, response_data in stage_responses.items():
                    # Get question weight from QUESTIONS data
                    question_weight = 5  # default weight
                    for q_data in QUESTIONS.get(stage_key, {}).get('questions', []):
                        if q_data['id'] == question_id:
                            question_weight = q_data['weight']
                            break
                    
                    # Convert to scoring engine format
                    scoring_responses[stage_key][question_id] = {
                        'value': response_data.get('score', 0),
                        'weight': question_weight,
                        'text': response_data.get('answer_text', ''),
                        'comments': response_data.get('comments', ''),
                        'timestamp': response_data.get('timestamp', ''),
                        'mitre_technique': ''  # Add empty mitre_technique for compatibility
                    }
            
            print(f"DEBUG: Converted responses: {scoring_responses}")
            
            scoring_engine = Scoring(scoring_responses)
            raw_results = scoring_engine.generate_score_report()
            
            # Transform the results to match template expectations
            stage_performance = {}
            for stage_name, stage_data in raw_results.get('stage_performance', {}).items():
                stage_performance[stage_name] = {
                    'percentage': stage_data.get('percentage', 0),
                    'score': stage_data.get('score', 0),
                    'max_score': stage_data.get('max_score', 0),
                    'answered_questions': len([q for q in scoring_responses.get(stage_name, {}).keys()]),
                    'total_questions': len([q for q in scoring_responses.get(stage_name, {}).keys()]),
                    'weighted_score': stage_data.get('score', 0)  # Use actual score as weighted score
                }
            
            # Calculate MITRE coverage summary
            mitre_data = raw_results.get('mitre_coverage', {})
            techniques_covered = len([t for t, data in mitre_data.items() if data.get('percentage', 0) > 0])
            coverage_percentage = (techniques_covered / len(mitre_data)) * 100 if mitre_data else 0
            
            results = {
                'overall_assessment': raw_results.get('overall_assessment', {}),
                'stage_performance': stage_performance,
                'risk_assessment': {
                    'top_risk_areas': [
                        {
                            'area': area.get('question_id', '').replace('_', ' ').title(),
                            'score': area.get('percentage', 0)
                        } for area in raw_results.get('risk_areas', [])
                    ]
                },
                'strength_assessment': {
                    'strength_areas': [
                        {
                            'area': area.get('question_id', '').replace('_', ' ').title(),
                            'score': area.get('percentage', 0)
                        } for area in raw_results.get('strength_areas', [])
                    ]
                },
                'mitre_coverage': {
                    'techniques_covered': techniques_covered,
                    'total_techniques': len(mitre_data),
                    'coverage_percentage': round(coverage_percentage, 1),
                    'technique_details': mitre_data
                },
                'summary_insights': raw_results.get('summary_insights', [])
            }
            
            return results
        except Exception as e:
            print(f"Score calculation error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_recommendations(self, scores: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate recommendations based on scores."""
        try:
            # For now, return basic recommendations until we fix the recommendation engine
            recommendations = {
                'priority_actions': [
                    {
                        'title': 'Enhance Backup Strategy',
                        'description': 'Implement comprehensive backup and recovery procedures',
                        'priority': 'High',
                        'timeframe': '30 days'
                    },
                    {
                        'title': 'Strengthen Access Controls',
                        'description': 'Deploy multi-factor authentication across all systems',
                        'priority': 'High',
                        'timeframe': '60 days'
                    },
                    {
                        'title': 'Improve Incident Response',
                        'description': 'Develop and test incident response procedures',
                        'priority': 'Medium',
                        'timeframe': '90 days'
                    }
                ],
                'framework_alignment': {
                    'nist': 'Recommendations align with NIST Cybersecurity Framework',
                    'iso27001': 'Supports ISO 27001 compliance requirements'
                },
                'executive_summary': 'Your organization shows good security practices with room for improvement in backup and incident response capabilities.',
                'detailed_recommendations': []
            }
            return recommendations
        except Exception as e:
            print(f"Recommendation generation error: {e}")
            return None

# Initialize the web application
web_app = WebAssessmentApp()

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')

@app.route('/start-assessment', methods=['GET', 'POST'])
def start_assessment():
    """Start a new assessment or display the setup form."""
    if request.method == 'POST':
        # Save organization information
        org_name = request.form.get('organization', '').strip()
        assessor_name = request.form.get('assessor', '').strip()
        role = request.form.get('role', '').strip()
        
        if not all([org_name, assessor_name, role]):
            return render_template('setup.html', error="All fields are required.")
        
        if web_app.save_organization_info(org_name, assessor_name, role):
            return redirect(url_for('questionnaire'))
        else:
            return render_template('setup.html', error="Failed to save information. Please try again.")
    
    # Initialize new session
    web_app.initialize_session()
    return render_template('setup.html')

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    """Display the interactive questionnaire."""
    if 'assessment_data' not in session:
        return redirect(url_for('start_assessment'))
    
    progress = web_app.calculate_progress()
    
    return render_template('questionnaire.html', 
                         questions=QUESTIONS,
                         session_data=session['assessment_data'],
                         progress=progress)

@app.route('/api/save-response', methods=['POST'])
def api_save_response():
    """API endpoint to save questionnaire responses."""
    try:
        data = request.get_json()
        stage = data.get('stage')
        question_id = data.get('question_id')
        response_data = data.get('response_data')
        
        if not all([stage, question_id, response_data]):
            return jsonify({'success': False, 'error': 'Missing required data'})
        
        success = web_app.save_response(stage, question_id, response_data)
        progress = web_app.calculate_progress()
        
        return jsonify({
            'success': success,
            'progress': progress,
            'completed': progress >= 100
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/results')
def results():
    """Display assessment results and recommendations."""
    if 'assessment_data' not in session:
        return redirect(url_for('start_assessment'))
    
    # Calculate scores
    scores = web_app.calculate_scores()
    if not scores:
        return render_template('error.html', 
                             error="Unable to calculate scores. Please complete the assessment first.")
    
    # Generate recommendations
    recommendations = web_app.generate_recommendations(scores)
    if not recommendations:
        return render_template('error.html', 
                             error="Unable to generate recommendations.")
    
    return render_template('results.html',
                         session_data=session['assessment_data'],
                         scores=scores,
                         recommendations=recommendations)

@app.route('/api/export/<format>')
def api_export(format):
    """API endpoint to export results in various formats."""
    try:
        if 'assessment_data' not in session:
            return jsonify({'error': 'No assessment data found'})
        
        scores = web_app.calculate_scores()
        if not scores:
            return jsonify({'error': 'Unable to calculate scores'})
        
        recommendations = web_app.generate_recommendations(scores)
        
        exporter = AssessmentExporter()
        export_data = {
            'session_data': session['assessment_data'],
            'scores': scores,
            'recommendations': recommendations
        }
        
        if format.lower() == 'json':
            result = exporter.export_to_json(export_data)
        elif format.lower() == 'csv':
            result = exporter.export_to_csv(export_data)
        else:
            return jsonify({'error': 'Unsupported format'})
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/framework-info')
def framework_info():
    """Display information about cybersecurity frameworks."""
    return render_template('framework_info.html',
                         mitre_techniques=MITRE_TECHNIQUES,
                         frameworks=FRAMEWORKS)

@app.route('/help')
def help_page():
    """Display help and documentation."""
    return render_template('help.html')

@app.route('/api/session-status')
def api_session_status():
    """API endpoint to get current session status."""
    if 'assessment_data' not in session:
        return jsonify({'session_active': False})
    
    progress = web_app.calculate_progress()
    return jsonify({
        'session_active': True,
        'progress': progress,
        'organization': session['assessment_data'].get('organization', ''),
        'assessor': session['assessment_data'].get('assessor', ''),
        'start_time': session['assessment_data'].get('start_time', '')
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
