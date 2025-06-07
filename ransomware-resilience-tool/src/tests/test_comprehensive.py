"""
Comprehensive Test Suite for Ransomware Resilience Assessment Tool

This module provides thorough testing of all components including questionnaire,
scoring, recommendations, validation, and export functionality.
"""

import unittest
import tempfile
import os
import json
from datetime import datetime
from unittest.mock import MagicMock, patch

# Import modules to test
import sys
sys.path.append('/workspaces/Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool/src')

from data.questions import QUESTIONS
from data.frameworks import MITRE_TECHNIQUES, FRAMEWORKS, RECOMMENDATION_TEMPLATES
from assessment.questionnaire import Questionnaire
from assessment.scoring import Scoring
from assessment.recommendations import Recommendations
from utils.validation import InputValidator
from utils.export import AssessmentExporter


class TestQuestionnaireModule(unittest.TestCase):
    """Test cases for the questionnaire module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = InputValidator()
        self.questionnaire = Questionnaire()
    
    def test_questionnaire_initialization(self):
        """Test questionnaire proper initialization."""
        self.assertIsNotNone(self.questionnaire.questions)
        self.assertIsNotNone(self.questionnaire.validator)
        # Check that we have the expected stages
        expected_stages = ['pre_infection', 'active_infection', 'post_infection']
        for stage in expected_stages:
            self.assertIn(stage, self.questionnaire.questions)
        
        # Count total questions across all stages
        total_questions = sum(len(stage_data['questions']) for stage_data in self.questionnaire.questions.values())
        self.assertEqual(total_questions, 15)
    
    def test_question_structure_validation(self):
        """Test that all questions have required structure."""
        required_fields = ['id', 'question', 'options', 'weight', 'mitre_technique']
        
        for stage_key, stage_data in self.questionnaire.questions.items():
            for question in stage_data['questions']:
                for field in required_fields:
                    self.assertIn(field, question, f"Question {question.get('id')} missing {field}")
            
            # Test options structure
            self.assertEqual(len(question['options']), 5, 
                           f"Question {question['id']} should have 5 options")
            
            # Test weight is numeric
            self.assertIsInstance(question['weight'], (int, float),
                                f"Question {question['id']} weight should be numeric")
    
    def test_stage_distribution(self):
        """Test that questions are properly distributed across stages."""
        stages = {}
        for stage_key, stage_data in self.questionnaire.questions.items():
            stages[stage_key] = len(stage_data['questions'])
        
        # Should have questions for all three stages
        expected_stages = ['pre_infection', 'active_infection', 'post_infection']
        for stage in expected_stages:
            self.assertIn(stage, stages, f"Missing questions for {stage} stage")
            self.assertGreater(stages[stage], 0, f"No questions for {stage} stage")
    
    def test_validate_response_structure(self):
        """Test response validation."""
        # Test empty responses - should be invalid
        is_valid, message = self.questionnaire.validate_responses()
        self.assertFalse(is_valid)
        self.assertIn("Missing responses", message)
        
        # Add some responses to test partial validation
        self.questionnaire.responses = {
            'pre_infection': {
                'backup_strategy': {
                    'value': 3,
                    'text': 'Daily automated backups',
                    'weight': 10,
                    'mitre_technique': 'T1490'
                }
            }
        }
        
        # Should still be invalid as we're missing other stages
        is_valid, message = self.questionnaire.validate_responses()
        self.assertFalse(is_valid)


class TestScoringModule(unittest.TestCase):
    """Test cases for the scoring module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Sample responses for testing
        self.sample_responses = {
            'pre_asset_mgmt': {'response_index': 3, 'stage': 'pre-infection'},
            'pre_access_control': {'response_index': 2, 'stage': 'pre-infection'},
            'pre_backup_strategy': {'response_index': 4, 'stage': 'pre-infection'},
            'active_incident_response': {'response_index': 1, 'stage': 'active-infection'},
            'active_containment': {'response_index': 2, 'stage': 'active-infection'},
            'post_recovery_procedures': {'response_index': 3, 'stage': 'post-infection'},
        }
        
        self.scoring_engine = Scoring(
            responses=self.sample_responses
        )
    
    def test_scoring_initialization(self):
        """Test scoring engine initialization."""
        self.assertIsNotNone(self.scoring_engine.responses)
        self.assertEqual(self.scoring_engine.total_score, 0)
        self.assertEqual(self.scoring_engine.percentage_score, 0)
    
    def test_overall_score_calculation(self):
        """Test overall score calculation."""
        score_report = self.scoring_engine.calculate_score()
        
        # Score should be between 0 and 100
        self.assertGreaterEqual(self.scoring_engine.percentage_score, 0)
        self.assertLessEqual(self.scoring_engine.percentage_score, 100)
        self.assertIsInstance(self.scoring_engine.percentage_score, (int, float))
    
    def test_stage_scores_calculation(self):
        """Test stage-specific score calculation."""
        self.scoring_engine.calculate_score()
        stage_scores = self.scoring_engine.scores
        
        # Should have scores for all stages
        expected_stages = ['pre_infection', 'active_infection', 'post_infection']
        for stage in expected_stages:
            self.assertIn(stage, stage_scores)
            score_data = stage_scores[stage]
            self.assertIn('score', score_data)
            self.assertIn('status', score_data)
            
            # Score should be valid percentage
            self.assertGreaterEqual(score_data['score'], 0)
            self.assertLessEqual(score_data['score'], 100)
    
    def test_readiness_level_determination(self):
        """Test readiness level categorization."""
        readiness_level = self.scoring_engine.get_readiness_level()
        
        valid_levels = ['Critical', 'Basic', 'Moderate', 'Advanced', 'Optimal']
        self.assertIn(readiness_level, valid_levels)
    
    def test_risk_analysis(self):
        """Test risk factor analysis."""
        risk_analysis = self.scoring_engine.analyze_risk_factors()
        
        self.assertIn('critical_gaps', risk_analysis)
        self.assertIn('high_priority', risk_analysis)
        self.assertIn('medium_priority', risk_analysis)
        self.assertIsInstance(risk_analysis['critical_gaps'], list)
    
    def test_strength_analysis(self):
        """Test strength identification."""
        strength_analysis = self.scoring_engine.analyze_strengths()
        
        self.assertIn('identified_strengths', strength_analysis)
        self.assertIn('strong_areas', strength_analysis)
        self.assertIsInstance(strength_analysis['identified_strengths'], list)
    
    def test_mitre_coverage_calculation(self):
        """Test MITRE ATT&CK coverage calculation."""
        coverage = self.scoring_engine.calculate_mitre_coverage()
        
        self.assertIn('total_techniques', coverage)
        self.assertIn('covered_techniques', coverage)
        self.assertIn('coverage_percentage', coverage)
        
        # Coverage percentage should be valid
        self.assertGreaterEqual(coverage['coverage_percentage'], 0)
        self.assertLessEqual(coverage['coverage_percentage'], 100)


class TestRecommendationModule(unittest.TestCase):
    """Test cases for the recommendation module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_responses = {
            'pre_asset_mgmt': {'response_index': 1, 'stage': 'pre-infection'},
            'pre_access_control': {'response_index': 0, 'stage': 'pre-infection'},
        }
        
        self.sample_scores = {
            'overall_score': 45.0,
            'stage_scores': {
                'pre-infection': {'score': 40.0, 'status': 'Critical'},
                'active-infection': {'score': 50.0, 'status': 'Basic'},
                'post-infection': {'score': 45.0, 'status': 'Basic'}
            },
            'readiness_level': 'Basic'
        }
        
        self.rec_engine = Recommendations(
            score_report=self.sample_scores
        )
    
    def test_recommendation_engine_initialization(self):
        """Test recommendation engine initialization."""
        self.assertIsNotNone(self.rec_engine.score_report)
        self.assertIsNotNone(self.rec_engine.recommendations)
    
    def test_priority_recommendations_generation(self):
        """Test priority recommendation generation."""
        priority_recs = self.rec_engine.generate_priority_recommendations()
        
        self.assertIsInstance(priority_recs, list)
        self.assertGreater(len(priority_recs), 0)
        
        # Check recommendation structure
        for rec in priority_recs[:5]:  # Check first 5
            self.assertIn('title', rec)
            self.assertIn('description', rec)
            self.assertIn('priority', rec)
            self.assertIn('timeline', rec)
            self.assertIn('category', rec)
    
    def test_framework_alignment(self):
        """Test framework alignment generation."""
        alignment = self.rec_engine.align_with_frameworks()
        
        self.assertIsInstance(alignment, dict)
        # Should have alignments for major frameworks
        framework_keys = ['nist', 'iso27001', 'cis_controls']
        for key in framework_keys:
            if key in alignment:
                self.assertIsInstance(alignment[key], list)
    
    def test_implementation_plan_creation(self):
        """Test implementation plan generation."""
        impl_plan = self.rec_engine.create_implementation_plan()
        
        self.assertIn('phases', impl_plan)
        self.assertIn('timeline', impl_plan)
        self.assertIn('resources', impl_plan)
        
        # Check phases structure
        phases = impl_plan['phases']
        expected_phases = ['immediate', 'short_term', 'long_term']
        for phase in expected_phases:
            if phase in phases:
                self.assertIsInstance(phases[phase], list)
    
    def test_executive_summary_generation(self):
        """Test executive summary generation."""
        exec_summary = self.rec_engine.generate_executive_summary()
        
        required_fields = ['overall_assessment', 'key_findings', 'critical_actions', 
                          'risk_level', 'investment_priority']
        
        for field in required_fields:
            self.assertIn(field, exec_summary)
            self.assertIsInstance(exec_summary[field], str)
            self.assertGreater(len(exec_summary[field]), 0)


class TestValidationModule(unittest.TestCase):
    """Test cases for the validation module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = InputValidator()
    
    def test_numeric_choice_validation(self):
        """Test numeric choice validation."""
        # Valid choices
        self.assertTrue(self.validator.validate_numeric_choice("1", 1, 5))
        self.assertTrue(self.validator.validate_numeric_choice("3", 1, 5))
        self.assertTrue(self.validator.validate_numeric_choice("5", 1, 5))
        
        # Invalid choices
        self.assertFalse(self.validator.validate_numeric_choice("0", 1, 5))
        self.assertFalse(self.validator.validate_numeric_choice("6", 1, 5))
        self.assertFalse(self.validator.validate_numeric_choice("abc", 1, 5))
        self.assertFalse(self.validator.validate_numeric_choice("", 1, 5))
    
    def test_text_validation(self):
        """Test text input validation."""
        # Valid text
        self.assertTrue(self.validator.validate_text("Valid organization name"))
        self.assertTrue(self.validator.validate_text("Test Corp"))
        
        # Invalid text
        self.assertFalse(self.validator.validate_text(""))
        self.assertFalse(self.validator.validate_text("   "))
        self.assertFalse(self.validator.validate_text("A" * 1001))  # Too long
    
    def test_email_validation(self):
        """Test email validation."""
        # Valid emails
        self.assertTrue(self.validator.validate_email("test@example.com"))
        self.assertTrue(self.validator.validate_email("user.name@domain.org"))
        
        # Invalid emails
        self.assertFalse(self.validator.validate_email("invalid-email"))
        self.assertFalse(self.validator.validate_email("@domain.com"))
        self.assertFalse(self.validator.validate_email("user@"))
        self.assertFalse(self.validator.validate_email(""))
    
    def test_sanitize_input(self):
        """Test input sanitization."""
        # Test trimming whitespace
        self.assertEqual(self.validator.sanitize_input("  test  "), "test")
        
        # Test HTML escaping
        self.assertEqual(self.validator.sanitize_input("<script>"), "&lt;script&gt;")
        
        # Test SQL injection prevention
        dangerous_input = "'; DROP TABLE users; --"
        sanitized = self.validator.sanitize_input(dangerous_input)
        self.assertNotIn("DROP TABLE", sanitized)


class TestExportModule(unittest.TestCase):
    """Test cases for the export module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_session = {
            'organization': 'Test Corp',
            'assessor': 'John Doe',
            'start_time': datetime.now(),
            'responses': {}
        }
        
        self.sample_results = {
            'overall_score': 75.5,
            'readiness_level': 'Moderate',
            'stage_scores': {
                'pre-infection': {'score': 80.0, 'status': 'Good'},
                'active-infection': {'score': 70.0, 'status': 'Moderate'},
                'post-infection': {'score': 76.0, 'status': 'Good'}
            }
        }
        
        self.sample_recommendations = {
            'priority_actions': [
                {
                    'title': 'Implement Multi-Factor Authentication',
                    'priority': 'High',
                    'timeline': '30 days',
                    'description': 'Deploy MFA across all critical systems',
                    'category': 'Access Control'
                }
            ]
        }
        
        self.exporter = AssessmentExporter(
            self.sample_session,
            self.sample_results,
            self.sample_recommendations
        )
    
    def test_exporter_initialization(self):
        """Test exporter initialization."""
        self.assertIsNotNone(self.exporter.session_data)
        self.assertIsNotNone(self.exporter.results)
        self.assertIsNotNone(self.exporter.recommendations)
        self.assertIsNotNone(self.exporter.export_timestamp)
    
    def test_json_export(self):
        """Test JSON export functionality."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            success = self.exporter.export_to_json(temp_file)
            self.assertTrue(success)
            self.assertTrue(os.path.exists(temp_file))
            
            # Verify JSON structure
            with open(temp_file, 'r') as f:
                data = json.load(f)
                self.assertIn('metadata', data)
                self.assertIn('session_info', data)
                self.assertIn('results', data)
                self.assertIn('recommendations', data)
        
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_csv_export(self):
        """Test CSV export functionality."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        try:
            success = self.exporter.export_to_csv(temp_file)
            self.assertTrue(success)
            self.assertTrue(os.path.exists(temp_file))
            
            # Verify file has content
            with open(temp_file, 'r') as f:
                content = f.read()
                self.assertIn('Ransomware Resilience Assessment Report', content)
                self.assertIn('Test Corp', content)
        
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_text_export(self):
        """Test text export functionality."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_file = f.name
        
        try:
            success = self.exporter.export_to_text(temp_file)
            self.assertTrue(success)
            self.assertTrue(os.path.exists(temp_file))
            
            # Verify file has content
            with open(temp_file, 'r') as f:
                content = f.read()
                self.assertIn('RANSOMWARE RESILIENCE ASSESSMENT REPORT', content)
                self.assertIn('Test Corp', content)
                self.assertIn('75.5%', content)
        
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete assessment flow."""
    
    def test_complete_assessment_flow(self):
        """Test the complete assessment workflow."""
        # Step 1: Initialize questionnaire
        validator = InputValidator()
        questionnaire = Questionnaire()
        
        # Step 2: Simulate responses
        sample_responses = {}
        for i, question in enumerate(QUESTIONS):
            sample_responses[question['id']] = {
                'response_index': i % 5,  # Cycle through response options
                'response_text': question['options'][i % 5],
                'stage': question['stage'],
                'timestamp': datetime.now().isoformat()
            }
        
        # Step 3: Calculate scores
        scoring_engine = Scoring(
            responses=sample_responses
        )
        
        scores = scoring_engine.generate_score_report()
        
        # Step 4: Generate recommendations
        rec_engine = Recommendations(
            score_report=scores
        )
        rec_engine.generate_recommendations()
        
        recommendations = {
            'priority_actions': rec_engine.get_prioritized_action_plan(),
            'executive_summary': rec_engine.generate_executive_summary()
        }
        
        # Step 5: Export results
        session_data = {
            'organization': 'Integration Test Corp',
            'assessor': 'Test User',
            'start_time': datetime.now()
        }
        
        exporter = AssessmentExporter(session_data, scores, recommendations)
        
        # Verify all components work together
        self.assertIsNotNone(scores['overall_score'])
        self.assertIsNotNone(scores['readiness_level'])
        self.assertGreater(len(recommendations['priority_actions']), 0)
        self.assertIsNotNone(exporter)
        
        # Test export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            export_success = exporter.export_to_json(temp_file)
            self.assertTrue(export_success)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


def run_comprehensive_tests():
    """Run all test suites."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestQuestionnaireModule,
        TestScoringModule,
        TestRecommendationModule,
        TestValidationModule,
        TestExportModule,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_comprehensive_tests()
    exit(0 if success else 1)
