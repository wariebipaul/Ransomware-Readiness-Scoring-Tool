import unittest
from src.assessment.questionnaire import Questionnaire
from src.assessment.scoring import Scoring

class TestAssessment(unittest.TestCase):

    def setUp(self):
        self.questionnaire = Questionnaire()
        self.scoring = Scoring()

    def test_questionnaire_initialization(self):
        self.assertIsNotNone(self.questionnaire)

    def test_collect_responses(self):
        # Simulate user responses
        responses = self.questionnaire.collect_responses()
        self.assertIsInstance(responses, dict)
        self.assertGreater(len(responses), 0)

    def test_scoring_calculation(self):
        # Simulate user responses for scoring
        responses = {
            'backup_data': 'yes',
            'update_software': 'no',
            'incident_response_plan': 'yes'
        }
        score = self.scoring.calculate_score(responses)
        self.assertIsInstance(score, int)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

if __name__ == '__main__':
    unittest.main()