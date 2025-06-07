import unittest
from src.assessment.scoring import Scoring

class TestScoring(unittest.TestCase):

    def setUp(self):
        self.scoring = Scoring()

    def test_calculate_score_perfect(self):
        responses = {
            'backups': True,
            'software_updates': True,
            'network_segmentation': True,
            'incident_response_plan': True
        }
        score = self.scoring.calculate_score(responses)
        self.assertEqual(score, 100)

    def test_calculate_score_partial(self):
        responses = {
            'backups': True,
            'software_updates': False,
            'network_segmentation': True,
            'incident_response_plan': False
        }
        score = self.scoring.calculate_score(responses)
        self.assertEqual(score, 50)

    def test_calculate_score_none(self):
        responses = {
            'backups': False,
            'software_updates': False,
            'network_segmentation': False,
            'incident_response_plan': False
        }
        score = self.scoring.calculate_score(responses)
        self.assertEqual(score, 0)

if __name__ == '__main__':
    unittest.main()