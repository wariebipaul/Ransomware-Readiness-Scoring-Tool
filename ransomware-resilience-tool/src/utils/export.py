"""
Ransomware Resilience Assessment Tool - Export Utilities

This module provides functionality to export assessment results in various formats
including PDF reports, JSON data, CSV summaries, and text reports.
"""

import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class AssessmentExporter:
    """
    Utility class for exporting assessment results in multiple formats.
    
    Supports PDF reports, JSON data exports, CSV summaries, and text reports
    with comprehensive formatting and customization options.
    """
    
    def __init__(self, session_data: Dict[str, Any], results: Dict[str, Any], 
                 recommendations: Dict[str, Any]):
        """
        Initialize the exporter with assessment data.
        
        Args:
            session_data: Session information and metadata
            results: Assessment scores and analysis
            recommendations: Generated recommendations
        """
        self.session_data = session_data
        self.results = results
        self.recommendations = recommendations
        self.export_timestamp = datetime.now()
    
    def export_to_json(self, filepath: str, include_details: bool = True) -> bool:
        """
        Export assessment data to JSON format.
        
        Args:
            filepath: Output file path
            include_details: Whether to include detailed analysis
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            export_data = {
                'metadata': {
                    'export_timestamp': self.export_timestamp.isoformat(),
                    'tool_version': '2.0',
                    'format_version': '1.0'
                },
                'session_info': self.session_data,
                'results': self.results
            }
            
            if include_details:
                export_data['recommendations'] = self.recommendations
            else:
                # Include only summary recommendations
                export_data['recommendations'] = {
                    'priority_actions': self.recommendations.get('priority_actions', [])[:5]
                }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"JSON export failed: {str(e)}")
            return False
    
    def export_to_csv(self, filepath: str) -> bool:
        """
        Export assessment summary to CSV format.
        
        Args:
            filepath: Output file path
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Header information
                writer.writerow(['Ransomware Resilience Assessment Report'])
                writer.writerow(['Generated:', self.export_timestamp.strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow(['Organization:', self.session_data.get('organization', 'N/A')])
                writer.writerow(['Assessor:', self.session_data.get('assessor', 'N/A')])
                writer.writerow([])
                
                # Overall scores
                writer.writerow(['Overall Results'])
                writer.writerow(['Metric', 'Score', 'Level'])
                writer.writerow([
                    'Overall Readiness',
                    f"{self.results.get('overall_score', 0):.1f}%",
                    self.results.get('readiness_level', 'Unknown')
                ])
                writer.writerow([])
                
                # Stage breakdown
                writer.writerow(['Stage Breakdown'])
                writer.writerow(['Stage', 'Score', 'Status'])
                
                for stage, data in self.results.get('stage_scores', {}).items():
                    writer.writerow([
                        stage,
                        f"{data.get('score', 0):.1f}%",
                        data.get('status', 'Unknown')
                    ])
                
                writer.writerow([])
                
                # Priority recommendations
                writer.writerow(['Priority Recommendations'])
                writer.writerow(['Priority', 'Title', 'Timeline', 'Category'])
                
                priority_recs = self.recommendations.get('priority_actions', [])
                for rec in priority_recs[:10]:  # Top 10 recommendations
                    writer.writerow([
                        rec.get('priority', 'Medium'),
                        rec.get('title', 'No title'),
                        rec.get('timeline', 'Not specified'),
                        rec.get('category', 'General')
                    ])
            
            return True
            
        except Exception as e:
            print(f"CSV export failed: {str(e)}")
            return False
    
    def export_to_text(self, filepath: str, include_details: bool = True) -> bool:
        """
        Export assessment to formatted text report.
        
        Args:
            filepath: Output file path
            include_details: Whether to include detailed analysis
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                # Header
                f.write("=" * 80 + "\n")
                f.write("RANSOMWARE RESILIENCE ASSESSMENT REPORT\n")
                f.write("=" * 80 + "\n\n")
                
                # Session information
                f.write("ASSESSMENT INFORMATION\n")
                f.write("-" * 40 + "\n")
                f.write(f"Organization: {self.session_data.get('organization', 'N/A')}\n")
                f.write(f"Assessor: {self.session_data.get('assessor', 'N/A')}\n")
                f.write(f"Assessment Date: {self.session_data.get('start_time', 'N/A')}\n")
                f.write(f"Report Generated: {self.export_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Overall results
                f.write("OVERALL RESULTS\n")
                f.write("-" * 40 + "\n")
                f.write(f"Overall Readiness Score: {self.results.get('overall_score', 0):.1f}%\n")
                f.write(f"Readiness Level: {self.results.get('readiness_level', 'Unknown')}\n\n")
                
                # Stage breakdown
                f.write("STAGE-BY-STAGE BREAKDOWN\n")
                f.write("-" * 40 + "\n")
                for stage, data in self.results.get('stage_scores', {}).items():
                    f.write(f"{stage}: {data.get('score', 0):.1f}% - {data.get('status', 'Unknown')}\n")
                f.write("\n")
                
                if include_details:
                    # Risk analysis
                    risk_analysis = self.results.get('risk_analysis', {})
                    if risk_analysis:
                        f.write("RISK ANALYSIS\n")
                        f.write("-" * 40 + "\n")
                        f.write(f"Critical Gaps: {len(risk_analysis.get('critical_gaps', []))}\n")
                        f.write(f"High Priority Areas: {len(risk_analysis.get('high_priority', []))}\n")
                        f.write(f"Medium Priority Areas: {len(risk_analysis.get('medium_priority', []))}\n\n")
                    
                    # Strengths
                    strengths = self.results.get('strength_analysis', {})
                    if strengths:
                        f.write("STRENGTH ANALYSIS\n")
                        f.write("-" * 40 + "\n")
                        for strength in strengths.get('identified_strengths', [])[:5]:
                            f.write(f"• {strength}\n")
                        f.write("\n")
                
                # Priority recommendations
                f.write("PRIORITY RECOMMENDATIONS\n")
                f.write("-" * 40 + "\n")
                priority_recs = self.recommendations.get('priority_actions', [])
                for i, rec in enumerate(priority_recs[:10], 1):
                    f.write(f"{i}. {rec.get('title', 'No title')}\n")
                    f.write(f"   Priority: {rec.get('priority', 'Medium')}\n")
                    f.write(f"   Timeline: {rec.get('timeline', 'Not specified')}\n")
                    if include_details and rec.get('description'):
                        f.write(f"   Description: {rec.get('description')}\n")
                    f.write("\n")
                
                if include_details:
                    # Executive summary
                    exec_summary = self.recommendations.get('executive_summary', {})
                    if exec_summary:
                        f.write("EXECUTIVE SUMMARY\n")
                        f.write("-" * 40 + "\n")
                        f.write(f"Overall Assessment: {exec_summary.get('overall_assessment', 'N/A')}\n\n")
                        f.write(f"Key Findings: {exec_summary.get('key_findings', 'N/A')}\n\n")
                        f.write(f"Critical Actions: {exec_summary.get('critical_actions', 'N/A')}\n\n")
                
                # Footer
                f.write("=" * 80 + "\n")
                f.write("End of Report\n")
                f.write("Generated by Ransomware Resilience Assessment Tool v2.0\n")
                f.write("=" * 80 + "\n")
            
            return True
            
        except Exception as e:
            print(f"Text export failed: {str(e)}")
            return False
    
    def export_assessment(self, export_format: str, include_details: bool = True, 
                         include_recommendations: bool = True, 
                         output_dir: Optional[str] = None) -> Optional[str]:
        """
        Export assessment in specified format.
        
        Args:
            export_format: Format to export ('json', 'csv', 'txt')
            include_details: Whether to include detailed analysis
            include_recommendations: Whether to include recommendations
            output_dir: Output directory (optional)
            
        Returns:
            Optional[str]: Path to exported file or None if failed
        """
        try:
            # Create output directory
            if output_dir is None:
                output_dir = "exports"
                os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename
            org_name = self.session_data.get('organization', 'unknown').replace(' ', '_')
            timestamp = self.export_timestamp.strftime("%Y%m%d_%H%M%S")
            filename = f"ransomware_assessment_{org_name}_{timestamp}.{export_format}"
            filepath = os.path.join(output_dir, filename)
            
            # Filter recommendations if needed
            if not include_recommendations:
                self.recommendations = {'priority_actions': []}
            
            # Export based on format
            success = False
            if export_format.lower() == 'json':
                success = self.export_to_json(filepath, include_details)
            elif export_format.lower() == 'csv':
                success = self.export_to_csv(filepath)
            elif export_format.lower() == 'txt':
                success = self.export_to_text(filepath, include_details)
            else:
                print(f"Unsupported export format: {export_format}")
                return None
            
            if success:
                return filepath
            else:
                return None
                
        except Exception as e:
            print(f"Export failed: {str(e)}")
            return None


# Legacy functions for backward compatibility
def export_to_csv(data, filename):
    """Legacy CSV export function for backward compatibility."""
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data.keys())  # Write header
            writer.writerow(data.values())  # Write data
    except Exception as e:
        print(f"Legacy CSV export failed: {str(e)}")


def export_to_json(data, filename):
    """Legacy JSON export function for backward compatibility."""
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)
    except Exception as e:
        print(f"Legacy JSON export failed: {str(e)}")


def main():
    """Demo function for testing export functionality."""
    # Sample data for testing
    sample_session = {
        'organization': 'Sample Corp',
        'assessor': 'John Doe',
        'start_time': datetime.now(),
        'responses': {}
    }
    
    sample_results = {
        'overall_score': 75.5,
        'readiness_level': 'Moderate',
        'stage_scores': {
            'Pre-Infection': {'score': 80.0, 'status': 'Good'},
            'Active Infection': {'score': 70.0, 'status': 'Moderate'},
            'Post-Infection': {'score': 76.0, 'status': 'Good'}
        }
    }
    
    sample_recommendations = {
        'priority_actions': [
            {
                'title': 'Implement Multi-Factor Authentication',
                'priority': 'High',
                'timeline': '30 days',
                'description': 'Deploy MFA across all critical systems'
            }
        ]
    }
    
    # Test export
    exporter = AssessmentExporter(sample_session, sample_results, sample_recommendations)
    
    # Test all formats
    for fmt in ['json', 'csv', 'txt']:
        result = exporter.export_assessment(fmt)
        if result:
            print(f"Successfully exported to: {result}")
        else:
            print(f"Failed to export {fmt} format")


if __name__ == "__main__":
    main()