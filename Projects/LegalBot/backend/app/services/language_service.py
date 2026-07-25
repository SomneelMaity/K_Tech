"""
Language detection and translation service
"""
from typing import Optional
from loguru import logger
import httpx

from app.core.config import settings


def detect_language(text: str) -> str:
    """
    Detect language of input text
    
    For now, uses simple heuristics. In production, would use:
    - Bhashini API
    - Google Language Detection
    - fastText language identification
    """
    # Simple Hindi detection (checks for Devanagari script)
    if any('\u0900' <= char <= '\u097F' for char in text):
        return "hi"
    
    # Bengali
    if any('\u0980' <= char <= '\u09FF' for char in text):
        return "bn"
    
    # Telugu
    if any('\u0C00' <= char <= '\u0C7F' for char in text):
        return "te"
    
    # Tamil
    if any('\u0B80' <= char <= '\u0BFF' for char in text):
        return "ta"
    
    # Gujarati
    if any('\u0A80' <= char <= '\u0AFF' for char in text):
        return "gu"
    
    # Kannada
    if any('\u0C80' <= char <= '\u0CFF' for char in text):
        return "kn"
    
    # Malayalam
    if any('\u0D00' <= char <= '\u0D7F' for char in text):
        return "ml"
    
    # Punjabi
    if any('\u0A00' <= char <= '\u0A7F' for char in text):
        return "pa"
    
    # Default to English
    return "en"


async def translate_text(
    text: str,
    source_lang: str,
    target_lang: str
) -> str:
    """
    Translate text using Bhashini API
    
    Falls back to returning original text if translation fails
    """
    if source_lang == target_lang:
        return text
    
    try:
        if settings.BHASHINI_API_KEY:
            # Use Bhashini API
            return await _translate_bhashini(text, source_lang, target_lang)
        else:
            logger.warning("Bhashini API key not configured, returning original text")
            return text
            
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        return text


async def _translate_bhashini(
    text: str,
    source_lang: str,
    target_lang: str
) -> str:
    """
    Translate using Bhashini (Government of India) API
    
    Bhashini language codes:
    - en: English
    - hi: Hindi
    - bn: Bengali
    - te: Telugu
    - mr: Marathi
    - ta: Tamil
    - gu: Gujarati
    - kn: Kannada
    - ml: Malayalam
    - or: Odia
    - pa: Punjabi
    """
    # TODO: Implement actual Bhashini API integration
    # For now, return placeholder
    logger.info(f"Translation requested: {source_lang} -> {target_lang}")
    return text


async def transliterate_text(
    text: str,
    script: str = "Devanagari"
) -> str:
    """
    Transliterate text to specified script
    Useful for legal terms that need to be in both scripts
    """
    # TODO: Implement transliteration using indic-transliteration
    return text
