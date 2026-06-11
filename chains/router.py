class QueryRouter:

    def route(self, query: str):

        query = query.lower()

        if "balance" in query:
            return "tool"

        if "fraud" in query:
            return "hitl"

        return "rag"