from typing import Any, Optional

from pydantic import BaseModel, Field


# ── Chat / Conversation ────────────────────────────────────────────────────────

class Message(BaseModel):
    role: str = Field(description="'user' or 'assistant'")
    content: str


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str
    segment: Optional[str] = None   # s5-employment | s10-msme
    language: str = "en"
    state: Optional[str] = None     # Indian state for state-specific law


class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
    citations: list[dict[str, Any]] = []
    disclaimer: str = (
        "This information is for general awareness only and does not constitute "
        "legal advice. For matters involving significant money, criminal proceedings, "
        "or personal safety, please consult a qualified lawyer. Free legal aid is "
        "available through NALSA (1516) and your District Legal Services Authority."
    )
    emergency_resources: list[dict[str, str]] = []


class FeedbackRequest(BaseModel):
    conversation_id: str
    score: int = Field(description="+1 (helpful) or -1 (not helpful)")


# ── Document Generation ────────────────────────────────────────────────────────

class DocGenRequest(BaseModel):
    conversation_id: Optional[str] = None
    segment: str
    doc_type: str
    language: str = "en"
    variables: dict[str, Any] = {}


class DocGenResponse(BaseModel):
    document_id: str
    file_url: str
    doc_type: str
    disclaimer: str = (
        "This is a draft document prepared for review. Please verify all details "
        "with a qualified legal professional before use."
    )


# ── RAG / Knowledge Base ───────────────────────────────────────────────────────

class KBEntry(BaseModel):
    entry_id: str
    segment: str
    title: str
    content: str
    act: str = ""
    section: str = ""
    state: str = "all"
    language: str = "en"
    last_verified: str = ""
    source_url: str = ""


class RetrievalResult(BaseModel):
    entry_id: str
    title: str
    content: str
    score: float
    act: str = ""
    section: str = ""
    source_url: str = ""


# ── Health ─────────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    anthropic_configured: bool
    bhashini_configured: bool
    vector_store: str
    chat_model: str
