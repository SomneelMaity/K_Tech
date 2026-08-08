import json

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

# Keywords that trigger immediate helpline-first response (English + Hindi transliterations)
_EMERGENCY_KEYWORDS = [
    # Violence / domestic abuse
    "beat", "beating", "hit me", "violence", "assault", "abuse",
    "maar raha", "maar rahi", "maar diya", "pitai", "hinsa",
    # Threats to life
    "kill", "murder", "death threat", "jaan se maarna", "jaan lena",
    # Suicide / self-harm
    "suicide", "self harm", "want to die", "marna chahta", "marna chahti",
    # Arrest / police custody
    "arrested", "in custody", "locked up", "giraftaar",
    # Sexual violence
    "rape", "sexual assault", "molest",
    # Child abuse
    "child abuse", "bacche ke saath",
    # Digital arrest scam (golden-hour)
    "digital arrest", "fake police", "cyber arrest",
]

_HELPLINES = [
    {"label": "Police", "number": "100"},
    {"label": "Women Helpline", "number": "181"},
    {"label": "Child Helpline", "number": "1098"},
    {"label": "Cyber Crime / Fraud (golden hour)", "number": "1930"},
    {"label": "Senior Citizens", "number": "14567"},
    {"label": "NALSA Free Legal Aid", "number": "1516"},
]

_SAFETY_ANSWER = (
    "Your safety comes first. Please contact one of the helplines below immediately. "
    "They provide free, confidential help 24/7. You do not need a lawyer to call them."
)


def _is_emergency(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in _EMERGENCY_KEYWORDS)


class SafetyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Only inspect chat POST requests
        if request.method == "POST" and request.url.path == "/api/chat":
            body = await request.body()
            try:
                payload = json.loads(body)
                message = payload.get("message", "")
            except (json.JSONDecodeError, AttributeError):
                message = ""

            if _is_emergency(message):
                return JSONResponse({
                    "conversation_id": "",
                    "answer": _SAFETY_ANSWER,
                    "citations": [],
                    "disclaimer": "",
                    "emergency_resources": _HELPLINES,
                })

            # Re-attach body so the router can still read it
            async def receive():
                return {"type": "http.request", "body": body}
            request = Request(request.scope, receive)

        return await call_next(request)
