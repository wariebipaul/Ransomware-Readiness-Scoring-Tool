/**
 * Ransomware Resilience Assessment Tool - Web Application JavaScript
 * Handles interactive features, AJAX requests, and UI enhancements
 */

// Global variables
let assessmentData = {
    responses: {},
    progress: 0,
    currentStage: 0
};

// Utility functions
const utils = {
    /**
     * Show loading spinner
     */
    showLoading: function(element) {
        if (element) {
            element.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
            element.disabled = true;
        }
    },

    /**
     * Hide loading spinner
     */
    hideLoading: function(element, originalText) {
        if (element) {
            element.innerHTML = originalText;
            element.disabled = false;
        }
    },

    /**
     * Show toast notification
     */
    showToast: function(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container') || this.createToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast after it's hidden
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    },

    /**
     * Create toast container if it doesn't exist
     */
    createToastContainer: function() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '1080';
        document.body.appendChild(container);
        return container;
    },

    /**
     * Debounce function
     */
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func(...args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func(...args);
        };
    },

    /**
     * Format percentage
     */
    formatPercentage: function(value) {
        return Math.round(value * 10) / 10 + '%';
    },

    /**
     * Animate number counting
     */
    animateNumber: function(element, start, end, duration = 1000) {
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
                current = end;
                clearInterval(timer);
            }
            element.textContent = Math.round(current * 10) / 10;
        }, 16);
    }
};

// Session management
const sessionManager = {
    /**
     * Check if there's an active session
     */
    checkActiveSession: function() {
        return fetch('/api/session-status')
            .then(response => response.json())
            .then(data => data.session_active)
            .catch(() => false);
    },

    /**
     * Get session data
     */
    getSessionData: function() {
        return fetch('/api/session-status')
            .then(response => response.json())
            .catch(() => ({}));
    },

    /**
     * Update session display
     */
    updateSessionDisplay: function(data) {
        const sessionStatus = document.getElementById('session-status');
        if (sessionStatus && data.session_active) {
            document.getElementById('session-org').textContent = data.organization || '';
            document.getElementById('session-assessor').textContent = data.assessor || '';
            
            const progressBar = document.getElementById('session-progress');
            const progressText = document.getElementById('session-progress-text');
            
            if (progressBar && progressText) {
                progressBar.style.width = data.progress + '%';
                progressText.textContent = Math.round(data.progress) + '%';
            }
            
            sessionStatus.style.display = 'block';
        }
    }
};

// Form validation
const formValidator = {
    /**
     * Validate required fields
     */
    validateRequired: function(form) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });
        
        return isValid;
    },

    /**
     * Add real-time validation
     */
    addRealTimeValidation: function(form) {
        const fields = form.querySelectorAll('input, select, textarea');
        
        fields.forEach(field => {
            field.addEventListener('blur', () => {
                if (field.hasAttribute('required') && !field.value.trim()) {
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            field.addEventListener('input', () => {
                if (field.classList.contains('is-invalid') && field.value.trim()) {
                    field.classList.remove('is-invalid');
                }
            });
        });
    }
};

// Assessment management
const assessmentManager = {
    /**
     * Save response to server
     */
    saveResponse: function(stage, questionId, responseData) {
        return fetch('/api/save-response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                stage: stage,
                question_id: questionId,
                response_data: responseData
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.updateProgress(data.progress);
                if (data.completed) {
                    this.showCompletionMessage();
                }
                utils.showToast('Response saved successfully', 'success');
            } else {
                throw new Error(data.error || 'Failed to save response');
            }
            return data;
        })
        .catch(error => {
            console.error('Error saving response:', error);
            utils.showToast('Error saving response: ' + error.message, 'danger');
            throw error;
        });
    },

    /**
     * Update progress display
     */
    updateProgress: function(progress) {
        assessmentData.progress = progress;
        
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        
        if (progressBar) {
            progressBar.style.width = progress + '%';
            progressBar.setAttribute('aria-valuenow', progress);
        }
        
        if (progressText) {
            progressText.textContent = Math.round(progress) + '%';
        }
        
        // Update stage progress indicators
        this.updateStageProgress();
    },

    /**
     * Update stage progress indicators
     */
    updateStageProgress: function() {
        const stages = ['pre_infection', 'active_infection', 'post_infection'];
        
        stages.forEach(stage => {
            const stageElement = document.getElementById(`stage-progress-${stage}`);
            if (stageElement) {
                const stageQuestions = document.querySelectorAll(`[data-stage="${stage}"] .answer-radio`);
                const uniqueQuestions = new Set();
                
                stageQuestions.forEach(radio => {
                    uniqueQuestions.add(radio.dataset.question);
                });
                
                let completed = 0;
                uniqueQuestions.forEach(questionId => {
                    const checkedRadio = document.querySelector(
                        `input[name="question-${stage}-${questionId}"]:checked`
                    );
                    if (checkedRadio) completed++;
                });
                
                stageElement.textContent = `${completed}/${uniqueQuestions.size}`;
            }
        });
    },

    /**
     * Show completion message
     */
    showCompletionMessage: function() {
        const resultsBtn = document.getElementById('view-results-btn');
        if (resultsBtn) {
            resultsBtn.style.display = 'inline-block';
            resultsBtn.classList.add('btn-pulse');
        }
        
        utils.showToast('Assessment completed! You can now view your results.', 'success');
    },

    /**
     * Auto-save functionality
     */
    setupAutoSave: function() {
        const saveResponse = utils.debounce((stage, questionId, responseData) => {
            this.saveResponse(stage, questionId, responseData);
        }, 1000);

        // Set up auto-save for radio buttons
        document.querySelectorAll('.answer-radio').forEach(radio => {
            radio.addEventListener('change', function() {
                const responseData = {
                    score: parseInt(this.value),
                    answer_text: this.nextElementSibling.textContent.trim(),
                    timestamp: new Date().toISOString()
                };
                
                saveResponse(this.dataset.stage, this.dataset.question, responseData);
                
                // Mark question as completed
                const questionItem = this.closest('.question-item');
                const statusIcon = questionItem.querySelector('.question-completed');
                if (statusIcon) {
                    statusIcon.style.display = 'inline';
                }
            });
        });

        // Set up auto-save for comments
        document.querySelectorAll('.question-comments').forEach(textarea => {
            textarea.addEventListener('blur', function() {
                if (this.value.trim()) {
                    const stage = this.dataset.stage;
                    const questionId = this.dataset.question;
                    
                    // Get existing response data
                    const existingRadio = document.querySelector(
                        `input[name="question-${stage}-${questionId}"]:checked`
                    );
                    
                    if (existingRadio) {
                        const responseData = {
                            score: parseInt(existingRadio.value),
                            answer_text: existingRadio.nextElementSibling.textContent.trim(),
                            comments: this.value.trim(),
                            timestamp: new Date().toISOString()
                        };
                        
                        this.saveResponse(stage, questionId, responseData);
                    }
                }
            });
        });
    }
};

// Export functionality
const exportManager = {
    /**
     * Export results in specified format
     */
    exportResults: function(format) {
        const button = event.target;
        const originalText = button.innerHTML;
        
        utils.showLoading(button);
        
        fetch(`/api/export/${format}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.downloadFile(data.data, `ransomware_assessment_results.${format}`, format);
                    utils.showToast(`Results exported successfully as ${format.toUpperCase()}`, 'success');
                } else {
                    throw new Error(data.error || 'Export failed');
                }
            })
            .catch(error => {
                console.error('Export error:', error);
                utils.showToast('Error exporting results: ' + error.message, 'danger');
            })
            .finally(() => {
                utils.hideLoading(button, originalText);
            });
    },

    /**
     * Download file
     */
    downloadFile: function(data, filename, format) {
        const mimeTypes = {
            'json': 'application/json',
            'csv': 'text/csv',
            'txt': 'text/plain'
        };
        
        const blob = new Blob([data], { type: mimeTypes[format] || 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }
};

// Chart management
const chartManager = {
    /**
     * Initialize all charts
     */
    initializeCharts: function() {
        this.initStageChart();
        this.initMitreChart();
    },

    /**
     * Initialize stage performance chart
     */
    initStageChart: function() {
        const canvas = document.getElementById('stageChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        
        // Get data from page
        const stageData = this.getStageData();
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(stageData).map(key => 
                    key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
                ),
                datasets: [{
                    label: 'Score Percentage',
                    data: Object.values(stageData).map(stage => stage.percentage),
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(255, 205, 86, 0.8)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 205, 86, 1)'
                    ],
                    borderWidth: 1,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.parsed.y + '%';
                            }
                        }
                    }
                }
            }
        });
    },

    /**
     * Initialize MITRE coverage chart
     */
    initMitreChart: function() {
        const canvas = document.getElementById('mitreChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        
        // Get data from page
        const mitreData = this.getMitreData();
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Covered', 'Not Covered'],
                datasets: [{
                    data: [
                        mitreData.coverage_percentage,
                        100 - mitreData.coverage_percentage
                    ],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.8)',
                        'rgba(220, 53, 69, 0.8)'
                    ],
                    borderColor: [
                        'rgba(40, 167, 69, 1)',
                        'rgba(220, 53, 69, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed + '%';
                            }
                        }
                    }
                }
            }
        });
    },

    /**
     * Get stage data from page
     */
    getStageData: function() {
        // Try to get data from a global variable or data attribute
        if (typeof stageData !== 'undefined') {
            return stageData;
        }
        
        // Fallback to default data
        return {
            pre_infection: { percentage: 0 },
            active_infection: { percentage: 0 },
            post_infection: { percentage: 0 }
        };
    },

    /**
     * Get MITRE data from page
     */
    getMitreData: function() {
        // Try to get data from a global variable or data attribute
        if (typeof mitreData !== 'undefined') {
            return mitreData;
        }
        
        // Fallback to default data
        return {
            coverage_percentage: 0,
            techniques_covered: 0
        };
    }
};

// Theme management
const themeManager = {
    /**
     * Initialize theme
     */
    init: function() {
        this.applyTheme();
        this.setupThemeToggle();
    },

    /**
     * Apply current theme
     */
    applyTheme: function() {
        const theme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', theme);
    },

    /**
     * Setup theme toggle functionality
     */
    setupThemeToggle: function() {
        const toggleButton = document.getElementById('theme-toggle');
        if (toggleButton) {
            toggleButton.addEventListener('click', this.toggleTheme.bind(this));
        }
    },

    /**
     * Toggle between light and dark themes
     */
    toggleTheme: function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    }
};

// PDF Export and Printing Functions
const reportGenerator = {
    /**
     * Export assessment results to PDF
     */
    exportToPDF: function() {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        
        // Get assessment data from the page
        const orgName = document.querySelector('.text-muted')?.textContent?.split(' | ')[0] || 'Organization';
        const assessor = document.querySelector('.text-muted')?.textContent?.split(' | ')[1] || 'Assessor';
        const overallScore = document.querySelector('.score-display')?.textContent || '0%';
        const readinessLevel = document.querySelector('.readiness-badge')?.textContent || 'Unknown';
        
        // PDF Header
        doc.setFontSize(20);
        doc.setTextColor(40, 116, 166); // Primary blue color
        doc.text('Ransomware Resilience Assessment Report', 20, 30);
        
        // Organization info
        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);
        doc.text(`Organization: ${orgName}`, 20, 50);
        doc.text(`Assessed by: ${assessor}`, 20, 60);
        doc.text(`Report Date: ${new Date().toLocaleDateString()}`, 20, 70);
        
        // Overall Score section
        doc.setFontSize(16);
        doc.setTextColor(40, 116, 166);
        doc.text('Overall Assessment Results', 20, 90);
        
        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);
        doc.text(`Overall Readiness Score: ${overallScore}`, 20, 110);
        doc.text(`Readiness Level: ${readinessLevel}`, 20, 120);
        
        // Stage Performance section
        const stageRows = document.querySelectorAll('#stageTable tbody tr');
        if (stageRows.length > 0) {
            doc.setFontSize(16);
            doc.setTextColor(40, 116, 166);
            doc.text('Stage Performance Breakdown', 20, 150);
            
            let yPos = 170;
            doc.setFontSize(10);
            doc.setTextColor(0, 0, 0);
            
            stageRows.forEach((row, index) => {
                const cells = row.querySelectorAll('td');
                if (cells.length >= 4) {
                    const stageName = cells[0].textContent.trim();
                    const stageScore = cells[1].textContent.trim();
                    const questionsAnswered = cells[2].textContent.trim();
                    const status = cells[4].textContent.trim();
                    
                    doc.text(`${stageName}: ${stageScore} (${questionsAnswered} questions) - ${status}`, 20, yPos);
                    yPos += 10;
                }
            });
        }
        
        // Risk Areas section
        const riskAreas = document.querySelectorAll('.card-header:contains("Risk Areas") + .card-body .d-flex');
        if (riskAreas.length > 0) {
            doc.setFontSize(16);
            doc.setTextColor(220, 53, 69); // Danger red color
            doc.text('Priority Risk Areas', 20, yPos + 20);
            
            yPos += 40;
            doc.setFontSize(10);
            doc.setTextColor(0, 0, 0);
            
            riskAreas.forEach((area, index) => {
                if (index < 5) { // Top 5 risks
                    const areaName = area.querySelector('.fw-bold')?.textContent || '';
                    const areaScore = area.querySelector('.badge')?.textContent || '';
                    doc.text(`• ${areaName}: ${areaScore}`, 25, yPos);
                    yPos += 8;
                }
            });
        }
        
        // Key Insights section
        const insights = document.querySelectorAll('.alert-info li');
        if (insights.length > 0) {
            doc.setFontSize(16);
            doc.setTextColor(40, 116, 166);
            doc.text('Key Insights & Recommendations', 20, yPos + 20);
            
            yPos += 40;
            doc.setFontSize(10);
            doc.setTextColor(0, 0, 0);
            
            insights.forEach((insight, index) => {
                if (yPos > 270) { // Check if we need a new page
                    doc.addPage();
                    yPos = 30;
                }
                const text = insight.textContent.trim();
                const lines = doc.splitTextToSize(text, 170);
                doc.text(lines, 20, yPos);
                yPos += lines.length * 8 + 5;
            });
        }
        
        // Footer
        if (yPos > 250) {
            doc.addPage();
            yPos = 30;
        }
        
        doc.setFontSize(8);
        doc.setTextColor(128, 128, 128);
        doc.text('Generated by Ransomware Resilience Assessment Tool', 20, yPos + 30);
        doc.text('Based on MITRE ATT&CK Framework', 20, yPos + 40);
        
        // Save the PDF
        const filename = `Ransomware_Assessment_${orgName.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`;
        doc.save(filename);
        
        // Show success message
        utils.showToast('PDF report generated successfully!', 'success');
    },
    
    /**
     * Generate a more detailed PDF using html2canvas
     */
    exportDetailedPDF: async function() {
        try {
            utils.showToast('Generating detailed PDF report...', 'info');
            
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF('p', 'mm', 'a4');
            
            // Hide export buttons temporarily
            const exportBtns = document.querySelectorAll('.dropdown');
            exportBtns.forEach(btn => btn.style.display = 'none');
            
            // Capture main content
            const element = document.querySelector('.container-fluid');
            const canvas = await html2canvas(element, {
                scale: 2,
                useCORS: true,
                allowTaint: true,
                backgroundColor: '#ffffff'
            });
            
            // Restore export buttons
            exportBtns.forEach(btn => btn.style.display = '');
            
            const imgData = canvas.toDataURL('image/png');
            const imgWidth = 210; // A4 width in mm
            const pageHeight = 295; // A4 height in mm
            const imgHeight = (canvas.height * imgWidth) / canvas.width;
            let heightLeft = imgHeight;
            
            let position = 0;
            
            // Add first page
            doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
            heightLeft -= pageHeight;
            
            // Add additional pages if needed
            while (heightLeft >= 0) {
                position = heightLeft - imgHeight;
                doc.addPage();
                doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
                heightLeft -= pageHeight;
            }
            
            // Save the PDF
            const orgName = document.querySelector('.text-muted')?.textContent?.split(' | ')[0] || 'Organization';
            const filename = `Detailed_Assessment_${orgName.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`;
            doc.save(filename);
            
            utils.showToast('Detailed PDF report generated successfully!', 'success');
        } catch (error) {
            console.error('Error generating PDF:', error);
            utils.showToast('Error generating PDF. Please try again.', 'danger');
        }
    },
    
    /**
     * Print the assessment results
     */
    printReport: function() {
        // Create a print-friendly version
        const printWindow = window.open('', '_blank');
        const orgName = document.querySelector('.text-muted')?.textContent?.split(' | ')[0] || 'Organization';
        const assessor = document.querySelector('.text-muted')?.textContent?.split(' | ')[1] || 'Assessor';
        
        // Get all the assessment data
        const overallScore = document.querySelector('.score-display')?.textContent || '0%';
        const readinessLevel = document.querySelector('.readiness-badge')?.textContent || 'Unknown';
        
        // Build print content
        let printContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ransomware Assessment Report - ${orgName}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
                .header { text-align: center; border-bottom: 2px solid #2874a6; margin-bottom: 30px; padding-bottom: 15px; }
                .org-info { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
                .score-section { text-align: center; background: #e3f2fd; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
                .score-large { font-size: 48px; font-weight: bold; color: #2874a6; }
                .section { margin-bottom: 25px; }
                .section-title { color: #2874a6; font-size: 18px; font-weight: bold; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
                table { width: 100%; border-collapse: collapse; margin-top: 10px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .risk-item, .insight-item { margin: 8px 0; padding: 5px; background: #fff3cd; border-left: 4px solid #ffc107; }
                .strength-item { margin: 8px 0; padding: 5px; background: #d4edda; border-left: 4px solid #28a745; }
                @media print { body { margin: 0; } .no-print { display: none; } }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Ransomware Resilience Assessment Report</h1>
                <p>Based on MITRE ATT&CK Framework</p>
            </div>
            
            <div class="org-info">
                <strong>Organization:</strong> ${orgName}<br>
                <strong>Assessed by:</strong> ${assessor}<br>
                <strong>Report Date:</strong> ${new Date().toLocaleDateString()}<br>
                <strong>Assessment Time:</strong> ${new Date().toLocaleTimeString()}
            </div>
            
            <div class="score-section">
                <div class="score-large">${overallScore}</div>
                <div style="font-size: 18px; margin-top: 10px;">Overall Readiness Level: <strong>${readinessLevel}</strong></div>
            </div>
        `;
        
        // Add stage performance table
        const stageRows = document.querySelectorAll('#stageTable tbody tr');
        if (stageRows.length > 0) {
            printContent += `
            <div class="section">
                <div class="section-title">Stage Performance Breakdown</div>
                <table>
                    <tr>
                        <th>Stage</th>
                        <th>Score</th>
                        <th>Questions</th>
                        <th>Status</th>
                    </tr>
            `;
            
            stageRows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length >= 4) {
                    printContent += `
                    <tr>
                        <td>${cells[0].textContent.trim()}</td>
                        <td>${cells[1].textContent.trim()}</td>
                        <td>${cells[2].textContent.trim()}</td>
                        <td>${cells[4].textContent.trim()}</td>
                    </tr>
                    `;
                }
            });
            
            printContent += '</table></div>';
        }
        
        // Add risk areas
        const riskItems = document.querySelectorAll('.bg-danger .fw-bold');
        if (riskItems.length > 0) {
            printContent += '<div class="section"><div class="section-title">Priority Risk Areas</div>';
            riskItems.forEach((item, index) => {
                if (index < 5) {
                    const score = item.parentElement.querySelector('.badge')?.textContent || '';
                    printContent += `<div class="risk-item">• ${item.textContent}: ${score}</div>`;
                }
            });
            printContent += '</div>';
        }
        
        // Add strength areas
        const strengthItems = document.querySelectorAll('.bg-success .fw-bold');
        if (strengthItems.length > 0) {
            printContent += '<div class="section"><div class="section-title">Strength Areas</div>';
            strengthItems.forEach((item, index) => {
                if (index < 5) {
                    const score = item.parentElement.querySelector('.badge')?.textContent || '';
                    printContent += `<div class="strength-item">• ${item.textContent}: ${score}</div>`;
                }
            });
            printContent += '</div>';
        }
        
        // Add key insights
        const insights = document.querySelectorAll('.alert-info li');
        if (insights.length > 0) {
            printContent += '<div class="section"><div class="section-title">Key Insights & Recommendations</div>';
            insights.forEach(insight => {
                printContent += `<div class="insight-item">${insight.textContent}</div>`;
            });
            printContent += '</div>';
        }
        
        printContent += `
            <div class="section" style="margin-top: 40px; text-align: center; color: #666; font-size: 12px;">
                <p>Generated by Ransomware Resilience Assessment Tool</p>
                <p>This report provides a comprehensive assessment based on industry best practices and the MITRE ATT&CK framework.</p>
            </div>
        </body>
        </html>
        `;
        
        printWindow.document.write(printContent);
        printWindow.document.close();
        
        // Wait for content to load then print
        setTimeout(() => {
            printWindow.print();
        }, 500);
        
        utils.showToast('Print dialog opened!', 'info');
    }
};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    themeManager.init();
    
    // Check for active session on dashboard
    if (document.getElementById('session-status')) {
        sessionManager.getSessionData().then(data => {
            sessionManager.updateSessionDisplay(data);
        });
    }
    
    // Initialize form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        formValidator.addRealTimeValidation(form);
    });
    
    // Initialize assessment features if on questionnaire page
    if (document.querySelector('.question-item')) {
        assessmentManager.setupAutoSave();
        assessmentManager.updateStageProgress();
    }
    
    // Initialize charts if on results page
    if (document.getElementById('stageChart') || document.getElementById('mitreChart')) {
        // Wait for Chart.js to load
        if (typeof Chart !== 'undefined') {
            chartManager.initializeCharts();
        } else {
            window.addEventListener('load', () => {
                chartManager.initializeCharts();
            });
        }
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    });
    
    cards.forEach(card => {
        observer.observe(card);
    });
});

// Global functions for inline event handlers
window.exportResults = function(format) {
    exportManager.exportResults(format);
};

window.assessmentUtils = {
    saveResponse: assessmentManager.saveResponse.bind(assessmentManager),
    updateProgress: assessmentManager.updateProgress.bind(assessmentManager),
    showToast: utils.showToast
};

// Add pulse animation for attention-grabbing elements
const style = document.createElement('style');
style.textContent = `
    .btn-pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(style);

// Global functions for PDF export
window.exportToPDF = function() {
    reportGenerator.exportToPDF();
};

window.exportDetailedPDF = function() {
    reportGenerator.exportDetailedPDF();
};

window.printReport = function() {
    reportGenerator.printReport();
};
