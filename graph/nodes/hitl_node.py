from hitl.manager import (
    HITLManager
)

from hitl.triggers import (
    requires_human_review
)


manager = HITLManager()


def hitl_node(state):

    confidence_score = state.get(
        "confidence_score",
        0.5
    )

    should_pause = (
        requires_human_review(
            confidence_score
        )
    )

    if should_pause:

        task = manager.create_review_task({

            "query":
                state["query"],

            "response":
                state["response"],

            "confidence_score":
                confidence_score
        })

        state["requires_hitl"] = True

        state["hitl_task_id"] = (
            task["task_id"]
        )

    return state