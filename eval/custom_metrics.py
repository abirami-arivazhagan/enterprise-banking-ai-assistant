from difflib import SequenceMatcher


class EvaluationMetrics:
    def answer_similarity(
        self,
        expected,
        generated
    ):
        return SequenceMatcher(
            None,
            expected,
            generated

        ).ratio()
    def role_compliance(
        self,
        role,
        response
    ):
        restricted_keywords = [
            "internal",
            "confidential"
        ]
        if role == "customer":
            for keyword in (
                restricted_keywords
            ):
                if keyword in (
                    response.lower()
                ):

                    return 0

        return 1

    def citation_presence(
        self,
        response
    ):

        return int(
            "Sources:" in response
        )

    def hitl_precision(
        self,
        requires_hitl,
        confidence_score
    ):

        if (
            confidence_score < 0.75
            and requires_hitl
        ):

            return 1

        return 0