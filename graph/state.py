from typing import TypedDict
from typing import List
from typing import Optional
from typing import Dict
from typing import Any

# =========================================================
# GRAPH STATE
# =========================================================

class GraphState(TypedDict, total=False):

    # =====================================================
    # USER INPUT
    # =====================================================

    question: str

    session_id: str

    query: str

    user_role: str

    metadata: Dict[str, Any]

    # =====================================================
    # ROUTING
    # =====================================================

    route: Optional[str]

    # =====================================================
    # RAG
    # =====================================================

    retrieved_docs: Optional[List]

    # =====================================================
    # RESPONSE
    # =====================================================

    answer: Optional[str]

    final_response: Optional[str]

    citations: Optional[List]

    # =====================================================
    # TOOLS
    # =====================================================

    tool_used: Optional[str]

    # =====================================================
    # MEMORY
    # =====================================================

    chat_history: Optional[List]
