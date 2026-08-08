from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator

# Supported language codes (ISO 639-1)
SUPPORTED_LANGUAGES = {"en", "hi", "bn", "te", "mr", "ta", "gu", "kn", "pa", "ur"}


def detect_language(text: str) -> str:
    """Return ISO 639-1 language code; fall back to 'en' on failure."""
    try:
        code = detect(text)
        return code if code in SUPPORTED_LANGUAGES else "en"
    except LangDetectException:
        return "en"


def translate_to_english(text: str, source_lang: str) -> str:
    """Translate text to English for RAG retrieval. No-op if already English."""
    if source_lang == "en":
        return text
    try:
        return GoogleTranslator(source=source_lang, target="en").translate(text)
    except Exception:
        return text  # fall back to original on error


def translate_from_english(text: str, target_lang: str) -> str:
    """Translate English answer back to the user's language. No-op if English."""
    if target_lang == "en":
        return text
    try:
        # Split into chunks ≤4500 chars to stay within free-tier limits
        chunks, start = [], 0
        while start < len(text):
            end = min(start + 4500, len(text))
            chunks.append(GoogleTranslator(source="en", target=target_lang).translate(text[start:end]))
            start = end
        return " ".join(chunks)
    except Exception:
        return text
