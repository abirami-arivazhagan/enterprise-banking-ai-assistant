from app.core.security import (
    validate_query,
    mask_sensitive_data,
    contains_pii
)

from graph.workflow import (
    app_graph
)

class ChatService:
    def __init__(self):
        pass
    async def process_chat(
        self,
        session_id,
        message,
        role="l1_agent"
    ):
        try:
            if not validate_query(message):
                return {
                    "answer":
                    "Unsafe query detected."
                }
            pii_masked = contains_pii(
                message
            )
            message = mask_sensitive_data(
                message
            )
            initial_state = {
                "question": message,
                "session_id": session_id,
                "user_role": role,
                "route": None,
                "retrieved_docs": [],
                "answer": None,
                "citations": [],
                "tool_used": None,
                "chat_history": []
            }
            response = app_graph.invoke(
                initial_state
            )
            response["pii_masked"] = pii_masked
            return response
        except Exception as e:
            print(f"\n[CHAT ERROR] {e}\n")
            return {
                "answer":
                "Internal server error.",
                "error": str(e)
            }
