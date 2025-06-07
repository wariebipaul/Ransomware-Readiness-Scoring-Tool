# Questionnaire data structure based on MITRE ATT&CK framework
# Covers pre-infection, active infection, and post-infection stages

QUESTIONS = {
    "pre_infection": {
        "title": "Pre-Infection Preparedness",
        "description": "These questions assess your organization's preventive measures against ransomware attacks.",
        "questions": [
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
            },
            {
                "id": "backup_isolation",
                "question": "Are your backups stored in an isolated, air-gapped environment?",
                "type": "multiple_choice",
                "options": [
                    {"value": 4, "text": "Yes, completely air-gapped with multiple copies"},
                    {"value": 3, "text": "Yes, air-gapped"},
                    {"value": 2, "text": "Partially isolated (network segmented)"},
                    {"value": 1, "text": "Limited isolation"},
                    {"value": 0, "text": "No isolation - connected to main network"}
                ],
                "weight": 9,
                "mitre_technique": "T1490"
            },
            {
                "id": "patch_management",
                "question": "How does your organization handle software updates and patches?",
                "type": "multiple_choice",
                "options": [
                    {"value": 4, "text": "Automated patching with testing and rollback capabilities"},
                    {"value": 3, "text": "Regular automated patching"},
                    {"value": 2, "text": "Monthly manual patching"},
                    {"value": 1, "text": "Irregular patching"},
                    {"value": 0, "text": "No formal patch management"}
                ],
                "weight": 8,
                "mitre_technique": "T1190"
            },
            {
                "id": "network_segmentation",
                "question": "Is your network properly segmented to limit lateral movement?",
                "type": "multiple_choice",
                "options": [
                    {"value": 4, "text": "Full micro-segmentation with zero-trust architecture"},
                    {"value": 3, "text": "Well-defined network segments with access controls"},
                    {"value": 2, "text": "Basic network segmentation"},
                    {"value": 1, "text": "Limited segmentation"},
                    {"value": 0, "text": "Flat network with no segmentation"}
                ],
                "weight": 8,
                "mitre_technique": "T1021"
            },
            {
                "id": "email_security",
                "question": "What email security measures are in place?",
                "type": "multiple_choice",
                "options": [
                    {"value": 4, "text": "Advanced threat protection, sandboxing, and user training"},
                    {"value": 3, "text": "Anti-spam and anti-malware with link protection"},
                    {"value": 2, "text": "Basic anti-spam and anti-malware"},
                    {"value": 1, "text": "Limited email filtering"},
                    {"value": 0, "text": "No email security measures"}
                ],
                "weight": 7,
                "mitre_technique": "T1566"
            },
            {
                "id": "endpoint_protection",
                "question": "What endpoint protection solutions are deployed?",
                "type": "multiple_choice",
                "options": [
                    {"value": 4, "text": "EDR/XDR with behavioral analysis and threat hunting"},
                    {"value": 3, "text": "Next-generation antivirus with behavioral detection"},
                    {"value": 2, "text": "Traditional antivirus with real-time scanning"},
                    {"value": 1, "text": "Basic antivirus"},
                    {"value": 0, "text": "No endpoint protection"}
                ],
                "weight": 8,
                "mitre_technique": "T1055"
            },
            {
                "id": "user_training",
                "question": "How often do employees receive cybersecurity awareness training?",
                "type": "multiple_choice",
                "options": [
                    {"value": 4, "text": "Quarterly training with phishing simulations"},
                    {"value": 3, "text": "Bi-annual training with simulations"},
                    {"value": 2, "text": "Annual training"},
                    {"value": 1, "text": "Irregular training"},
                    {"value": 0, "text": "No formal training program"}
                ],
                "weight": 7,
                "mitre_technique": "T1566"
            }
        ]
    },
    "active_infection": {
        "title": "Active Infection Response",
        "description": "These questions assess your organization's ability to detect and respond to active ransomware attacks.",
        "questions": [
            {
                "id": "monitoring_logging",
                "question": "What monitoring and logging capabilities are in place?",
                "type": "multiple_choice",
                "options": [
                    {"value": 4, "text": "SIEM with real-time alerting and 24/7 monitoring"},
                    {"value": 3, "text": "Centralized logging with automated alerting"},
                    {"value": 2, "text": "Basic logging and monitoring"},
                    {"value": 1, "text": "Limited logging"},
                    {"value": 0, "text": "No centralized monitoring"}
                ],
                "weight": 9,
                "mitre_technique": "T1083"
            },
            {
                "id": "incident_response_plan",
                "question": "Does your organization have a documented incident response plan?",
                "type": "multiple_choice",
                "options": [
                    {"value": 4, "text": "Comprehensive plan with regular testing and updates"},
                    {"value": 3, "text": "Documented plan with annual testing"},
                    {"value": 2, "text": "Basic documented plan"},
                    {"value": 1, "text": "Informal response procedures"},
                    {"value": 0, "text": "No incident response plan"}
                ],
                "weight": 10,
                "mitre_technique": "T1486"
            },
            {
                "id": "network_isolation",
                "question": "Can you quickly isolate infected systems from the network?",
                "type": "multiple_choice",
                "options": [
                    {"value": 4, "text": "Automated isolation with orchestrated response"},
                    {"value": 3, "text": "Remote isolation capabilities"},
                    {"value": 2, "text": "Manual isolation procedures"},
                    {"value": 1, "text": "Limited isolation capabilities"},
                    {"value": 0, "text": "No isolation procedures"}
                ],
                "weight": 8,
                "mitre_technique": "T1021"
            },
            {
                "id": "communication_plan",
                "question": "Is there a communication plan for ransomware incidents?",
                "type": "multiple_choice",
                "options": [
                    {"value": 4, "text": "Comprehensive plan with stakeholder matrix and templates"},
                    {"value": 3, "text": "Documented communication procedures"},
                    {"value": 2, "text": "Basic communication plan"},
                    {"value": 1, "text": "Informal communication procedures"},
                    {"value": 0, "text": "No communication plan"}
                ],
                "weight": 6,
                "mitre_technique": "T1486"
            }
        ]
    },
    "post_infection": {
        "title": "Post-Infection Recovery",
        "description": "These questions assess your organization's recovery capabilities after a ransomware attack.",
        "questions": [
            {
                "id": "recovery_procedures",
                "question": "How comprehensive are your data recovery procedures?",
                "type": "multiple_choice",
                "options": [
                    {"value": 4, "text": "Tested procedures with defined RTOs and RPOs"},
                    {"value": 3, "text": "Documented recovery procedures"},
                    {"value": 2, "text": "Basic recovery procedures"},
                    {"value": 1, "text": "Informal recovery approach"},
                    {"value": 0, "text": "No recovery procedures"}
                ],
                "weight": 10,
                "mitre_technique": "T1490"
            },
            {
                "id": "business_continuity",
                "question": "Does your organization have a business continuity plan?",
                "type": "multiple_choice",
                "options": [
                    {"value": 4, "text": "Comprehensive BCP with regular testing"},
                    {"value": 3, "text": "Documented BCP with annual testing"},
                    {"value": 2, "text": "Basic business continuity plan"},
                    {"value": 1, "text": "Informal continuity procedures"},
                    {"value": 0, "text": "No business continuity plan"}
                ],
                "weight": 8,
                "mitre_technique": "T1486"
            },
            {
                "id": "forensic_capabilities",
                "question": "What forensic and investigation capabilities are available?",
                "type": "multiple_choice",
                "options": [
                    {"value": 4, "text": "In-house forensic team with external support"},
                    {"value": 3, "text": "External forensic support arrangements"},
                    {"value": 2, "text": "Basic forensic capabilities"},
                    {"value": 1, "text": "Limited investigation capabilities"},
                    {"value": 0, "text": "No forensic capabilities"}
                ],
                "weight": 6,
                "mitre_technique": "T1083"
            },
            {
                "id": "lessons_learned",
                "question": "How does your organization handle post-incident reviews?",
                "type": "multiple_choice",
                "options": [
                    {"value": 4, "text": "Formal post-incident review with improvement tracking"},
                    {"value": 3, "text": "Documented lessons learned process"},
                    {"value": 2, "text": "Basic post-incident review"},
                    {"value": 1, "text": "Informal review process"},
                    {"value": 0, "text": "No post-incident review"}
                ],
                "weight": 5,
                "mitre_technique": "T1486"
            }
        ]
    }
}

# Scoring thresholds
SCORE_THRESHOLDS = {
    "excellent": 85,
    "good": 70,
    "moderate": 55,
    "poor": 40,
    "critical": 0
}