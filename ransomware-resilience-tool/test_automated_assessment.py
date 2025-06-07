#!/usr/bin/env python3
"""
Automated test to complete a full assessment
"""
import subprocess
import sys

def create_input_sequence():
    """Create input sequence for a complete assessment"""
    inputs = [
        "1",  # Start New Assessment
        "Test Organization",  # Organization name
        "John Doe",  # Assessor name
        "IT Manager",  # Role
        "john@test.com",  # Email
        "y",  # Ready to begin
        # Pre-infection stage (7 questions)
        "2", "2", "2", "2", "2", "2", "2",
        # Active infection stage (4 questions) 
        "2", "2", "2", "2",
        # Post infection stage (4 questions)
        "2", "2", "2", "2",
        "6"  # Exit after completion
    ]
    return "\n".join(inputs) + "\n"

def test_full_assessment():
    """Run a complete assessment test"""
    print("=== Running Full Assessment Test ===")
    
    input_data = create_input_sequence()
    
    try:
        # Run the main application with the input sequence
        process = subprocess.run(
            [sys.executable, "src/main.py"],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=30,
            cwd="/workspaces/Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool"
        )
        
        print("Return code:", process.returncode)
        print("\n--- STDOUT ---")
        print(process.stdout)
        
        if process.stderr:
            print("\n--- STDERR ---")
            print(process.stderr)
            
        # Check if the assessment completed successfully
        if "Readiness Level:" in process.stdout:
            print("\n✅ Assessment completed successfully!")
            return True
        else:
            print("\n❌ Assessment may not have completed properly")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    test_full_assessment()
