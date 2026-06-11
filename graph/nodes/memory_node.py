from memory.manager import (
    MemoryManager
)

# =========================================================
# MEMORY MANAGER
# =========================================================

memory_manager = MemoryManager()

# =========================================================
# MEMORY NODE
# =========================================================

def memory_node(state):

    session_id = (
        state.get(
            "session_id"
        )
        or
        "default"
    )

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

    answer = (
        state.get(
            "answer"
        )
        or
        ""
    )

    state["session_id"] = session_id

    state["question"] = question

    memory = (
        memory_manager.get_memory(
            session_id
        )
    )

    # =====================================================
    # SAVE MEMORY
    # =====================================================

    memory.save_context(

        question,

        answer
    )

    state["chat_history"] = (

        memory.load_context()
    )

    return state
