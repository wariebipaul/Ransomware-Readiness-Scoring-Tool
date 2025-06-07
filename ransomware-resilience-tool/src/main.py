"""
Ransomware Resilience Assessment Tool - Main Application Entry Point

This is the main entry point for the comprehensive ransomware resilience assessment tool.
It orchestrates the entire assessment process from questionnaire to results and recommendations.
"""

import sys
import os
import traceback
from typing import Dict, Any, Optional
from datetime import datetime

# Import assessment modules
from assessment.questionnaire import Questionnaire
from assessment.scoring import Scoring
from assessment.recommendations import Recommendations
from ui.interface import RansomwareResilienceInterface
from utils.validation import InputValidator

# Import data modules
from data.questions import QUESTIONS
from data.frameworks import MITRE_TECHNIQUES, FRAMEWORKS


class RansomwareResilienceApp:
    """
    Main application class for the Ransomware Resilience Assessment Tool.
    
    Coordinates the assessment process, manages application flow, and handles
    error conditions gracefully.
    """
    
    def __init__(self):
        """Initialize the application."""
        self.interface = RansomwareResilienceInterface()
        self.validator = InputValidator()
        self.session_data = {}
        self.results = {}
        
    def initialize_session(self) -> bool:
        """
        Initialize a new assessment session.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            self.interface.clear_screen()
            self.interface.display_banner()
            
            # Collect session information
            session_info = self.interface.collect_session_info()
            self.session_data.update(session_info)
            self.session_data['start_time'] = datetime.now()
            
            # Display assessment overview
            self.interface.display_assessment_stages()
            
            # Confirm start
            if hasattr(self.interface, 'rich_available') and self.interface.rich_available:
                from rich.prompt import Confirm
                ready = Confirm.ask("\nReady to begin the assessment?", default=True)
            else:
                ready = input("\nReady to begin the assessment? (y/n): ").lower().startswith('y')
            
            if not ready:
                self.interface.console.print("Assessment cancelled.")
                return False
                
            return True
            
        except Exception as e:
            self.interface.display_error(f"Failed to initialize session: {str(e)}")
            return False
    
    def run_assessment(self) -> Optional[Dict[str, Any]]:
        """
        Run the complete assessment questionnaire.
        
        Returns:
            Optional[Dict[str, Any]]: Assessment responses or None if failed
        """
        try:
            # Initialize questionnaire with existing structure
            questionnaire = Questionnaire()
            
            # Run the assessment using the existing method
            self.interface.console.print("\n[bold green]🚀 Starting Assessment...[/bold green]")
            responses = questionnaire.collect_responses()
            
            if not responses:
                self.interface.display_error("Assessment was not completed.")
                return None
            
            # Validate that all responses were collected
            is_valid, validation_message = questionnaire.validate_responses()
            if not is_valid:
                self.interface.display_error(f"Assessment incomplete: {validation_message}")
                return None
            
            self.interface.console.print(f"\n[green]✓ {validation_message}[/green]")
            
            # Store responses in session data
            self.session_data['responses'] = responses
            self.session_data['completion_time'] = datetime.now()
            
            return responses
            
        except KeyboardInterrupt:
            self.interface.console.print("\n[yellow]Assessment interrupted by user.[/yellow]")
            return None
        except Exception as e:
            self.interface.display_error(f"Assessment failed: {str(e)}")
            if "--debug" in sys.argv:
                traceback.print_exc()
            return None
    
    def calculate_scores(self, responses: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Calculate assessment scores and generate analysis.
        
        Args:
            responses: Assessment responses
            
        Returns:
            Optional[Dict[str, Any]]: Scoring results or None if failed
        """
        try:
            # Validate responses structure before scoring
            if not responses or not isinstance(responses, dict):
                raise ValueError("Invalid responses structure")
            
            # Check that we have responses for all expected stages
            expected_stages = ['pre_infection', 'active_infection', 'post_infection']
            for stage in expected_stages:
                if stage not in responses or not responses[stage]:
                    raise ValueError(f"Missing or empty responses for stage: {stage}")
            
            # Initialize scoring engine with current data structure
            scoring_engine = Scoring(
                responses=responses
            )
            
            # Calculate comprehensive scores
            self.interface.console.print("\n[bold blue]📊 Calculating Scores...[/bold blue]")
            
            results = scoring_engine.generate_score_report()
            
            # Store results
            self.results = results
            return results
            
        except Exception as e:
            self.interface.display_error(f"Score calculation failed: {str(e)}")
            if "--debug" in sys.argv:
                traceback.print_exc()
            return None
    
    def generate_recommendations(self, responses: Dict[str, Any], scores: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate actionable recommendations based on assessment results.
        
        Args:
            responses: Assessment responses
            scores: Calculated scores
            
        Returns:
            Optional[Dict[str, Any]]: Recommendations or None if failed
        """
        try:
            # Initialize recommendation engine with current data structure
            rec_engine = Recommendations(
                score_report=scores
            )
            
            self.interface.console.print("\n[bold cyan]🎯 Generating Recommendations...[/bold cyan]")
            
            # Generate recommendations
            rec_engine.generate_recommendations()
            
            recommendations = {
                'priority_actions': rec_engine.get_prioritized_action_plan(),
                'framework_alignment': rec_engine.get_framework_alignment(),
                'executive_summary': rec_engine.generate_executive_summary(),
                'detailed_recommendations': rec_engine.recommendations
            }
            
            return recommendations
            
        except Exception as e:
            self.interface.display_error(f"Recommendation generation failed: {str(e)}")
            if "--debug" in sys.argv:
                traceback.print_exc()
            return None
    
    def display_results(self, scores: Dict[str, Any], recommendations: Dict[str, Any]):
        """
        Display comprehensive assessment results.
        
        Args:
            scores: Assessment scores
            recommendations: Generated recommendations
        """
        try:
            # Display main results
            self.interface.display_assessment_results(scores)
            
            # Display recommendations
            priority_recs = recommendations.get('priority_actions', [])
            self.interface.display_recommendations(priority_recs)
            
            # Offer to view executive summary
            if hasattr(self.interface, 'rich_available') and self.interface.rich_available:
                from rich.prompt import Confirm
                show_summary = Confirm.ask("\nView executive summary?", default=True)
            else:
                show_summary = input("\nView executive summary? (y/n): ").lower().startswith('y')
            
            if show_summary:
                exec_summary = recommendations.get('executive_summary', {})
                self.display_executive_summary(exec_summary)
            
        except Exception as e:
            self.interface.display_error(f"Results display failed: {str(e)}")
    
    def display_executive_summary(self, summary: Dict[str, Any]):
        """
        Display executive summary.
        
        Args:
            summary: Executive summary data
        """
        try:
            if hasattr(self.interface, 'rich_available') and self.interface.rich_available:
                from rich.panel import Panel
                
                summary_text = f"""
[bold]Executive Summary[/bold]

[cyan]Overall Assessment:[/cyan]
{summary.get('overall_assessment', 'Assessment data not available')}

[cyan]Key Findings:[/cyan]
{summary.get('key_findings', 'No key findings available')}

[cyan]Critical Actions:[/cyan]
{summary.get('critical_actions', 'No critical actions identified')}

[cyan]Risk Level:[/cyan] {summary.get('risk_level', 'Unknown')}
[cyan]Investment Priority:[/cyan] {summary.get('investment_priority', 'Not specified')}
                """
                
                self.interface.console.print(Panel(
                    summary_text,
                    title="[bold green]Executive Summary[/bold green]",
                    border_style="green"
                ))
            else:
                print("\n" + "="*60)
                print("EXECUTIVE SUMMARY")
                print("="*60)
                print(f"Overall Assessment: {summary.get('overall_assessment', 'N/A')}")
                print(f"Key Findings: {summary.get('key_findings', 'N/A')}")
                print(f"Critical Actions: {summary.get('critical_actions', 'N/A')}")
                print(f"Risk Level: {summary.get('risk_level', 'Unknown')}")
                print(f"Investment Priority: {summary.get('investment_priority', 'Not specified')}")
                
        except Exception as e:
            self.interface.display_error(f"Executive summary display failed: {str(e)}")
    
    def export_results(self) -> bool:
        """
        Export assessment results based on user preferences.
        
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            # Get export preferences
            export_prefs = self.interface.get_export_preferences()
            
            # For now, just display a message about export
            # In a full implementation, this would create actual files
            export_filename = f"ransomware_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_prefs['format']}"
            
            self.interface.display_success(f"Results would be exported to: {export_filename}")
            
            # TODO: Implement actual export functionality
            # This would involve creating PDF reports, JSON exports, etc.
            
            return True
            
        except Exception as e:
            self.interface.display_error(f"Export failed: {str(e)}")
            return False
    
    def run(self):
        """Main application run loop."""
        try:
            self.interface.clear_screen()
            self.interface.display_banner()
            
            while True:
                choice = self.interface.display_main_menu()
                
                if choice == 1:  # Start New Assessment
                    if self.initialize_session():
                        responses = self.run_assessment()
                        if responses:
                            scores = self.calculate_scores(responses)
                            if scores:
                                recommendations = self.generate_recommendations(responses, scores)
                                if recommendations:
                                    self.display_results(scores, recommendations)
                                    
                                    # Offer export
                                    if hasattr(self.interface, 'rich_available') and self.interface.rich_available:
                                        from rich.prompt import Confirm
                                        do_export = Confirm.ask("\nExport results?", default=True)
                                    else:
                                        do_export = input("\nExport results? (y/n): ").lower().startswith('y')
                                    
                                    if do_export:
                                        self.export_results()
                
                elif choice == 2:  # Load Previous Assessment
                    self.interface.display_error("Load feature not yet implemented.")
                
                elif choice == 3:  # View Framework Information
                    self.display_framework_info()
                
                elif choice == 4:  # Export Results
                    if self.results:
                        self.export_results()
                    else:
                        self.interface.display_error("No assessment results to export. Please complete an assessment first.")
                
                elif choice == 5:  # Help & Documentation
                    self.interface.display_help_menu()
                
                elif choice == 6:  # Exit
                    if self.interface.confirm_exit():
                        self.interface.console.print("\n[bold green]Thank you for using the Ransomware Resilience Assessment Tool![/bold green]")
                        break
        
        except KeyboardInterrupt:
            self.interface.console.print("\n[yellow]Application interrupted by user.[/yellow]")
        except Exception as e:
            self.interface.display_error(f"Application error: {str(e)}")
            if "--debug" in sys.argv:
                traceback.print_exc()
    
    def display_framework_info(self):
        """Display information about cybersecurity frameworks."""
        try:
            framework_info = """
            🔒 CYBERSECURITY FRAMEWORKS REFERENCE
            
            This assessment tool aligns with major cybersecurity frameworks:
            
            • NIST Cybersecurity Framework
            • ISO 27001/27002
            • CIS Critical Security Controls
            • MITRE ATT&CK Framework
            
            The recommendations generated will reference specific controls
            and best practices from these frameworks to help you implement
            effective ransomware defense strategies.
            """
            
            if hasattr(self.interface, 'rich_available') and self.interface.rich_available:
                from rich.panel import Panel
                self.interface.console.print(Panel(
                    framework_info,
                    title="[bold blue]Framework Information[/bold blue]",
                    border_style="blue"
                ))
            else:
                print(framework_info)
                
            input("\nPress Enter to continue...")
            
        except Exception as e:
            self.interface.display_error(f"Framework info display failed: {str(e)}")


def main():
    """Main entry point for the application."""
    try:
        app = RansomwareResilienceApp()
        app.run()
    except Exception as e:
        print(f"Critical application error: {str(e)}")
        if "--debug" in sys.argv:
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()