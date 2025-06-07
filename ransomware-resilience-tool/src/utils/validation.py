# Input validation utilities for ransomware readiness assessment
import re
from typing import Any, List, Dict, Optional

class InputValidator:
    """Comprehensive input validation for assessment responses"""
    
    def __init__(self):
        self.validation_errors = []
    
    def validate_numeric_choice(self, input_value: str, min_value: int, max_value: int) -> tuple[bool, Optional[int]]:
        """
        Validate numeric choice input (e.g., 1-5 for multiple choice)
        Returns (is_valid, converted_value)
        """
        try:
            # Remove whitespace and convert to int
            choice = int(input_value.strip())
            
            if min_value <= choice <= max_value:
                return True, choice
            else:
                self.validation_errors.append(f"Choice must be between {min_value} and {max_value}")
                return False, None
                
        except ValueError:
            self.validation_errors.append("Please enter a valid number")
            return False, None
    
    def validate_text_input(self, input_value: str, min_length: int = 1, max_length: int = 1000) -> tuple[bool, str]:
        """
        Validate text input with length constraints
        Returns (is_valid, cleaned_value)
        """
        if not isinstance(input_value, str):
            self.validation_errors.append("Input must be text")
            return False, ""
        
        cleaned_value = input_value.strip()
        
        if len(cleaned_value) < min_length:
            self.validation_errors.append(f"Input must be at least {min_length} characters long")
            return False, ""
        
        if len(cleaned_value) > max_length:
            self.validation_errors.append(f"Input must be no more than {max_length} characters long")
            return False, ""
        
        return True, cleaned_value
    
    def validate_email(self, email: str) -> tuple[bool, str]:
        """
        Validate email address format
        Returns (is_valid, cleaned_email)
        """
        if not isinstance(email, str):
            self.validation_errors.append("Email must be text")
            return False, ""
        
        cleaned_email = email.strip().lower()
        
        # Basic email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(email_pattern, cleaned_email):
            return True, cleaned_email
        else:
            self.validation_errors.append("Please enter a valid email address")
            return False, ""
    
    def validate_organization_size(self, size_input: str) -> tuple[bool, str]:
        """
        Validate organization size input
        Returns (is_valid, standardized_size)
        """
        valid_sizes = {
            '1': 'small',
            '2': 'medium', 
            '3': 'large',
            '4': 'enterprise',
            'small': 'small',
            'medium': 'medium',
            'large': 'large',
            'enterprise': 'enterprise'
        }
        
        cleaned_input = size_input.strip().lower()
        
        if cleaned_input in valid_sizes:
            return True, valid_sizes[cleaned_input]
        else:
            self.validation_errors.append("Please select a valid organization size")
            return False, ""
    
    def validate_assessment_responses(self, responses: Dict[str, Dict[str, Any]]) -> tuple[bool, List[str]]:
        """
        Validate complete assessment responses structure
        Returns (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required stages
        required_stages = ['pre_infection', 'active_infection', 'post_infection']
        
        for stage in required_stages:
            if stage not in responses:
                errors.append(f"Missing responses for {stage} stage")
                continue
            
            if not isinstance(responses[stage], dict):
                errors.append(f"Invalid response format for {stage} stage")
                continue
            
            # Validate individual responses in each stage
            for question_id, response_data in responses[stage].items():
                if not self._validate_single_response(question_id, response_data):
                    errors.extend(self.validation_errors)
                    self.validation_errors = []  # Clear for next validation
        
        return len(errors) == 0, errors
    
    def _validate_single_response(self, question_id: str, response_data: Dict[str, Any]) -> bool:
        """Validate a single question response"""
        required_fields = ['value', 'text', 'weight', 'mitre_technique']
        
        for field in required_fields:
            if field not in response_data:
                self.validation_errors.append(f"Missing {field} in response for {question_id}")
                return False
        
        # Validate value is numeric and in range
        if not isinstance(response_data['value'], (int, float)):
            self.validation_errors.append(f"Invalid value type for {question_id}")
            return False
        
        if not (0 <= response_data['value'] <= 4):
            self.validation_errors.append(f"Value out of range for {question_id}")
            return False
        
        # Validate weight
        if not isinstance(response_data['weight'], (int, float)):
            self.validation_errors.append(f"Invalid weight type for {question_id}")
            return False
        
        if response_data['weight'] <= 0:
            self.validation_errors.append(f"Weight must be positive for {question_id}")
            return False
        
        return True
    
    def sanitize_input(self, input_value: str) -> str:
        """
        Sanitize user input to prevent injection attacks
        Returns cleaned input
        """
        if not isinstance(input_value, str):
            return str(input_value)
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '|', '`']
        cleaned = input_value
        
        for char in dangerous_chars:
            cleaned = cleaned.replace(char, '')
        
        # Limit length
        cleaned = cleaned[:500]
        
        return cleaned.strip()
    
    def validate_file_path(self, file_path: str) -> tuple[bool, str]:
        """
        Validate file path for export functionality
        Returns (is_valid, cleaned_path)
        """
        if not isinstance(file_path, str):
            self.validation_errors.append("File path must be text")
            return False, ""
        
        cleaned_path = file_path.strip()
        
        # Check for dangerous path components
        dangerous_patterns = ['..', '~', '$', '|', ';', '&']
        
        for pattern in dangerous_patterns:
            if pattern in cleaned_path:
                self.validation_errors.append("Invalid characters in file path")
                return False, ""
        
        # Check file extension
        valid_extensions = ['.txt', '.json', '.csv', '.pdf']
        if not any(cleaned_path.lower().endswith(ext) for ext in valid_extensions):
            self.validation_errors.append("File must have a valid extension (.txt, .json, .csv, .pdf)")
            return False, ""
        
        return True, cleaned_path
    
    def get_validation_errors(self) -> List[str]:
        """Get list of validation errors"""
        return self.validation_errors.copy()
    
    def clear_validation_errors(self):
        """Clear validation errors"""
        self.validation_errors = []
    
    def has_errors(self) -> bool:
        """Check if there are any validation errors"""
        return len(self.validation_errors) > 0

# Additional utility functions for backward compatibility
def validate_input(input_value, expected_type, valid_options=None):
    """Legacy validation function"""
    validator = InputValidator()
    
    if not isinstance(input_value, expected_type):
        raise ValueError(f"Input must be of type {expected_type.__name__}.")
    
    if valid_options and input_value not in valid_options:
        raise ValueError(f"Input must be one of the following: {valid_options}.")
    
    return True

def validate_yes_no(input_value):
    """Legacy yes/no validation"""
    return validate_input(input_value, str, valid_options=['yes', 'no'])

def validate_score(input_value):
    """Legacy score validation"""
    validate_input(input_value, int)
    if not (0 <= input_value <= 100):
        raise ValueError("Score must be between 0 and 100.")
    return True