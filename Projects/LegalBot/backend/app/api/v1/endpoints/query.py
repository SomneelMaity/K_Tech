"""
Query endpoints - Main chat/Q&A functionality
"""
from fastapi import APIRouter, HTTPException, Depends
from loguru import logger

from app.models.schemas import QueryRequest, QueryResponse
from app.core.rag_engine import rag_engine
from app.services.language_service import detect_language, translate_text
from app.services.safety_service import detect_emergency, get_relevant_helplines

router = APIRouter()


@router.post("/", response_model=QueryResponse)
async def query_legal_question(request: QueryRequest):
    """
    Main endpoint: Ask a legal question and get an answer
    
    This endpoint:
    1. Detects language and translates if needed
    2. Checks for emergency situations
    3. Retrieves relevant legal information
    4. Generates a grounded answer with citations
    5. Returns with disclaimer and helplines if applicable
    """
    try:
        # Detect language if not provided
        if request.language == "en":
            detected_lang = detect_language(request.query)
            if detected_lang != "en":
                request.language = detected_lang
                logger.info(f"Detected language: {detected_lang}")
        
        # Translate query to English for processing if needed
        query_en = request.query
        if request.language != "en":
            query_en = await translate_text(request.query, request.language, "en")
            logger.info(f"Translated query: {query_en}")
        
        # Check for emergency situations
        emergency_info = detect_emergency(query_en)
        
        # If emergency, prioritize helplines
        if emergency_info["is_emergency"]:
            logger.warning(f"Emergency detected: {emergency_info['type']}")
            helplines = get_relevant_helplines(emergency_info["type"], request.state)
            
            # Still provide answer, but flag as emergency
            result = await rag_engine.query(
                query_text=query_en,
                segment=request.segment,
                state=request.state,
                language=request.language
            )
            
            result["emergency_detected"] = True
            result["helplines"] = helplines
            
            # Prepend emergency notice to answer
            emergency_notice = "⚠️ URGENT: This appears to be an emergency situation. "
            if helplines:
                emergency_notice += f"Immediately call {helplines[0]['number']} ({helplines[0]['name']}). "
            result["answer"] = emergency_notice + result["answer"]
            
            return QueryResponse(**result)
        
        # Normal query flow
        result = await rag_engine.query(
            query_text=query_en,
            segment=request.segment,
            state=request.state,
            language=request.language
        )
        
        # Translate answer back if needed
        if request.language != "en":
            result["answer"] = await translate_text(result["answer"], "en", request.language)
        
        # Add relevant helplines based on segment
        if request.segment:
            result["helplines"] = get_relevant_helplines(request.segment, request.state)
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {str(e)}"
        )


@router.post("/classify")
async def classify_query(query: str):
    """
    Classify a query into one of the 10 segments
    Useful for routing and UI
    """
    # TODO: Implement classification
    # For now, return a placeholder
    return {
        "query": query,
        "segment": "s1-consumer",  # Placeholder
        "confidence": 0.85
    }
