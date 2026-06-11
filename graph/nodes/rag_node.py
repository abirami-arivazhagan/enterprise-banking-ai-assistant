retrieval_service = None

from memory.upload_context import (
    upload_context_store
)

# =========================================================
# EXECUTE RAG
# =========================================================

def rag_node(state):

    global retrieval_service

    question = (
        state.get(
            "question"
        )
        or
        state.get(
            "query",
            ""
        )
    )

    state["question"] = question

    latest_upload = upload_context_store.get_latest(
        state.get(
            "session_id",
            "default"
        )
    )

    if (
        latest_upload
        and
        question.strip().lower() in [
            "facing this issue",
            "i am facing this issue",
            "i'm facing this issue",
            "this issue",
            "same issue"
        ]
    ):

        question = (
            "The user is referring to the latest uploaded file. "
            f"File: {latest_upload.get('filename')}. "
            f"Extracted text: {latest_upload.get('preview', '')}. "
            "Explain what the issue appears to be and guide the user on the safest next step."
        )

        state["question"] = question

    if retrieval_service is None:

        from app.services.retrieval_service import (
            RetrievalService
        )

        retrieval_service = RetrievalService()

    response = (
        retrieval_service.ask(
            question,
            chat_history=state.get(
                "chat_history",
                []
            ),
            role=state.get(
                "user_role",
                "l1_agent"
            )
        )
    )

    state["answer"] = (
        response["answer"]
    )

    state["citations"] = (
        response["citations"]
    )

    return state
