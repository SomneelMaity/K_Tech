"""
Segments endpoints - Information about legal segments
"""
from fastapi import APIRouter
from typing import List

from app.models.schemas import SegmentInfo
from app.core.rag_engine import rag_engine

router = APIRouter()


# Segment definitions
SEGMENTS_DATA = [
    {
        "id": "s1-consumer",
        "name": "Consumer & E-commerce",
        "description": "Consumer rights, defective products, refunds, e-commerce disputes, builder delays",
        "key_laws": ["Consumer Protection Act 2019", "e-Jagriti Portal", "NCH 1915"],
        "portals": [
            {"name": "e-Jagriti", "url": "https://jagriti.gov.in"},
            {"name": "Consumer Helpline", "url": "https://consumerhelpline.gov.in"}
        ],
        "helplines": [
            {"name": "National Consumer Helpline", "number": "1915"}
        ],
        "difficulty": "Easy-Medium"
    },
    {
        "id": "s2-property",
        "name": "Property, Land & Tenancy",
        "description": "Property disputes, title verification, RERA, rent agreements, succession",
        "key_laws": ["Transfer of Property Act", "RERA 2016", "Registration Act"],
        "portals": [
            {"name": "RERA Portal", "url": "https://rera.gov.in"}
        ],
        "helplines": [],
        "difficulty": "Hard"
    },
    {
        "id": "s3-family",
        "name": "Family Law & Maintenance",
        "description": "Divorce, maintenance, custody, domestic violence, marriage laws",
        "key_laws": ["Hindu Marriage Act", "PWDVA 2005", "BNSS §144"],
        "portals": [],
        "helplines": [
            {"name": "Women in Distress", "number": "181"}
        ],
        "difficulty": "Hard"
    },
    {
        "id": "s4-cybercrime",
        "name": "Cyber Crime Response",
        "description": "Online fraud, UPI scams, digital arrest, hacking, sextortion",
        "key_laws": ["IT Act 2000", "BNS 2023"],
        "portals": [
            {"name": "Cybercrime Portal", "url": "https://cybercrime.gov.in"}
        ],
        "helplines": [
            {"name": "Cybercrime Helpline", "number": "1930"}
        ],
        "difficulty": "Medium"
    },
    {
        "id": "s5-employment",
        "name": "Employment & Labour",
        "description": "Salary disputes, termination, PF, gratuity, workplace harassment",
        "key_laws": ["Code on Wages", "POSH Act 2013", "PF/ESI Acts"],
        "portals": [],
        "helplines": [],
        "difficulty": "Medium"
    },
    {
        "id": "s6-police",
        "name": "Police, FIR & Bail",
        "description": "FIR filing, arrest rights, bail procedures, police complaints",
        "key_laws": ["BNS 2023", "BNSS 2023", "BSA 2023"],
        "portals": [],
        "helplines": [],
        "difficulty": "Hard"
    },
    {
        "id": "s7-women-child",
        "name": "Women & Child Safety",
        "description": "Domestic violence, child safety, POCSO, protection orders",
        "key_laws": ["PWDVA", "POCSO 2012", "POSH"],
        "portals": [],
        "helplines": [
            {"name": "Women Helpline", "number": "181"},
            {"name": "Child Helpline", "number": "1098"}
        ],
        "difficulty": "Hard"
    },
    {
        "id": "s8-seniors",
        "name": "Senior Citizens",
        "description": "Maintenance, elder abuse, pension, property rights",
        "key_laws": ["MWPSC Act 2007"],
        "portals": [],
        "helplines": [
            {"name": "Elder Helpline", "number": "14567"}
        ],
        "difficulty": "Easy-Medium"
    },
    {
        "id": "s9-rti",
        "name": "RTI & Govt Services",
        "description": "RTI applications, government schemes, traffic challans",
        "key_laws": ["RTI Act 2005", "Motor Vehicles Act"],
        "portals": [],
        "helplines": [],
        "difficulty": "Easy"
    },
    {
        "id": "s10-msme",
        "name": "MSME & Small Business",
        "description": "Payment delays, Samadhaan, licenses, contracts, cheque bounce",
        "key_laws": ["MSMED Act 2006", "NI Act §138"],
        "portals": [
            {"name": "Samadhaan", "url": "https://samadhaan.msme.gov.in"}
        ],
        "helplines": [],
        "difficulty": "Medium"
    }
]


@router.get("/", response_model=List[SegmentInfo])
async def get_all_segments():
    """Get information about all legal segments"""
    segments = []
    for seg_data in SEGMENTS_DATA:
        seg_info = SegmentInfo(**seg_data)
        seg_info.loaded = seg_data["id"] in rag_engine.loaded_segments
        segments.append(seg_info)
    
    return segments


@router.get("/{segment_id}", response_model=SegmentInfo)
async def get_segment(segment_id: str):
    """Get information about a specific segment"""
    for seg_data in SEGMENTS_DATA:
        if seg_data["id"] == segment_id:
            seg_info = SegmentInfo(**seg_data)
            seg_info.loaded = segment_id in rag_engine.loaded_segments
            return seg_info
    
    return {"error": "Segment not found"}
