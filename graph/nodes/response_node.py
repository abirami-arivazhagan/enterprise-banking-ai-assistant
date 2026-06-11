# =========================================================
# RESPONSE NODE
# =========================================================

def response_node(state):

    answer = state.get(
        "answer"
    )

    citations = [

        citation

        for citation in (
            state.get("citations")
            or
            []
        )

        if citation.get("source")
    ]

    if state.get("tool_used"):

        citations = []

    return {

        "answer":
        answer,

        "final_response":
        answer,

        "citations":
        citations,

        "tool_used":
        state.get("tool_used")
    }
