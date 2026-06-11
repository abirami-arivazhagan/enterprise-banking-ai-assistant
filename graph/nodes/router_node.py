# =========================================================
# ROUTER NODE
# =========================================================

from memory.dialog_state import (
    dialog_state_store
)

from graph.nodes.memory_node import (
    memory_manager
)


def router_node(state):

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

    question = (
        question
        .lower()
    )

    session_id = (
        state.get(
            "session_id"
        )
        or
        "default"
    )

    dialog_state = dialog_state_store.get(
        session_id
    )

    state["chat_history"] = (
        memory_manager
        .get_memory(
            session_id
        )
        .load_context()
    )

    def has_action_complaint_intent():

        return (
            "complaint" in question
            and
            (
                "raise" in question
                or
                "create" in question
                or
                "register" in question
                or
                "file a complaint" in question
                or
                "list" in question
                or
                "complaint number" in question
                or
                "ticket" in question
            )
        )

    # =====================================================
    # TOOL ROUTING
    # =====================================================

    if dialog_state.get("pending") in [
        "complaint_issue",
        "complaint_details"
    ]:

        state["route"] = "tool"

    elif (

        question.strip()
        in
        [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ]

    ):

        state["route"] = "tool"

    elif (

        "block" in question
        and
        "card" in question

    ):

        state["route"] = "tool"

    elif has_action_complaint_intent():

        state["route"] = "tool"

    elif (

        "loan" in question
        and
        (
            "eligibility" in question
            or
            "eligible" in question
            or
            "calculate" in question
        )

    ):

        state["route"] = "tool"

    elif (

        "unblock" in question
        or
        "blocked account" in question
        or
        "account blocked" in question
        or
        "frozen account" in question
        or
        "account frozen" in question

    ):

        state["route"] = "tool"

    else:

        state["route"] = "rag"

    print(
        f"\n[ROUTER] "
        f"Route Selected: "
        f"{state['route']}\n"
    )

    return state
