from google import genai
from google.genai import types
from google.genai.errors import ClientError

from ..config import settings

_DISCLAIMER = (
    "This information is for general awareness only and does not constitute "
    "legal advice. For matters involving significant money, criminal proceedings, "
    "or personal safety, please consult a qualified lawyer. Free legal aid is "
    "available through NALSA (1516) and your District Legal Services Authority."
)

_SYSTEM_PROMPT = """
You are LegalBot, an AI legal information assistant for Indian citizens.
You ONLY answer using the retrieved knowledge-base excerpts provided below.
Rules you must follow without exception:
1. Never cite a section number, act, fee, or deadline that is not present in the retrieved excerpts.
2. If the retrieved excerpts do not contain enough information, say exactly: "I don\'t have verified information on this. Please consult a lawyer or call NALSA on 1516."
3. Always write at an 8th-grade reading level in the language of the user\'s question.
4. End every answer with the disclaimer provided.
5. Suggest the most relevant free government helpline or portal where applicable.
"""


def _build_context(chunks: list[dict]) -> str:
    if not chunks:
        return "No relevant excerpts retrieved."
    parts = []
    for i, c in enumerate(chunks, 1):
        parts.append(
            f"[{i}] {c.get('title', '')} ({c.get('act', '')} {c.get('section', '')})\n"
            f"{c.get('content', '')}"
        )
    return "\n\n".join(parts)


def get_answer(user_message: str, chunks: list[dict], history: list[dict]) -> dict:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    context_block = _build_context(chunks)
    prompt = (
        f"RETRIEVED KNOWLEDGE-BASE EXCERPTS:\n{context_block}\n\n"
        f"USER QUESTION: {user_message}\n\n"
        f"Answer strictly from the excerpts above. Append this disclaimer at the end:\n{_DISCLAIMER}"
    )

    gemini_history = [
        types.Content(role=m["role"], parts=[types.Part(text=m["content"])])
        for m in history
        if m["role"] in ("user", "model")
    ]
    gemini_history.append(
        types.Content(role="user", parts=[types.Part(text=prompt)])
    )

    try:
        response = client.models.generate_content(
            model=settings.CHAT_MODEL,
            contents=gemini_history,
            config=types.GenerateContentConfig(system_instruction=_SYSTEM_PROMPT),
        )
        answer = response.text
    except ClientError as e:
        status = getattr(e, 'status_code', 0)
        if status == 429:
            raise RuntimeError("AI service quota exceeded. Please check your Gemini API key at https://aistudio.google.com/app/apikey and ensure it has free-tier access.")
        raise RuntimeError(f"AI service error ({status}): {e}")

    citations = [
        {
            "entry_id": c.get("entry_id", ""),
            "title": c.get("title", ""),
            "act": c.get("act", ""),
            "section": c.get("section", ""),
            "source_url": c.get("source_url", ""),
        }
        for c in chunks
    ]
    return {"answer": answer, "citations": citations}
