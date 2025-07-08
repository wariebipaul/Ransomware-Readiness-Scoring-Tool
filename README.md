# 🛡️ Ransomware Resilience Assessment Tool

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.2%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

> **A comprehensive cybersecurity assessment platform to evaluate organizational preparedness against ransomware attacks.**

## 🚀 Quick Start

### Web Application (Recommended)
```bash
git clone https://github.com/wariebipaul/Ransomware-Readiness-Scoring-Tool.git
cd Ransomware-Readiness-Scoring-Tool/ransomware-resilience-tool
pip install -r requirements.txt
python web_app.py
```

Visit `http://127.0.0.1:5000` to start your assessment!

### Console Application
```bash
python src/main.py
```

## 🌟 Key Features

- **🎯 MITRE ATT&CK Integration**: Questions mapped to specific attack techniques
- **📊 Intelligent Scoring**: Weighted algorithm with 5-level readiness classification
- **💡 Actionable Recommendations**: Prioritized improvement suggestions
- **📄 Multiple Export Formats**: PDF, JSON, CSV, and print-ready reports
- **🔒 Framework Compliance**: NIST CSF, ISO 27001, CIS Controls alignment
- **🌐 Dual Interface**: Web-based and console applications

## 📋 Assessment Overview

The tool evaluates your organization across **3 critical stages**:

1. **🛡️ Pre-Infection (8 questions)**: Preventive measures and preparedness
2. **⚠️ Active Infection (4 questions)**: Response capabilities during an attack
3. **🔄 Post-Infection (3 questions)**: Recovery and lessons learned

## 📖 Complete Documentation

For detailed documentation, architecture details, and comprehensive guides, see:

**[📚 COMPREHENSIVE_README.md](COMPREHENSIVE_README.md)**

This includes:
- 🏗️ Complete project architecture
- 📁 Detailed directory structure
- 🔧 Technical implementation details
- 🧪 Testing and validation procedures
- 🐛 Troubleshooting guide
- 🛡️ Security frameworks integration

## 🎯 Sample Assessment Results

| Readiness Level | Score Range | Description |
|----------------|-------------|-------------|
| 🏆 Excellent | 85-100% | Industry-leading security posture |
| ✅ Good | 70-84% | Strong defenses with minor gaps |
| ⚡ Moderate | 55-69% | Adequate protection, needs improvement |
| ⚠️ Poor | 40-54% | Significant vulnerabilities present |
| 🚨 Critical | 0-39% | Immediate action required |

## 🛠️ Technology Stack

- **Backend**: Python 3.6+, Flask 2.2+
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **UI Libraries**: Rich (console), Chart.js (web)
- **Export**: jsPDF, html2canvas (client-side PDF generation)
- **Testing**: Pytest, comprehensive integration tests

## 📊 Project Structure

```
ransomware-resilience-tool/
├── 🌐 web_app.py              # Flask web application
├── 📱 src/main.py             # Console application
├── 🧠 src/assessment/         # Core assessment engine
├── 🎨 templates/              # Web interface templates
├── 📄 static/                 # CSS, JavaScript, assets
├── 🧪 tests/                  # Comprehensive test suite
└── 📚 docs/                   # Documentation
```

## 🚀 Production Ready Features

- ✅ **Enterprise-Grade Security**: MITRE ATT&CK framework integration
- ✅ **Professional Reporting**: Multiple export formats with charts
- ✅ **Comprehensive Testing**: Unit and integration test coverage
- ✅ **Session Management**: Secure data handling and progress tracking
- ✅ **Responsive Design**: Mobile and desktop compatibility
- ✅ **Privacy-Focused**: Client-side processing, minimal data retention

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 **Documentation**: [COMPREHENSIVE_README.md](COMPREHENSIVE_README.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/wariebipaul/Ransomware-Readiness-Scoring-Tool/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/wariebipaul/Ransomware-Readiness-Scoring-Tool/discussions)

---

**⚡ Start your ransomware readiness assessment today and strengthen your organization's cyber defenses!**

[![GitHub stars](https://img.shields.io/github/stars/wariebipaul/Ransomware-Readiness-Scoring-Tool.svg?style=social&label=Star)](https://github.com/wariebipaul/Ransomware-Readiness-Scoring-Tool)
[![GitHub forks](https://img.shields.io/github/forks/wariebipaul/Ransomware-Readiness-Scoring-Tool.svg?style=social&label=Fork)](https://github.com/wariebipaul/Ransomware-Readiness-Scoring-Tool/fork)
