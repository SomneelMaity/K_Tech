from fastapi import APIRouter, HTTPException

from ..schemas import DocGenRequest, DocGenResponse
from ..services.docgen_service import generate_document

router = APIRouter(prefix="/api/documents", tags=["documents"])

_DISCLAIMER = (
    "This is a draft document prepared for review only and does not constitute "
    "legal advice. Please verify all details with a qualified legal professional "
    "before use."
)


@router.post("/generate", response_model=DocGenResponse)
def generate(req: DocGenRequest):
    try:
        result = generate_document(
            segment=req.segment,
            doc_type=req.doc_type,
            variables=req.variables,
            language=req.language,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document generation failed: {e}")

    return DocGenResponse(
        document_id=result["document_id"],
        file_url=result["file_url"],
        doc_type=req.doc_type,
        disclaimer=_DISCLAIMER,
    )
