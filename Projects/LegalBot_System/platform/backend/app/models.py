import datetime
import uuid

from sqlalchemy import Column, DateTime, Integer, JSON, String, Text

from .database import Base


def _uuid() -> str:
    return uuid.uuid4().hex


class Conversation(Base):
    """One user session / conversation thread."""

    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=_uuid)

    # Context
    segment = Column(String, default="")          
    language = Column(String, default="en")       
    state = Column(String, default="")            

    # Messages stored as list of {role, content} dicts
    messages = Column(JSON, default=list)

    # RAG
    retrieved_chunks = Column(JSON, default=list) # last retrieval for audit
    citations = Column(JSON, default=list)        # cited KB entries in last answer

    # Feedback
    feedback_score = Column(Integer, default=0)   # thumbs: +1 / -1 / 0

    # Bookkeeping
    # active | closed
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class Document(Base):
    """A generated legal document (notice, complaint, RTI, template)."""

    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=_uuid)
    conversation_id = Column(String, default="")
    segment = Column(String, default="")
    doc_type = Column(String, default="")         # demand_letter | complaint | agreement | ...
    language = Column(String, default="en")
    file_path = Column(String, default="")        # path under UPLOAD_DIR
    template_used = Column(String, default="")
    variables = Column(JSON, default=dict)        # data merged into template
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
