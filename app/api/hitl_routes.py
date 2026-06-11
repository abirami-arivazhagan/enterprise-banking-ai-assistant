from fastapi import APIRouter
from pydantic import BaseModel
from hitl.manager import (
    HITLManager
)

router = APIRouter()
manager = HITLManager()

class HITLReviewRequest(
    BaseModel
):
    decision: str


class HITLCreateRequest(
    BaseModel
):
    query: str
    response: str
    confidence_score: float = 0.5

@router.get("/hitl/pending")
def pending_tasks():
    return manager.get_pending_tasks()


@router.post("/hitl/create")
def create_task(
    payload: HITLCreateRequest
):
    return manager.create_review_task(
        payload.model_dump()
    )

@router.post(
    "/hitl/review/{task_id}"
)

def review_task(
    task_id: str,
    payload: HITLReviewRequest
):
    manager.review_task(
        task_id,
        payload.decision
    )
    return {
        "status": "updated"
    }
