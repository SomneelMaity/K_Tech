import datetime
import uuid

from sqlalchemy import Column, DateTime, Integer, JSON, String, Text

from .database import Base


def _uuid() -> str:
    return uuid.uuid4().hex


class Generation(Base):
    """One end-to-end run of the Content-to-Post pipeline."""

    __tablename__ = "generations"

    id = Column(String, primary_key=True, default=_uuid)

    # --- input ---
    idea = Column(Text, nullable=False)
    platform = Column(String, default="instagram")
    tone = Column(String, default="friendly")
    image_style = Column(String, default="photo")

    # --- strategy stage ---
    angle = Column(Text, default="")
    audience = Column(Text, default="")

    # --- copy stage (chosen variant on the row, all variants in `variants`) ---
    hook = Column(Text, default="")
    caption = Column(Text, default="")
    hashtags = Column(JSON, default=list)
    variants = Column(JSON, default=list)
    image_prompt = Column(Text, default="")

    # --- image stage ---
    image_url = Column(String, default="")
    image_aspect = Column(String, default="1:1")

    # --- campaign planning ---
    campaign_plan = Column(JSON, default=dict)
    automation_runs = Column(JSON, default=list)

    # --- bookkeeping ---
    # queued | researching | writing | rendering | complete | error
    status = Column(String, default="queued")
    failed_stage = Column(String, default="")  # strategy | copy | image
    error = Column(Text, default="")
    duration_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
