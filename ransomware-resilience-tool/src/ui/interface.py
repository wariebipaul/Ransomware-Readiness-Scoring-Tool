"""
Ransomware Resilience Assessment Tool - Console Interface Module

This module provides a rich console-based user interface for the ransomware resilience
assessment tool, featuring interactive menus, progress tracking, and results display.
"""

import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

# Rich console library for enhanced terminal UI
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    from rich.align import Align
    from rich.layout import Layout
    from rich.live import Live
except ImportError:
    # Fallback for basic console operations
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
    
    console = Console()


class RansomwareResilienceInterface:
    """
    Console-based interface for the Ransomware Resilience Assessment Tool.
    
    Provides an interactive command-line interface with rich formatting,
    progress tracking, and comprehensive results display.
    """
    
    def __init__(self):
        """Initialize the console interface."""
        try:
            self.console = Console()
            self.rich_available = True
        except:
            self.console = Console()  # Fallback console
            self.rich_available = False
        
        self.session_data = {
            'start_time': None,
            'organization': '',
            'assessor': '',
            'responses': {},
            'current_stage': 0,
            'progress': 0
        }
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_banner(self):
        """Display the application banner."""
        banner_text = """
        ╔═══════════════════════════════════════════════════════════════╗
        ║                                                               ║
        ║     RANSOMWARE RESILIENCE ASSESSMENT TOOL v2.0               ║
        ║                                                               ║
        ║     Comprehensive Security Readiness Evaluation              ║
        ║     Based on MITRE ATT&CK Framework                          ║
        ║                                                               ║
        ╚═══════════════════════════════════════════════════════════════╝
        """
        
        if self.rich_available:
            self.console.print(Panel(
                Align.center(banner_text),
                style="bold blue",
                border_style="bright_blue"
            ))
        else:
            print(banner_text)
    
    def display_main_menu(self) -> int:
        """
        Display the main menu and get user selection.
        
        Returns:
            int: Selected menu option
        """
        menu_options = [
            "1. Start New Assessment",
            "2. Load Previous Assessment",
            "3. View Framework Information",
            "4. Export Results",
            "5. Help & Documentation",
            "6. Exit"
        ]
        
        if self.rich_available:
            self.console.print("\n[bold cyan]Main Menu[/bold cyan]")
            for option in menu_options:
                self.console.print(f"  {option}")
            
            choice = Prompt.ask(
                "\nSelect an option",
                choices=["1", "2", "3", "4", "5", "6"],
                default="1"
            )
        else:
            print("\nMain Menu:")
            for option in menu_options:
                print(f"  {option}")
            
            while True:
                choice = input("\nSelect an option (1-6): ").strip()
                if choice in ["1", "2", "3", "4", "5", "6"]:
                    break
                print("Invalid choice. Please select 1-6.")
        
        return int(choice)
    
    def collect_session_info(self) -> Dict[str, str]:
        """
        Collect basic session information from the user.
        
        Returns:
            Dict[str, str]: Session information
        """
        self.console.print("\n[bold yellow]Assessment Setup[/bold yellow]")
        
        if self.rich_available:
            organization = Prompt.ask("Organization Name")
            assessor = Prompt.ask("Assessor Name")
            role = Prompt.ask("Your Role/Title", default="IT Manager")
        else:
            organization = input("Organization Name: ").strip()
            assessor = input("Assessor Name: ").strip()
            role = input("Your Role/Title (default: IT Manager): ").strip() or "IT Manager"
        
        session_info = {
            'organization': organization,
            'assessor': assessor,
            'role': role,
            'timestamp': datetime.now().isoformat()
        }
        
        self.session_data.update(session_info)
        return session_info
    
    def display_assessment_stages(self):
        """Display information about the assessment stages."""
        stages_info = """
        The assessment is divided into three critical stages:
        
        🔒 PRE-INFECTION STAGE (Prevention & Preparation)
           • Asset Management & Network Security
           • Access Controls & User Training
           • Backup & Recovery Planning
           • Security Monitoring & Detection
        
        ⚠️  ACTIVE INFECTION STAGE (Response & Containment)
           • Incident Response Procedures
           • Network Isolation & Containment
           • Communication & Decision Making
           • Evidence Collection & Analysis
        
        🔄 POST-INFECTION STAGE (Recovery & Improvement)
           • Recovery & Restoration Procedures
           • Business Continuity Management
           • Lessons Learned & Improvement
           • Stakeholder Communication
        """
        
        if self.rich_available:
            self.console.print(Panel(
                stages_info,
                title="[bold]Assessment Stages Overview[/bold]",
                border_style="green"
            ))
        else:
            print(stages_info)
    
    def display_question_with_progress(self, question_data: Dict, current: int, total: int):
        """
        Display a question with progress information.
        
        Args:
            question_data: Question information
            current: Current question number
            total: Total number of questions
        """
        # Calculate progress percentage
        progress_percent = (current / total) * 100
        
        if self.rich_available:
            # Create progress bar
            progress_bar = "█" * int(progress_percent // 4) + "░" * (25 - int(progress_percent // 4))
            
            self.console.print(f"\n[bold]Question {current} of {total}[/bold]")
            self.console.print(f"Progress: [{progress_bar}] {progress_percent:.1f}%")
            self.console.print(f"Stage: [cyan]{question_data.get('stage', 'Unknown')}[/cyan]")
            self.console.print(f"Category: [yellow]{question_data.get('category', 'General')}[/yellow]")
            
            self.console.print(Panel(
                question_data['question'],
                title="[bold blue]Question[/bold blue]",
                border_style="blue"
            ))
            
            # Display options
            self.console.print("\n[bold]Response Options:[/bold]")
            for i, option in enumerate(question_data['options'], 1):
                self.console.print(f"  {i}. {option}")
        else:
            print(f"\nQuestion {current} of {total} ({progress_percent:.1f}% complete)")
            print(f"Stage: {question_data.get('stage', 'Unknown')}")
            print(f"Category: {question_data.get('category', 'General')}")
            print(f"\n{question_data['question']}")
            print("\nResponse Options:")
            for i, option in enumerate(question_data['options'], 1):
                print(f"  {i}. {option}")
    
    def get_user_response(self, question_data: Dict) -> int:
        """
        Get user response to a question.
        
        Args:
            question_data: Question information
            
        Returns:
            int: Selected option index (0-4)
        """
        max_options = len(question_data['options'])
        valid_choices = [str(i) for i in range(1, max_options + 1)]
        
        if self.rich_available:
            choice = Prompt.ask(
                "\nSelect your response",
                choices=valid_choices,
                show_choices=True
            )
        else:
            while True:
                choice = input(f"\nSelect your response (1-{max_options}): ").strip()
                if choice in valid_choices:
                    break
                print(f"Invalid choice. Please select 1-{max_options}.")
        
        return int(choice) - 1  # Convert to 0-based index
    
    def display_stage_completion(self, stage_name: str, stage_score: float):
        """
        Display stage completion information.
        
        Args:
            stage_name: Name of the completed stage
            stage_score: Score for the completed stage
        """
        completion_msg = f"""
        ✅ {stage_name} Complete!
        
        Stage Score: {stage_score:.1f}%
        """
        
        if self.rich_available:
            self.console.print(Panel(
                Align.center(completion_msg),
                title="[bold green]Stage Complete[/bold green]",
                border_style="green"
            ))
        else:
            print(completion_msg)
        
        # Brief pause for user to see the message
        time.sleep(2)
    
    def display_assessment_results(self, results: Dict[str, Any]):
        """
        Display comprehensive assessment results.
        
        Args:
            results: Assessment results dictionary
        """
        self.clear_screen()
        self.display_banner()
        
        if self.rich_available:
            self.console.print("\n[bold green]🎯 ASSESSMENT RESULTS[/bold green]")
            
            # Overall Score Table
            score_table = Table(title="Overall Readiness Score")
            score_table.add_column("Metric", style="cyan")
            score_table.add_column("Score", style="magenta")
            score_table.add_column("Level", style="green")
            
            # Extract overall assessment data
            overall_assessment = results.get('overall_assessment', {})
            score_table.add_row(
                "Overall Readiness",
                f"{overall_assessment.get('percentage_score', 0):.1f}%",
                overall_assessment.get('readiness_level', 'Unknown')
            )
            
            self.console.print(score_table)
            
            # Stage Breakdown
            stage_table = Table(title="Stage-by-Stage Breakdown")
            stage_table.add_column("Stage", style="cyan")
            stage_table.add_column("Score", style="magenta")
            stage_table.add_column("Status", style="yellow")
            
            # Extract stage performance data
            stage_performance = results.get('stage_performance', {})
            for stage, data in stage_performance.items():
                stage_name = stage.replace('_', ' ').title()
                percentage = data.get('percentage', 0)
                
                # Determine status based on percentage
                if percentage >= 80:
                    status = "Excellent"
                elif percentage >= 70:
                    status = "Good"
                elif percentage >= 60:
                    status = "Moderate"
                elif percentage >= 50:
                    status = "Poor"
                else:
                    status = "Critical"
                
                stage_table.add_row(
                    stage_name,
                    f"{percentage:.1f}%",
                    status
                )
            
            self.console.print(stage_table)
            
        else:
            print("\n🎯 ASSESSMENT RESULTS")
            print("=" * 50)
            
            # Extract overall assessment data
            overall_assessment = results.get('overall_assessment', {})
            print(f"Overall Readiness: {overall_assessment.get('percentage_score', 0):.1f}%")
            print(f"Readiness Level: {overall_assessment.get('readiness_level', 'Unknown')}")
            
            print("\nStage Breakdown:")
            stage_performance = results.get('stage_performance', {})
            for stage, data in stage_performance.items():
                stage_name = stage.replace('_', ' ').title()
                percentage = data.get('percentage', 0)
                
                # Determine status based on percentage
                if percentage >= 80:
                    status = "Excellent"
                elif percentage >= 70:
                    status = "Good"
                elif percentage >= 60:
                    status = "Moderate"
                elif percentage >= 50:
                    status = "Poor"
                else:
                    status = "Critical"
                    
                print(f"  {stage_name}: {percentage:.1f}% - {status}")
    
    def display_recommendations(self, recommendations: List[Dict]):
        """
        Display prioritized recommendations.
        
        Args:
            recommendations: List of recommendation dictionaries
        """
        if self.rich_available:
            self.console.print("\n[bold yellow]📋 PRIORITY RECOMMENDATIONS[/bold yellow]")
            
            for i, rec in enumerate(recommendations[:5], 1):  # Show top 5
                rec_panel = Panel(
                    f"[bold]{rec.get('title', 'Recommendation')}[/bold]\n\n"
                    f"{rec.get('description', 'No description available')}\n\n"
                    f"[cyan]Priority:[/cyan] {rec.get('priority', 'Medium')}\n"
                    f"[green]Timeline:[/green] {rec.get('timeline', 'Not specified')}",
                    title=f"[bold]Recommendation #{i}[/bold]",
                    border_style="yellow"
                )
                self.console.print(rec_panel)
        else:
            print("\n📋 PRIORITY RECOMMENDATIONS")
            print("=" * 50)
            
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"\n{i}. {rec.get('title', 'Recommendation')}")
                print(f"   {rec.get('description', 'No description available')}")
                print(f"   Priority: {rec.get('priority', 'Medium')}")
                print(f"   Timeline: {rec.get('timeline', 'Not specified')}")
    
    def get_export_preferences(self) -> Dict[str, Any]:
        """
        Get user preferences for exporting results.
        
        Returns:
            Dict[str, Any]: Export preferences
        """
        if self.rich_available:
            export_format = Prompt.ask(
                "Export format",
                choices=["pdf", "json", "csv", "txt"],
                default="pdf"
            )
            
            include_details = Confirm.ask("Include detailed analysis?", default=True)
            include_recommendations = Confirm.ask("Include recommendations?", default=True)
            
        else:
            print("\nExport Options:")
            print("1. PDF Report")
            print("2. JSON Data")
            print("3. CSV Summary")
            print("4. Text Report")
            
            while True:
                choice = input("Select format (1-4): ").strip()
                if choice in ["1", "2", "3", "4"]:
                    formats = {"1": "pdf", "2": "json", "3": "csv", "4": "txt"}
                    export_format = formats[choice]
                    break
                print("Invalid choice. Please select 1-4.")
            
            include_details = input("Include detailed analysis? (y/n): ").lower().startswith('y')
            include_recommendations = input("Include recommendations? (y/n): ").lower().startswith('y')
        
        return {
            'format': export_format,
            'include_details': include_details,
            'include_recommendations': include_recommendations,
            'timestamp': datetime.now().isoformat()
        }
    
    def display_help_menu(self):
        """Display help and documentation menu."""
        help_text = """
        📚 HELP & DOCUMENTATION
        
        🔍 About This Assessment:
        This tool evaluates your organization's ransomware resilience across three 
        critical stages using questions based on the MITRE ATT&CK framework.
        
        📊 Scoring System:
        • Questions are weighted by importance and stage
        • Scores range from 0-100% with readiness levels:
          - Critical (0-40%): Immediate action required
          - Basic (41-60%): Significant improvements needed
          - Moderate (61-75%): Good foundation, some gaps
          - Advanced (76-85%): Strong security posture
          - Optimal (86-100%): Excellent ransomware resilience
        
        🎯 Recommendations:
        Based on your responses, you'll receive prioritized recommendations
        aligned with industry frameworks (NIST, ISO 27001, CIS Controls).
        
        💾 Export Options:
        Save your results in multiple formats for sharing and tracking progress.
        
        ❓ Need Help?
        Contact your IT security team or visit the documentation for more details.
        """
        
        if self.rich_available:
            self.console.print(Panel(
                help_text,
                title="[bold blue]Help & Documentation[/bold blue]",
                border_style="blue"
            ))
        else:
            print(help_text)
        
        input("\nPress Enter to continue...")
    
    def confirm_exit(self) -> bool:
        """
        Confirm user wants to exit the application.
        
        Returns:
            bool: True if user confirms exit
        """
        if self.rich_available:
            return Confirm.ask("\nAre you sure you want to exit?")
        else:
            response = input("\nAre you sure you want to exit? (y/n): ").lower()
            return response.startswith('y')
    
    def display_error(self, error_message: str):
        """
        Display an error message to the user.
        
        Args:
            error_message: Error message to display
        """
        if self.rich_available:
            self.console.print(f"[bold red]Error:[/bold red] {error_message}")
        else:
            print(f"Error: {error_message}")
    
    def display_success(self, success_message: str):
        """
        Display a success message to the user.
        
        Args:
            success_message: Success message to display
        """
        if self.rich_available:
            self.console.print(f"[bold green]Success:[/bold green] {success_message}")
        else:
            print(f"Success: {success_message}")


def main():
    """Main function for testing the interface."""
    interface = RansomwareResilienceInterface()
    interface.clear_screen()
    interface.display_banner()
    
    while True:
        choice = interface.display_main_menu()
        
        if choice == 1:
            print("Starting new assessment...")
            break
        elif choice == 5:
            interface.display_help_menu()
        elif choice == 6:
            if interface.confirm_exit():
                break
        else:
            print("Feature not yet implemented in this demo.")
            time.sleep(1)


if __name__ == "__main__":
    main()