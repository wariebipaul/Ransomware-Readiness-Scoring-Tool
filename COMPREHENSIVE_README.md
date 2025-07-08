# 🛡️ Ransomware Resilience Assessment Tool

## 📋 Table of Contents
- [Overview](#overview)
- [Project Architecture](#project-architecture)
- [Core Components](#core-components)
- [Directory Structure](#directory-structure)
- [Installation & Setup](#installation--setup)
- [Usage Modes](#usage-modes)
- [Technical Implementation](#technical-implementation)
- [Testing & Validation](#testing--validation)
- [Export Capabilities](#export-capabilities)
- [Security Frameworks](#security-frameworks)
- [Development Notes](#development-notes)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The **Ransomware Resilience Assessment Tool** is a comprehensive cybersecurity assessment platform designed to evaluate an organization's preparedness against ransomware attacks. Built with enterprise-grade security frameworks in mind, this tool provides actionable insights and recommendations based on industry best practices.

### 🌟 Key Features
- **Multi-Modal Interface**: Both web-based and console applications
- **MITRE ATT&CK Integration**: Questions mapped to specific attack techniques
- **Intelligent Scoring**: Weighted algorithm with readiness level classification
- **Actionable Recommendations**: Prioritized improvement suggestions
- **Multiple Export Formats**: PDF, JSON, CSV, and print-ready reports
- **Framework Alignment**: NIST CSF, ISO 27001, CIS Controls compliance
- **Session Management**: Secure data handling and progress tracking

---

## 🏗️ Project Architecture

The application follows a modular, layered architecture designed for scalability and maintainability:

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                    │
├─────────────────────────────────────────────────────────────┤
│  Web Interface (Flask)    │    Console Interface (Rich)    │
├─────────────────────────────────────────────────────────────┤
│                   APPLICATION LAYER                        │
├─────────────────────────────────────────────────────────────┤
│  Assessment Engine  │  Scoring Engine  │  Recommendation   │
│                     │                  │     Engine        │
├─────────────────────────────────────────────────────────────┤
│                      DATA LAYER                            │
├─────────────────────────────────────────────────────────────┤
│  Questions DB  │  Frameworks  │  Templates  │  Validation   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧩 Core Components

### 1. **Assessment Engine** (`src/assessment/`)
- **Questionnaire Module** (`questionnaire.py`): Manages the 15-question assessment across 3 stages
- **Scoring Module** (`scoring.py`): Implements weighted scoring algorithm (0-4 scale)
- **Recommendations Module** (`recommendations.py`): Generates prioritized action plans

### 2. **User Interface Layer** (`src/ui/` & `templates/`)
- **Console Interface** (`interface.py`): Rich terminal-based UI with progress tracking
- **Web Interface** (`templates/`): Bootstrap 5 responsive web application
- **Static Assets** (`static/`): CSS styling and JavaScript functionality

### 3. **Data Management** (`src/data/`)
- **Questions Database** (`questions.py`): Structured question data with MITRE mapping
- **Frameworks Integration** (`frameworks.py`): MITRE ATT&CK and other standards
- **Validation Rules** (`validation.py`): Input validation and data integrity

### 4. **Utility Services** (`src/utils/`)
- **Export Engine** (`export.py`): Multi-format report generation
- **Validation Service** (`validation.py`): Data validation and error handling

---

## 📁 Directory Structure

```
ransomware-resilience-tool/
├── 📄 README.md                     # Basic project documentation
├── 📄 requirements.txt              # Python dependencies
├── 📄 setup.py                      # Package installation script
├── 📄 web_app.py                    # Flask web application entry point
├── 📄 FINAL_STATUS_REPORT.md       # Implementation completion report
│
├── 📁 src/                          # Source code directory
│   ├── 📄 main.py                   # Console application entry point
│   │
│   ├── 📁 assessment/               # Core assessment logic
│   │   ├── 📄 __init__.py
│   │   ├── 📄 questionnaire.py      # Question flow management
│   │   ├── 📄 scoring.py            # Scoring algorithms
│   │   └── 📄 recommendations.py    # Recommendation generation
│   │
│   ├── 📁 data/                     # Data models and frameworks
│   │   ├── 📄 __init__.py
│   │   ├── 📄 questions.py          # Question database (15 questions)
│   │   └── 📄 frameworks.py         # MITRE ATT&CK, NIST CSF mappings
│   │
│   ├── 📁 ui/                       # User interface components
│   │   ├── 📄 __init__.py
│   │   └── 📄 interface.py          # Console UI with Rich library
│   │
│   ├── 📁 utils/                    # Utility functions
│   │   ├── 📄 __init__.py
│   │   ├── 📄 export.py             # Export utilities (PDF, JSON, CSV)
│   │   └── 📄 validation.py         # Input validation
│   │
│   └── 📁 tests/                    # Unit tests
│       └── 📄 test_comprehensive.py
│
├── 📁 templates/                    # Flask HTML templates
│   ├── 📄 base.html                 # Base template with navigation
│   ├── 📄 index.html                # Dashboard/home page
│   ├── 📄 setup.html                # Organization setup form
│   ├── 📄 questionnaire.html        # Assessment questions interface
│   ├── 📄 results.html              # Results display with charts
│   ├── 📄 framework_info.html       # Framework information page
│   ├── 📄 help.html                 # Help and documentation
│   └── 📄 error.html                # Error handling page
│
├── 📁 static/                       # Static web assets
│   ├── 📁 css/
│   │   └── 📄 style.css             # Custom CSS (417 lines)
│   └── 📁 js/
│       └── 📄 app.js                # JavaScript functionality
│
├── 📁 docs/                         # Documentation
│   ├── 📄 user_guide.md             # User manual
│   ├── 📄 development_notes.md      # Development documentation
│   └── 📄 PDF_Export_Guide.md       # Export functionality guide
│
├── 📁 tests/                        # Integration tests
│   ├── 📄 __init__.py
│   ├── 📄 test_assessment.py        # Assessment engine tests
│   ├── 📄 test_scoring.py           # Scoring algorithm tests
│   └── 📄 test_validation.py        # Validation tests
│
└── 📁 debug_scripts/                # Development and testing scripts
    ├── 📄 debug_main_flow.py        # Main flow debugging
    ├── 📄 test_web_flow.py          # Web application testing
    ├── 📄 final_validation.py       # Final validation script
    └── ... (multiple debug files)
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.6+** (recommended: Python 3.8+)
- **pip** (Python package manager)
- **Web browser** (for web interface)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd ransomware-resilience-tool
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```bash
   python src/main.py --help
   ```

### Dependencies Overview
```
Core Framework:
- Flask 2.2.0+ (Web application framework)
- Rich 12.0.0+ (Console UI enhancement)

Data Processing:
- Pandas 1.5.0+ (Data manipulation)
- NumPy 1.21.0+ (Numerical computations)
- JSONSchema 4.0.0+ (Data validation)

Development & Testing:
- Pytest 7.0.0+ (Testing framework)
- Black 22.0.0+ (Code formatting)
- Flake8 5.0.0+ (Linting)
```

---

## 🎮 Usage Modes

### 1. Web Application Mode (Recommended)

**Start the Web Server:**
```bash
python web_app.py
```

**Access the Application:**
- Open browser to `http://127.0.0.1:5000`
- Complete organization setup
- Navigate through the 3-stage assessment
- View results and export reports

**Features:**
- ✅ Responsive web interface
- ✅ Real-time progress tracking
- ✅ Session management
- ✅ Multiple export formats
- ✅ Interactive charts and visualizations

### 2. Console Application Mode

**Start the Console Application:**
```bash
python src/main.py
```

**Features:**
- ✅ Rich terminal interface with colors
- ✅ Interactive menu system
- ✅ Progress bars and status indicators
- ✅ Text-based reporting

### 3. Automated Testing Mode

**Run Comprehensive Tests:**
```bash
python test_web_flow.py        # Web application flow test
python final_validation.py     # Complete system validation
pytest tests/                  # Unit tests
```

---

## 🔧 Technical Implementation

### Assessment Engine Architecture

#### **Question Structure**
Each question follows a standardized format:
```python
{
    "id": "backup_strategy",
    "question": "How frequently does your organization perform data backups?",
    "type": "multiple_choice",
    "options": [
        {"value": 4, "text": "Daily automated backups with testing"},
        {"value": 3, "text": "Daily automated backups"},
        {"value": 2, "text": "Weekly backups"},
        {"value": 1, "text": "Monthly or irregular backups"},
        {"value": 0, "text": "No regular backup strategy"}
    ],
    "weight": 10,
    "mitre_technique": "T1490"
}
```

#### **Scoring Algorithm**
```python
# Weighted scoring calculation
weighted_score = response_value * question_weight
stage_score = sum(all_weighted_scores_in_stage)
overall_percentage = (total_score / max_possible_score) * 100

# Readiness level classification
if percentage >= 85: level = "Excellent"
elif percentage >= 70: level = "Good"
elif percentage >= 55: level = "Moderate"
elif percentage >= 40: level = "Poor"
else: level = "Critical"
```

#### **Three Assessment Stages**

1. **Pre-Infection (8 questions)**
   - Backup strategies and isolation
   - Patch management
   - Network segmentation
   - Email security
   - Endpoint protection
   - User training
   - Access controls
   - Monitoring systems

2. **Active Infection (4 questions)**
   - Incident response procedures
   - Isolation capabilities
   - Communication protocols
   - Decision-making processes

3. **Post-Infection (3 questions)**
   - Recovery procedures
   - Business continuity
   - Lessons learned integration

### Web Application Technical Stack

#### **Backend (Flask)**
- **Routes**: 8 main endpoints for assessment flow
- **Session Management**: Secure server-side session handling
- **API Design**: RESTful endpoints for data operations
- **Error Handling**: Comprehensive exception management

#### **Frontend (Bootstrap 5 + Custom CSS)**
- **Responsive Design**: Mobile-first approach
- **Progressive Enhancement**: Works without JavaScript
- **Accessibility**: ARIA labels and screen reader support
- **Interactive Elements**: Progress bars, charts, tooltips

#### **Client-Side PDF Generation**
- **jsPDF**: PDF document creation
- **html2canvas**: Chart and visualization capture
- **Privacy-Focused**: No data sent to external servers

---

## 🧪 Testing & Validation

### Test Coverage Areas

1. **Unit Tests** (`tests/`)
   - Assessment engine functionality
   - Scoring algorithm accuracy
   - Data validation rules
   - Export functionality

2. **Integration Tests**
   - Complete assessment flow
   - Web application endpoints
   - Session management
   - File export operations

3. **User Experience Tests**
   - Interface responsiveness
   - Error handling
   - Progress tracking
   - Results display

### Running Tests

```bash
# Run all unit tests
pytest tests/ -v

# Test web application flow
python test_web_flow.py

# Complete system validation
python final_validation.py

# Test specific components
python debug_scoring.py        # Scoring engine
python debug_questionnaire.py  # Question flow
```

---

## 📊 Export Capabilities

### Supported Export Formats

#### **1. PDF Reports**
- **Quick PDF**: Basic text report (1-3 seconds)
- **Detailed PDF**: Charts and visualizations (5-10 seconds)
- **Client-Side Generation**: No server processing required
- **Professional Formatting**: Corporate-ready layout

#### **2. JSON Export**
```json
{
  "metadata": {
    "export_timestamp": "2025-01-08T10:30:00",
    "tool_version": "2.0",
    "format_version": "1.0"
  },
  "session_info": { /* Organization and assessor data */ },
  "results": { /* Comprehensive scoring results */ },
  "recommendations": { /* Prioritized action plans */ }
}
```

#### **3. CSV Export**
- Summary scores by stage
- Question-by-question breakdown
- Recommendation priorities
- Spreadsheet-ready format

#### **4. Print-Optimized Output**
- Browser print dialog integration
- Clean, professional layout
- Page break optimization

---

## 🛡️ Security Frameworks

### MITRE ATT&CK Framework Integration

Each assessment question maps to specific MITRE ATT&CK techniques:

| Technique | Name | Tactic | Questions |
|-----------|------|---------|-----------|
| T1566 | Phishing | Initial Access | Email Security |
| T1190 | Exploit Public-Facing Application | Initial Access | Patch Management |
| T1021 | Remote Services | Lateral Movement | Network Segmentation |
| T1055 | Process Injection | Defense Evasion | Endpoint Protection |
| T1083 | File and Directory Discovery | Discovery | Monitoring Systems |
| T1486 | Data Encrypted for Impact | Impact | Recovery Procedures |
| T1490 | Inhibit System Recovery | Impact | Backup Strategy |

### Framework Alignment

#### **NIST Cybersecurity Framework**
- **IDENTIFY**: Asset management and risk assessment questions
- **PROTECT**: Safeguards and access control questions
- **DETECT**: Monitoring and detection capability questions
- **RESPOND**: Incident response and communication questions
- **RECOVER**: Recovery planning and improvement questions

#### **ISO 27001 Compliance**
- Information security management system components
- Risk management practices
- Incident management procedures
- Business continuity planning

#### **CIS Critical Security Controls**
- Inventory and control of hardware/software assets
- Continuous vulnerability management
- Controlled use of administrative privileges
- Incident response and management

---

## 👨‍💻 Development Notes

### Code Quality Standards
- **PEP 8 Compliance**: Consistent Python style
- **Type Hints**: Enhanced code documentation
- **Docstrings**: Comprehensive function documentation
- **Error Handling**: Graceful failure management
- **Logging**: Comprehensive debugging support

### Architecture Decisions

1. **Modular Design**: Separated concerns for maintainability
2. **Framework Agnostic**: Core logic independent of UI framework
3. **Data-Driven**: Questions and frameworks easily configurable
4. **Extensible**: Simple to add new assessment areas
5. **Privacy-First**: Minimal data retention, local processing

### Performance Considerations
- **Lazy Loading**: Questions loaded on demand
- **Session Optimization**: Minimal server-side storage
- **Client-Side Processing**: PDF generation in browser
- **Caching**: Static assets and framework data

---

## 🐛 Troubleshooting

### Common Issues

#### **Installation Problems**
```bash
# Missing dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Python version compatibility
python --version  # Should be 3.6+
```

#### **Web Application Issues**
```bash
# Port already in use
python web_app.py --port 5001

# Session errors
# Clear browser cache and cookies

# Template not found
# Verify templates/ directory exists
```

#### **Console Application Issues**
```bash
# Rich library not working
pip install rich>=12.0.0

# Encoding issues on Windows
# Use UTF-8 compatible terminal
```

#### **Export Failures**
- **PDF Generation**: Ensure modern browser with JavaScript enabled
- **File Permissions**: Check write permissions in export directory
- **Large Reports**: Allow extra time for detailed PDF generation

### Debug Scripts

The project includes comprehensive debug scripts:
- `debug_main_flow.py`: Test complete assessment flow
- `debug_scoring.py`: Validate scoring calculations
- `debug_web_scoring.py`: Test web-based scoring
- `test_web_functionality.py`: Comprehensive web testing

---

## 📈 Project Status

### ✅ Completed Features
- [x] Complete assessment questionnaire (15 questions)
- [x] MITRE ATT&CK framework integration
- [x] Weighted scoring algorithm
- [x] Web application with Bootstrap 5 UI
- [x] Console application with Rich UI
- [x] Multi-format export capabilities
- [x] Session management and progress tracking
- [x] Comprehensive testing suite
- [x] Professional documentation

### 🚀 Production Ready
The tool is **production-ready** with:
- Comprehensive testing and validation
- Security best practices implementation
- Professional user interface
- Enterprise-grade reporting
- Framework compliance alignment
- Extensive documentation

### 📋 Future Enhancements
- Database integration for large-scale deployments
- Multi-language support
- Advanced analytics and trending
- Integration with security tools
- Mobile application development

---

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please follow the standard practices for submitting issues and pull requests.

## 📞 Support

For questions, issues, or feature requests:
1. Check the documentation in the `docs/` directory
2. Review the troubleshooting section
3. Run the debug scripts for diagnosis
4. Create an issue with detailed information

---

**Last Updated**: January 8, 2025  
**Version**: 2.0  
**Status**: Production Ready ✅
