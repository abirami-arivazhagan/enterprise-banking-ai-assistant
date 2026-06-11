class ResponseChain:
    def invoke(self, state: dict):
        response = state.get(
            "response",
            ""
        )
        citations = state.get(
            "citations",
            []
        )
        if citations:
            response += "\n\nSources:\n"
            for idx, citation in enumerate(
                citations,
                1
            ):
                response += (
                    f"{idx}. "
                    f"{citation['source']}\n"
                )
        return {
            "final_response": response
        }