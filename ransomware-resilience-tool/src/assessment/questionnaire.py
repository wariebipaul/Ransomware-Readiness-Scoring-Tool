# Questionnaire module for ransomware readiness assessment
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data.questions import QUESTIONS
from utils.validation import InputValidator

class Questionnaire:
    def __init__(self):
        self.questions = QUESTIONS
        self.responses = {}
        self.validator = InputValidator()
        
    def collect_responses(self):
        """
        Main method to collect all user responses through the questionnaire
        Returns a dictionary of responses organized by stage and question ID
        """
        print("\n" + "="*60)
        print("🛡️  RANSOMWARE READINESS ASSESSMENT TOOL")
        print("="*60)
        print("\nThis assessment will evaluate your organization's preparedness")
        print("against ransomware attacks across three key stages:")
        print("• Pre-Infection: Prevention and preparation measures")
        print("• Active Infection: Detection and response capabilities") 
        print("• Post-Infection: Recovery and business continuity")
        print("\nPlease answer all questions honestly for the most accurate assessment.")
        print("-"*60)
        
        self.responses = {
            "pre_infection": {},
            "active_infection": {},
            "post_infection": {}
        }
        
        # Process each stage
        for stage_key, stage_data in self.questions.items():
            self._present_stage(stage_key, stage_data)
            
        return self.responses
    
    def _present_stage(self, stage_key, stage_data):
        """Present questions for a specific stage"""
        print(f"\n{'='*20} {stage_data['title'].upper()} {'='*20}")
        print(f"\n{stage_data['description']}")
        print("-"*60)
        
        for i, question in enumerate(stage_data['questions'], 1):
            self._ask_question(stage_key, question, i, len(stage_data['questions']))
    
    def _ask_question(self, stage_key, question, question_num, total_questions):
        """Ask a single question and collect response"""
        print(f"\nQuestion {question_num}/{total_questions}")
        print(f"📋 {question['question']}")
        print("\nOptions:")
        
        # Display options
        for i, option in enumerate(question['options'], 1):
            print(f"  {i}. {option['text']}")
        
        # Get and validate response
        while True:
            try:
                response = input(f"\nSelect option (1-{len(question['options'])}): ").strip()
                
                if not response:
                    print("❌ Please enter a response.")
                    continue
                    
                choice_index = int(response) - 1
                
                if 0 <= choice_index < len(question['options']):
                    selected_option = question['options'][choice_index]
                    
                    # Store response
                    self.responses[stage_key][question['id']] = {
                        'value': selected_option['value'],
                        'text': selected_option['text'],
                        'weight': question['weight'],
                        'mitre_technique': question['mitre_technique']
                    }
                    
                    print(f"✅ Response recorded: {selected_option['text']}")
                    break
                else:
                    print(f"❌ Please enter a number between 1 and {len(question['options'])}")
                    
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\n❌ Assessment cancelled by user.")
                sys.exit(0)
    
    def get_response_summary(self):
        """Get a summary of all responses"""
        summary = {}
        
        for stage_key, stage_responses in self.responses.items():
            stage_title = self.questions[stage_key]['title']
            summary[stage_title] = {}
            
            for question_id, response in stage_responses.items():
                # Find the question text
                question_text = None
                for question in self.questions[stage_key]['questions']:
                    if question['id'] == question_id:
                        question_text = question['question']
                        break
                
                summary[stage_title][question_text] = response['text']
        
        return summary
    
    def display_progress(self, current_stage, current_question, total_questions):
        """Display progress indicator"""
        progress = (current_question / total_questions) * 100
        print(f"\n📊 Progress: {progress:.1f}% complete")
    
    def validate_responses(self):
        """Validate that all required responses have been collected"""
        for stage_key, stage_data in self.questions.items():
            if stage_key not in self.responses:
                return False, f"Missing responses for {stage_data['title']}"
                
            for question in stage_data['questions']:
                if question['id'] not in self.responses[stage_key]:
                    return False, f"Missing response for question: {question['question']}"
        
        return True, "All responses collected successfully"