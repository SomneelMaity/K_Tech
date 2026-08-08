import os
import uuid
from io import BytesIO
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from xhtml2pdf import pisa

from ..config import settings


def _get_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(settings.TEMPLATES_DIR),
        autoescape=select_autoescape(["html"]),
    )


_TEMPLATE_MAP = {
    "demand_letter": "s5_demand_letter.html",
    "cheque_bounce_notice": "s10_cheque_bounce_notice.html",
}


def generate_document(segment: str, doc_type: str, variables: dict, language: str = "en") -> dict:
    template_name = _TEMPLATE_MAP.get(doc_type)
    if not template_name:
        raise ValueError(f"Unknown doc_type: {doc_type}")

    env = _get_env()
    template = env.get_template(template_name)
    html_content = template.render(**variables, language=language)

    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    doc_id = uuid.uuid4().hex
    filename = f"{doc_id}.pdf"
    file_path = str(Path(settings.OUTPUT_DIR) / filename)

    with open(file_path, "wb") as pdf_file:
        result = pisa.CreatePDF(BytesIO(html_content.encode("utf-8")), dest=pdf_file)

    if result.err:
        raise RuntimeError("PDF generation failed")

    return {"document_id": doc_id, "file_path": file_path, "file_url": f"/storage/docs/{filename}"}
