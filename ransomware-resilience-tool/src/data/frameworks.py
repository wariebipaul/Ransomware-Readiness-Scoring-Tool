# Cybersecurity frameworks and MITRE ATT&CK mapping for ransomware assessment

# MITRE ATT&CK techniques relevant to ransomware
MITRE_TECHNIQUES = {
    "T1566": {
        "name": "Phishing",
        "description": "Adversaries may send phishing messages to gain access to victim systems",
        "tactic": "Initial Access"
    },
    "T1190": {
        "name": "Exploit Public-Facing Application",
        "description": "Adversaries may exploit weaknesses in software to gain access",
        "tactic": "Initial Access"
    },
    "T1021": {
        "name": "Remote Services",
        "description": "Adversaries may use valid accounts to log into a service specifically designed to accept remote connections",
        "tactic": "Lateral Movement"
    },
    "T1055": {
        "name": "Process Injection",
        "description": "Adversaries may inject code into processes to evade detection",
        "tactic": "Defense Evasion"
    },
    "T1083": {
        "name": "File and Directory Discovery",
        "description": "Adversaries may enumerate files and directories to find specific files",
        "tactic": "Discovery"
    },
    "T1486": {
        "name": "Data Encrypted for Impact",
        "description": "Adversaries may encrypt data on target systems to interrupt availability",
        "tactic": "Impact"
    },
    "T1490": {
        "name": "Inhibit System Recovery",
        "description": "Adversaries may delete or remove built-in operating system data and turn off services",
        "tactic": "Impact"
    }
}

# Cybersecurity frameworks mapping
FRAMEWORKS = {
    "NIST_CSF": {
        "name": "NIST Cybersecurity Framework",
        "functions": {
            "IDENTIFY": "Develop organizational understanding to manage cybersecurity risk",
            "PROTECT": "Develop and implement appropriate safeguards",
            "DETECT": "Develop and implement activities to identify cybersecurity events",
            "RESPOND": "Develop and implement activities to take action on detected cybersecurity incident",
            "RECOVER": "Develop and implement activities to maintain resilience and restore capabilities"
        }
    },
    "ISO_27001": {
        "name": "ISO/IEC 27001",
        "description": "International standard for information security management systems"
    },
    "CIS_CONTROLS": {
        "name": "CIS Critical Security Controls",
        "description": "Prioritized set of actions to protect organizations from cyber attacks"
    }
}

# Recommendation templates based on scores
RECOMMENDATION_TEMPLATES = {
    "backup_strategy": {
        "critical": "Implement daily automated backups immediately with testing procedures.",
        "poor": "Establish more frequent backup schedules and automation.",
        "moderate": "Enhance backup testing and validation procedures.",
        "good": "Consider implementing backup integrity monitoring.",
        "excellent": "Maintain current backup practices and review annually."
    },
    "network_segmentation": {
        "critical": "Implement basic network segmentation to limit lateral movement.",
        "poor": "Enhance network segmentation with additional controls.",
        "moderate": "Implement micro-segmentation for critical assets.",
        "good": "Consider zero-trust architecture implementation.",
        "excellent": "Maintain current segmentation and review architecture."
    },
    "incident_response": {
        "critical": "Develop and document incident response procedures immediately.",
        "poor": "Enhance incident response plan with testing procedures.",
        "moderate": "Implement regular tabletop exercises and plan updates.",
        "good": "Consider automation and orchestration capabilities.",
        "excellent": "Maintain current capabilities and conduct regular reviews."
    }
}