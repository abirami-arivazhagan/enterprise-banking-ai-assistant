from datetime import datetime
import os
from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    File,
    Form
)

from app.services.chat_service import (
    ChatService
)

from app_tools.complaint_tools import (
    load_complaints
)

router = APIRouter()
chat_service = ChatService()
upload_service = None

@router.get("/")
def home():
    return {
        "message":
        "Enterprise Banking AI Running"
    }
@router.get("/health")
def health():
    return {
        "status": "healthy",
        "vector_store_status":
        "ready" if os.path.exists("faiss_index/index.faiss") else "missing",
        "document_count":
        len(os.listdir("uploads")) if os.path.isdir("uploads") else 0,
        "timestamp":
        datetime.utcnow().isoformat()
    }
@router.post("/chat")
async def chat(
    session_id: str = Form(...),
    message: str = Form(...),
    role: str = Form(
        default="l1_agent"
    )
):
    response = (
        await chat_service.process_chat(
            session_id=session_id,
            message=message,
            role=role
        )
    )
    return response

@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    session_id: str = Form(
        default="default"
    )
):
    global upload_service
    if upload_service is None:
        from app.services.upload_service import (
            UploadService
        )
        upload_service = UploadService()
    try:
        response = (
            await upload_service.upload_document(
                file,
                session_id=session_id
            )
        )
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc
    return response

@router.get("/complaints")
def complaints():
    return {
        "complaints":
        load_complaints()
    }
@router.post("/ingest")
async def ingest(
    file: UploadFile = File(...),
    session_id: str = Form(
        default="default"
    )
):
    return await upload(
        file,
        session_id
    )
