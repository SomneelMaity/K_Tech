from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Conversation
from ..schemas import ChatRequest, ChatResponse, FeedbackRequest
from ..services.llm_service import get_answer
from ..services.rag_service import retrieve
from ..services.language_service import detect_language, translate_to_english, translate_from_english

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    # Load or create conversation
    if req.conversation_id:
        conv = db.get(Conversation, req.conversation_id)
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conv = Conversation(
            segment=req.segment or "",
            language=req.language,
            state=req.state or "",
            messages=[],
        )
        db.add(conv)
        db.flush()

    # Detect language and translate query to English for RAG
    user_lang = req.language if req.language != "en" else detect_language(req.message)
    query_en = translate_to_english(req.message, user_lang)

    # Retrieve relevant KB chunks
    chunks = retrieve(
        query=query_en,
        segment=req.segment,
        state=req.state,
        top_k=5,
    )

    # Generate grounded answer (always in English first)
    try:
        result = get_answer(
            user_message=query_en,
            chunks=chunks,
            history=conv.messages,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    # Translate answer back to user's language
    answer = translate_from_english(result["answer"], user_lang)

    # Persist messages
    conv.messages = conv.messages + [
        {"role": "user", "content": req.message},
        {"role": "model", "content": answer},
    ]
    conv.retrieved_chunks = chunks
    conv.citations = result["citations"]
    db.commit()

    return ChatResponse(
        conversation_id=conv.id,
        answer=answer,
        citations=result["citations"],
    )


@router.post("/feedback")
def feedback(req: FeedbackRequest, db: Session = Depends(get_db)):
    conv = db.get(Conversation, req.conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conv.feedback_score = req.score
    db.commit()
    return {"status": "ok"}


@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    # Load or create conversation
    if req.conversation_id:
        conv = db.get(Conversation, req.conversation_id)
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conv = Conversation(
            segment=req.segment or "",
            language=req.language,
            state=req.state or "",
            messages=[],
        )
        db.add(conv)
        db.flush()

    # Retrieve relevant KB chunks
    chunks = retrieve(
        query=req.message,
        segment=req.segment,
        state=req.state,
        top_k=5,
    )

    # Generate grounded answer
    result = get_answer(
        user_message=req.message,
        chunks=chunks,
        history=conv.messages,
    )

    # Persist messages
    conv.messages = conv.messages + [
        {"role": "user", "content": req.message},
        {"role": "model", "content": result["answer"]},
    ]
    conv.retrieved_chunks = chunks
    conv.citations = result["citations"]
    db.commit()

    return ChatResponse(
        conversation_id=conv.id,
        answer=result["answer"],
        citations=result["citations"],
    )


@router.post("/feedback")
def feedback(req: FeedbackRequest, db: Session = Depends(get_db)):
    conv = db.get(Conversation, req.conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conv.feedback_score = req.score
    db.commit()
    return {"status": "ok"}

