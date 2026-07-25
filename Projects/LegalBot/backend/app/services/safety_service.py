"""
Safety detection and emergency handling service
"""
from typing import Dict, List, Any, Optional
from loguru import logger
import re


# Emergency keywords by category
EMERGENCY_KEYWORDS = {
    "violence": [
        "beating", "hit", "assault", "abuse", "threat", "kill", "murder",
        "violence", "beaten", "attacked", "hurt", "injured", "weapon",
        "मारपीट", "हिंसा", "धमकी", "हमला"
    ],
    "arrest": [
        "arrested", "police custody", "jail", "detained", "lock up",
        "arrest warrant", "taken by police", "in custody",
        "गिरफ्तार", "हिरासत", "जेल"
    ],
    "cybercrime": [
        "scam", "fraud", "hacked", "stolen money", "upi fraud", "otp",
        "digital arrest", "fake call", "account frozen", "lost money",
        "ठगी", "धोखाधड़ी", "पैसे गए"
    ],
    "sexual_violence": [
        "rape", "sexual assault", "molest", "harassment", "eve teasing",
        "inappropriate touch", "sexual abuse", "molestation",
        "बलात्कार", "छेड़छाड़"
    ],
    "child_safety": [
        "child abuse", "minor", "underage", "child sexual", "pocso",
        "child marriage", "child labor",
        "बाल शोषण"
    ],
    "domestic_violence": [
        "husband beating", "wife beating", "domestic violence", "dowry",
        "torture", "kicked out", "in-laws harassment",
        "घरेलू हिंसा", "दहेज"
    ],
    "suicide": [
        "suicide", "kill myself", "end my life", "want to die",
        "आत्महत्या", "मरना चाहता"
    ]
}


# Helplines by category and state
HELPLINES = {
    "national": {
        "cybercrime": {
            "name": "Cybercrime Helpline",
            "number": "1930",
            "description": "Report cyber fraud, UPI scams, digital arrest"
        },
        "women": {
            "name": "Women in Distress Helpline",
            "number": "181",
            "description": "24x7 helpline for women in distress"
        },
        "child": {
            "name": "Child Helpline",
            "number": "1098",
            "description": "24x7 helpline for child safety"
        },
        "senior": {
            "name": "Elder Helpline",
            "number": "14567",
            "description": "Helpline for senior citizens"
        },
        "consumer": {
            "name": "National Consumer Helpline",
            "number": "1915",
            "description": "Consumer complaints and grievances"
        },
        "mental_health": {
            "name": "KIRAN Mental Health Helpline",
            "number": "1800-599-0019",
            "description": "24x7 mental health support"
        },
        "police": {
            "name": "Police Emergency",
            "number": "112",
            "description": "Emergency police assistance"
        }
    }
}


def detect_emergency(query: str) -> Dict[str, Any]:
    """
    Detect if query indicates an emergency situation
    
    Returns:
        {
            "is_emergency": bool,
            "type": str,  # violence, arrest, cybercrime, etc.
            "severity": str,  # critical, high, medium
            "keywords_found": List[str]
        }
    """
    query_lower = query.lower()
    
    detected_types = []
    all_keywords_found = []
    
    for category, keywords in EMERGENCY_KEYWORDS.items():
        found = []
        for keyword in keywords:
            if keyword.lower() in query_lower:
                found.append(keyword)
        
        if found:
            detected_types.append(category)
            all_keywords_found.extend(found)
    
    if not detected_types:
        return {
            "is_emergency": False,
            "type": None,
            "severity": "none",
            "keywords_found": []
        }
    
    # Determine severity
    severity = "medium"
    critical_types = ["violence", "arrest", "sexual_violence", "suicide"]
    if any(t in critical_types for t in detected_types):
        severity = "critical"
    elif "cybercrime" in detected_types:
        # Check if it's within golden hours (recent fraud)
        if any(word in query_lower for word in ["today", "just now", "now", "अभी", "आज"]):
            severity = "high"
    
    return {
        "is_emergency": True,
        "type": detected_types[0],  # Primary type
        "all_types": detected_types,
        "severity": severity,
        "keywords_found": all_keywords_found
    }


def get_relevant_helplines(
    category: str,
    state: Optional[str] = None
) -> List[Dict[str, str]]:
    """
    Get relevant helpline numbers for a category or segment
    
    Args:
        category: Emergency type (violence, cybercrime) or segment (s1-consumer, s4-cybercrime)
        state: Optional state code for state-specific numbers
    
    Returns:
        List of helpline dicts with name, number, description
    """
    helplines = []
    
    # Map segments to categories
    segment_to_category = {
        "s1-consumer": ["consumer"],
        "s4-cybercrime": ["cybercrime", "police"],
        "s3-family": ["women"],
        "s7-women-child": ["women", "child"],
        "s8-seniors": ["senior"],
        "violence": ["police", "women"],
        "domestic_violence": ["women"],
        "arrest": ["police"],
        "cybercrime": ["cybercrime"],
        "sexual_violence": ["women", "police"],
        "child_safety": ["child"],
        "suicide": ["mental_health"]
    }
    
    categories = segment_to_category.get(category, [category])
    
    # Get national helplines
    for cat in categories:
        if cat in HELPLINES["national"]:
            helplines.append(HELPLINES["national"][cat])
    
    # Add state-specific helplines if available
    # TODO: Add state-specific helpline database
    
    # Always add general police number for emergencies
    if category in ["violence", "arrest", "sexual_violence", "child_safety"]:
        if not any(h["number"] == "112" for h in helplines):
            helplines.append(HELPLINES["national"]["police"])
    
    return helplines


def get_safety_instructions(emergency_type: str) -> List[str]:
    """
    Get safety-first instructions for emergency situations
    """
    instructions = {
        "violence": [
            "🚨 Your safety comes first. If you're in immediate danger, call 112 (Police)",
            "Move to a safe location if possible",
            "Do not confront the aggressor alone",
            "Preserve evidence: photos of injuries, medical records, threatening messages",
            "Inform trusted family/friends about your situation"
        ],
        "domestic_violence": [
            "🚨 Your safety is the priority. You can call 181 (Women Helpline) 24x7",
            "You have the right to stay in your shared household (PWDVA)",
            "You can get a protection order from the magistrate",
            "Free legal aid is available through NALSA/DLSA",
            "Contact your local Protection Officer or One Stop Centre"
        ],
        "cybercrime": [
            "🚨 GOLDEN HOURS: Act immediately to freeze funds",
            "1. Call 1930 (Cybercrime Helpline) RIGHT NOW",
            "2. Call your bank to freeze the account: SBI 1800-1234, ICICI 1860-1200-7777",
            "3. File complaint on cybercrime.gov.in",
            "4. Do NOT delete any messages, screenshots, or transaction records",
            "Recovery chances decrease after 72 hours - ACT NOW"
        ],
        "arrest": [
            "🚨 Know your rights under BNSS 2023:",
            "Right to know the grounds of arrest",
            "Right to inform family/friend immediately",
            "Right to free legal aid (ask for DLSA lawyer)",
            "Right to medical examination",
            "Cannot be detained beyond 24 hours without magistrate's order",
            "For bailable offenses, you have the right to bail"
        ],
        "sexual_violence": [
            "🚨 This is NOT your fault. Help is available.",
            "Call 181 (Women Helpline) or 112 (Police) immediately",
            "Do NOT bathe or change clothes - preserve evidence",
            "Go to nearest hospital/One Stop Centre for medical examination",
            "You will get free legal aid and counseling",
            "Complaint can be filed at ANY police station (no jurisdiction needed)"
        ],
        "child_safety": [
            "🚨 Child safety is paramount. Call 1098 (Child Helpline)",
            "Under POCSO: Every adult MUST report child sexual abuse",
            "Child's statement can be recorded at home/safe place",
            "Special court ensures privacy and fast trial",
            "Free legal aid and counseling for the child and family"
        ]
    }
    
    return instructions.get(emergency_type, [
        "If this is an emergency, please call the relevant helpline immediately",
        "Your safety and wellbeing come first",
        "Free legal aid is available through NALSA/DLSA"
    ])
