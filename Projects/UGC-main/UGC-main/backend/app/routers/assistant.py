import anthropic
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..schemas import AssistantChatRequest, AssistantChatResponse
from ..services import assistant_service

router = APIRouter(prefix="/api/assistant", tags=["assistant"])


@router.post("/chat", response_model=AssistantChatResponse)
async def chat(
    req: AssistantChatRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if not settings.has_anthropic:
        raise HTTPException(
            status_code=503,
            detail="Voice assistant needs ANTHROPIC_API_KEY in backend/.env",
        )
    try:
        reply, generation_id = await assistant_service.run_turn(
            [m.model_dump() for m in req.messages], db, background_tasks
        )
    except anthropic.AuthenticationError:
        raise HTTPException(
            status_code=502,
            detail="The Anthropic API rejected your key. Check ANTHROPIC_API_KEY in backend/.env",
        )
    except anthropic.APIError as e:
        raise HTTPException(status_code=502, detail=f"Anthropic API error: {e}")
    return AssistantChatResponse(reply=reply, generation_id=generation_id)
