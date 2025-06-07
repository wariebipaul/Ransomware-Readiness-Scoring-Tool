# Scoring module for ransomware readiness assessment
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data.questions import SCORE_THRESHOLDS
from data.frameworks import MITRE_TECHNIQUES

class Scoring:
    def __init__(self, responses=None):
        self.responses = responses or {}
        self.scores = {}
        self.total_score = 0
        self.max_possible_score = 0
        self.percentage_score = 0
        self.readiness_level = ""
        
    def calculate_score(self, responses=None):
        """
        Calculate comprehensive readiness score based on weighted responses
        Returns detailed scoring breakdown and overall assessment
        """
        if responses:
            self.responses = responses
            
        self.scores = {
            "pre_infection": {"score": 0, "max_score": 0, "percentage": 0},
            "active_infection": {"score": 0, "max_score": 0, "percentage": 0},
            "post_infection": {"score": 0, "max_score": 0, "percentage": 0}
        }
        
        # Calculate scores for each stage
        for stage_key, stage_responses in self.responses.items():
            stage_score, stage_max = self._calculate_stage_score(stage_responses)
            self.scores[stage_key]["score"] = stage_score
            self.scores[stage_key]["max_score"] = stage_max
            self.scores[stage_key]["percentage"] = (stage_score / stage_max * 100) if stage_max > 0 else 0
        
        # Calculate overall scores
        self.total_score = sum(stage["score"] for stage in self.scores.values())
        self.max_possible_score = sum(stage["max_score"] for stage in self.scores.values())
        self.percentage_score = (self.total_score / self.max_possible_score * 100) if self.max_possible_score > 0 else 0
        
        # Determine readiness level
        self.readiness_level = self._determine_readiness_level(self.percentage_score)
        
        return {
            "total_score": self.total_score,
            "max_possible_score": self.max_possible_score,
            "percentage_score": round(self.percentage_score, 1),
            "readiness_level": self.readiness_level,
            "stage_scores": self.scores,
            "detailed_breakdown": self._get_detailed_breakdown()
        }
    
    def _calculate_stage_score(self, stage_responses):
        """Calculate score for a specific stage"""
        stage_score = 0
        stage_max = 0
        
        for question_id, response in stage_responses.items():
            weighted_score = response['value'] * response['weight']
            max_weighted_score = 4 * response['weight']  # Maximum value is 4
            
            stage_score += weighted_score
            stage_max += max_weighted_score
            
        return stage_score, stage_max
    
    def _determine_readiness_level(self, percentage):
        """Determine readiness level based on percentage score"""
        if percentage >= SCORE_THRESHOLDS["excellent"]:
            return "Excellent"
        elif percentage >= SCORE_THRESHOLDS["good"]:
            return "Good"
        elif percentage >= SCORE_THRESHOLDS["moderate"]:
            return "Moderate"
        elif percentage >= SCORE_THRESHOLDS["poor"]:
            return "Poor"
        else:
            return "Critical"
    
    def _get_detailed_breakdown(self):
        """Get detailed breakdown of scores by question"""
        breakdown = {}
        
        for stage_key, stage_responses in self.responses.items():
            stage_breakdown = {}
            
            for question_id, response in stage_responses.items():
                weighted_score = response['value'] * response['weight']
                max_weighted_score = 4 * response['weight']
                question_percentage = (weighted_score / max_weighted_score * 100) if max_weighted_score > 0 else 0
                
                stage_breakdown[question_id] = {
                    "score": weighted_score,
                    "max_score": max_weighted_score,
                    "percentage": round(question_percentage, 1),
                    "weight": response['weight'],
                    "response_text": response['text'],
                    "mitre_technique": response['mitre_technique']
                }
            
            breakdown[stage_key] = stage_breakdown
        
        return breakdown
    
    def get_risk_areas(self):
        """Identify areas with the highest risk (lowest scores)"""
        risk_areas = []
        breakdown = self._get_detailed_breakdown()
        
        for stage_key, stage_breakdown in breakdown.items():
            for question_id, question_data in stage_breakdown.items():
                if question_data['percentage'] < 50:  # Below 50% considered high risk
                    risk_areas.append({
                        'stage': stage_key,
                        'question_id': question_id,
                        'percentage': question_data['percentage'],
                        'mitre_technique': question_data['mitre_technique'],
                        'response': question_data['response_text']
                    })
        
        # Sort by percentage (lowest first)
        risk_areas.sort(key=lambda x: x['percentage'])
        return risk_areas
    
    def get_strength_areas(self):
        """Identify areas of strength (highest scores)"""
        strength_areas = []
        breakdown = self._get_detailed_breakdown()
        
        for stage_key, stage_breakdown in breakdown.items():
            for question_id, question_data in stage_breakdown.items():
                if question_data['percentage'] >= 75:  # Above 75% considered strength
                    strength_areas.append({
                        'stage': stage_key,
                        'question_id': question_id,
                        'percentage': question_data['percentage'],
                        'mitre_technique': question_data['mitre_technique'],
                        'response': question_data['response_text']
                    })
        
        # Sort by percentage (highest first)
        strength_areas.sort(key=lambda x: x['percentage'], reverse=True)
        return strength_areas
    
    def get_mitre_coverage(self):
        """Analyze coverage of MITRE ATT&CK techniques"""
        technique_scores = {}
        
        for stage_key, stage_responses in self.responses.items():
            for question_id, response in stage_responses.items():
                technique = response['mitre_technique']
                weighted_score = response['value'] * response['weight']
                max_weighted_score = 4 * response['weight']
                
                if technique not in technique_scores:
                    technique_scores[technique] = {
                        'total_score': 0,
                        'max_score': 0,
                        'questions': []
                    }
                
                technique_scores[technique]['total_score'] += weighted_score
                technique_scores[technique]['max_score'] += max_weighted_score
                technique_scores[technique]['questions'].append({
                    'question_id': question_id,
                    'stage': stage_key,
                    'score': weighted_score,
                    'max_score': max_weighted_score
                })
        
        # Calculate percentages
        for technique, data in technique_scores.items():
            data['percentage'] = (data['total_score'] / data['max_score'] * 100) if data['max_score'] > 0 else 0
            if technique in MITRE_TECHNIQUES:
                data['technique_info'] = MITRE_TECHNIQUES[technique]
        
        return technique_scores
    
    def generate_score_report(self):
        """Generate a comprehensive scoring report"""
        score_data = self.calculate_score()
        risk_areas = self.get_risk_areas()
        strength_areas = self.get_strength_areas()
        mitre_coverage = self.get_mitre_coverage()
        
        report = {
            "overall_assessment": {
                "percentage_score": score_data["percentage_score"],
                "readiness_level": score_data["readiness_level"],
                "total_score": score_data["total_score"],
                "max_possible_score": score_data["max_possible_score"]
            },
            "stage_performance": score_data["stage_scores"],
            "risk_areas": risk_areas[:5],  # Top 5 risk areas
            "strength_areas": strength_areas[:5],  # Top 5 strengths
            "mitre_coverage": mitre_coverage,
            "summary_insights": self._generate_insights(score_data, risk_areas, strength_areas)
        }
        
        return report
    
    def _generate_insights(self, score_data, risk_areas, strength_areas):
        """Generate key insights from the assessment"""
        insights = []
        
        # Overall performance insight
        level = score_data["readiness_level"]
        percentage = score_data["percentage_score"]
        
        if level == "Critical":
            insights.append(f"🚨 URGENT: Your organization scores {percentage}% and requires immediate attention to basic security controls.")
        elif level == "Poor":
            insights.append(f"⚠️ WARNING: Your organization scores {percentage}% and has significant security gaps that need addressing.")
        elif level == "Moderate":
            insights.append(f"📊 DEVELOPING: Your organization scores {percentage}% with a moderate security posture that can be enhanced.")
        elif level == "Good":
            insights.append(f"✅ STRONG: Your organization scores {percentage}% with good security practices in place.")
        else:
            insights.append(f"🏆 EXCELLENT: Your organization scores {percentage}% with outstanding security practices.")
        
        # Stage-specific insights
        stages = score_data["stage_scores"]
        weakest_stage = min(stages.items(), key=lambda x: x[1]["percentage"])
        strongest_stage = max(stages.items(), key=lambda x: x[1]["percentage"])
        
        insights.append(f"📉 Weakest area: {weakest_stage[0].replace('_', ' ').title()} ({weakest_stage[1]['percentage']:.1f}%)")
        insights.append(f"📈 Strongest area: {strongest_stage[0].replace('_', ' ').title()} ({strongest_stage[1]['percentage']:.1f}%)")
        
        # Risk area insights
        if risk_areas:
            insights.append(f"🎯 Priority focus: {len(risk_areas)} critical areas need immediate attention")
        
        return insights