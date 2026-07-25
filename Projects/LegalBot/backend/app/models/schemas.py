"""
Pydantic models for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatMessage(BaseModel):
    """Single chat message"""
    role: str = Field(..., description="Role: user, assistant, system")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = None


class QueryRequest(BaseModel):
    """Request for legal query"""
    query: str = Field(..., min_length=3, max_length=2000, description="User's legal question")
    segment: Optional[str] = Field(None, description="Segment ID (s1-consumer, s2-property, etc.)")
    state: Optional[str] = Field(None, description="Indian state code (DL, MH, KA, etc.)")
    language: str = Field("en", description="Language code (en, hi, bn, etc.)")
    session_id: Optional[str] = None
    context: Optional[List[ChatMessage]] = Field(None, description="Previous messages for context")
    

class SourceDocument(BaseModel):
    """Source document with citation"""
    text: str
    metadata: Dict[str, Any]
    score: float
    

class QueryResponse(BaseModel):
    """Response to legal query"""
    answer: str = Field(..., description="Generated answer")
    sources: List[SourceDocument] = Field(default_factory=list, description="Source documents")
    confidence: str = Field(..., description="Confidence level: high, medium, low")
    disclaimer: str = Field(..., description="Legal disclaimer")
    emergency_detected: bool = Field(False, description="Whether emergency was detected")
    helplines: Optional[List[Dict[str, str]]] = Field(None, description="Relevant helpline numbers")
    suggested_actions: Optional[List[str]] = Field(None, description="Next steps user should take")
    

class DocumentGenerationRequest(BaseModel):
    """Request to generate legal document"""
    template_type: str = Field(..., description="Type: notice, complaint, rti, agreement, etc.")
    segment: str = Field(..., description="Segment ID")
    data: Dict[str, Any] = Field(..., description="Data to fill template")
    format: str = Field("pdf", description="Output format: pdf or docx")
    language: str = Field("en", description="Language code")


class DocumentGenerationResponse(BaseModel):
    """Response with generated document"""
    document_id: str
    download_url: str
    expires_at: datetime
    preview_text: Optional[str] = None


class SegmentInfo(BaseModel):
    """Information about a legal segment"""
    id: str
    name: str
    description: str
    key_laws: List[str]
    portals: List[Dict[str, str]]
    helplines: List[Dict[str, str]]
    difficulty: str
    loaded: bool = False


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    rag_engine: str
    segments_loaded: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
