# Recommendations module for ransomware readiness assessment
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data.frameworks import RECOMMENDATION_TEMPLATES, MITRE_TECHNIQUES

class Recommendations:
    def __init__(self, score_report=None):
        self.score_report = score_report or {}
        self.recommendations = {}
        
    def generate_recommendations(self, score_report=None):
        """
        Generate comprehensive, prioritized recommendations based on assessment results
        """
        if score_report:
            self.score_report = score_report
            
        self.recommendations = {
            "immediate_actions": [],
            "short_term": [],
            "medium_term": [],
            "long_term": [],
            "best_practices": []
        }
        
        # Generate recommendations based on overall score
        self._generate_overall_recommendations()
        
        # Generate specific recommendations for risk areas
        self._generate_risk_based_recommendations()
        
        # Generate MITRE ATT&CK specific recommendations
        self._generate_mitre_recommendations()
        
        # Generate stage-specific recommendations
        self._generate_stage_recommendations()
        
        return self.recommendations
    
    def _generate_overall_recommendations(self):
        """Generate recommendations based on overall readiness level"""
        if not self.score_report.get("overall_assessment"):
            return
            
        level = self.score_report["overall_assessment"]["readiness_level"].lower()
        percentage = self.score_report["overall_assessment"]["percentage_score"]
        
        if level == "critical":
            self.recommendations["immediate_actions"].extend([
                "🚨 CRITICAL: Implement basic data backup procedures immediately",
                "🚨 CRITICAL: Establish incident response team and basic procedures",
                "🚨 CRITICAL: Deploy basic endpoint protection on all systems",
                "🚨 CRITICAL: Create network inventory and implement basic segmentation"
            ])
            
        elif level == "poor":
            self.recommendations["immediate_actions"].extend([
                "⚠️ HIGH PRIORITY: Review and enhance existing backup strategies",
                "⚠️ HIGH PRIORITY: Develop comprehensive incident response plan",
                "⚠️ HIGH PRIORITY: Implement employee security awareness training"
            ])
            
        elif level == "moderate":
            self.recommendations["short_term"].extend([
                "📈 ENHANCE: Test and validate backup and recovery procedures",
                "📈 ENHANCE: Implement advanced threat detection capabilities",
                "📈 ENHANCE: Conduct regular security assessments"
            ])
            
        elif level == "good":
            self.recommendations["medium_term"].extend([
                "🔧 OPTIMIZE: Implement zero-trust architecture principles",
                "🔧 OPTIMIZE: Deploy advanced threat hunting capabilities",
                "🔧 OPTIMIZE: Enhance automation in incident response"
            ])
            
        else:  # excellent
            self.recommendations["best_practices"].extend([
                "🏆 MAINTAIN: Continue current excellent practices",
                "🏆 MAINTAIN: Share best practices with industry peers",
                "🏆 MAINTAIN: Consider becoming a cybersecurity mentor organization"
            ])
    
    def _generate_risk_based_recommendations(self):
        """Generate specific recommendations for identified risk areas"""
        risk_areas = self.score_report.get("risk_areas", [])
        
        for risk in risk_areas[:3]:  # Focus on top 3 risks
            question_id = risk["question_id"]
            percentage = risk["percentage"]
            stage = risk["stage"]
            
            # Map question IDs to specific recommendations
            if question_id == "backup_strategy":
                if percentage < 25:
                    self.recommendations["immediate_actions"].append(
                        "💾 BACKUP: Implement automated daily backups with 3-2-1 strategy"
                    )
                else:
                    self.recommendations["short_term"].append(
                        "💾 BACKUP: Enhance backup testing and validation procedures"
                    )
                    
            elif question_id == "incident_response_plan":
                if percentage < 25:
                    self.recommendations["immediate_actions"].append(
                        "📋 INCIDENT RESPONSE: Create documented incident response procedures"
                    )
                else:
                    self.recommendations["short_term"].append(
                        "📋 INCIDENT RESPONSE: Conduct tabletop exercises and plan testing"
                    )
                    
            elif question_id == "network_segmentation":
                if percentage < 25:
                    self.recommendations["immediate_actions"].append(
                        "🔒 NETWORK: Implement basic network segmentation and access controls"
                    )
                else:
                    self.recommendations["medium_term"].append(
                        "🔒 NETWORK: Deploy micro-segmentation and zero-trust principles"
                    )
                    
            elif question_id == "endpoint_protection":
                if percentage < 25:
                    self.recommendations["immediate_actions"].append(
                        "🛡️ ENDPOINT: Deploy next-generation antivirus on all endpoints"
                    )
                else:
                    self.recommendations["short_term"].append(
                        "🛡️ ENDPOINT: Implement EDR/XDR solutions with threat hunting"
                    )
    
    def _generate_mitre_recommendations(self):
        """Generate recommendations based on MITRE ATT&CK technique coverage"""
        mitre_coverage = self.score_report.get("mitre_coverage", {})
        
        for technique, data in mitre_coverage.items():
            if data["percentage"] < 50:  # Poor coverage
                technique_info = data.get("technique_info", {})
                technique_name = technique_info.get("name", technique)
                
                if technique == "T1566":  # Phishing
                    self.recommendations["short_term"].append(
                        f"📧 ANTI-PHISHING: Implement advanced email security and user training for {technique_name}"
                    )
                elif technique == "T1490":  # Inhibit System Recovery
                    self.recommendations["immediate_actions"].append(
                        f"🔄 RECOVERY: Strengthen backup and recovery capabilities against {technique_name}"
                    )
                elif technique == "T1486":  # Data Encrypted for Impact
                    self.recommendations["short_term"].append(
                        f"🔐 PROTECTION: Implement file integrity monitoring and backup protection against {technique_name}"
                    )
    
    def _generate_stage_recommendations(self):
        """Generate recommendations based on stage performance"""
        stages = self.score_report.get("stage_performance", {})
        
        for stage_key, stage_data in stages.items():
            if stage_data["percentage"] < 60:  # Below good threshold
                stage_name = stage_key.replace("_", " ").title()
                
                if stage_key == "pre_infection":
                    self.recommendations["short_term"].append(
                        f"🛡️ PREVENTION: Strengthen {stage_name} controls including backups, patching, and training"
                    )
                elif stage_key == "active_infection":
                    self.recommendations["short_term"].append(
                        f"🔍 DETECTION: Improve {stage_name} capabilities with monitoring and response procedures"
                    )
                elif stage_key == "post_infection":
                    self.recommendations["medium_term"].append(
                        f"🔄 RECOVERY: Enhance {stage_name} planning including business continuity and forensics"
                    )
    
    def get_prioritized_action_plan(self):
        """Generate a prioritized 30-60-90 day action plan"""
        action_plan = {
            "30_days": {
                "title": "Immediate Actions (Next 30 Days)",
                "actions": self.recommendations.get("immediate_actions", [])[:5]
            },
            "60_days": {
                "title": "Short-term Improvements (Next 60 Days)", 
                "actions": self.recommendations.get("short_term", [])[:5]
            },
            "90_days": {
                "title": "Medium-term Enhancements (Next 90 Days)",
                "actions": self.recommendations.get("medium_term", [])[:5]
            }
        }
        
        return action_plan
    
    def get_framework_alignment(self):
        """Map recommendations to cybersecurity frameworks"""
        framework_mapping = {
            "NIST_CSF": {
                "IDENTIFY": [],
                "PROTECT": [],
                "DETECT": [],
                "RESPOND": [],
                "RECOVER": []
            }
        }
        
        # Map recommendations to NIST CSF functions
        all_recommendations = (
            self.recommendations.get("immediate_actions", []) +
            self.recommendations.get("short_term", []) +
            self.recommendations.get("medium_term", [])
        )
        
        for rec in all_recommendations:
            if "backup" in rec.lower() or "recovery" in rec.lower():
                framework_mapping["NIST_CSF"]["RECOVER"].append(rec)
            elif "monitor" in rec.lower() or "detect" in rec.lower():
                framework_mapping["NIST_CSF"]["DETECT"].append(rec)
            elif "incident" in rec.lower() or "response" in rec.lower():
                framework_mapping["NIST_CSF"]["RESPOND"].append(rec)
            elif "segment" in rec.lower() or "protection" in rec.lower():
                framework_mapping["NIST_CSF"]["PROTECT"].append(rec)
            else:
                framework_mapping["NIST_CSF"]["IDENTIFY"].append(rec)
        
        return framework_mapping
    
    def generate_executive_summary(self):
        """Generate executive summary of recommendations"""
        risk_areas = self.score_report.get("risk_areas", [])
        overall_score = self.score_report.get("overall_assessment", {}).get("percentage_score", 0)
        readiness_level = self.score_report.get("overall_assessment", {}).get("readiness_level", "Unknown")
        
        summary = {
            "overall_risk": readiness_level,
            "score": f"{overall_score}%",
            "critical_areas": len([r for r in risk_areas if r["percentage"] < 25]),
            "immediate_actions_needed": len(self.recommendations.get("immediate_actions", [])),
            "investment_priority": self._determine_investment_priority(),
            "timeline": "30-90 days for critical improvements"
        }
        
        return summary
    
    def _determine_investment_priority(self):
        """Determine investment priority based on assessment"""
        overall_score = self.score_report.get("overall_assessment", {}).get("percentage_score", 0)
        
        if overall_score < 40:
            return "HIGH - Immediate investment required"
        elif overall_score < 70:
            return "MEDIUM - Planned investment recommended"
        else:
            return "LOW - Maintain current investment levels"