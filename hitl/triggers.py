import yaml


with open(
    "config/hitl_rules.yaml",
    "r"
) as file:

    RULES = yaml.safe_load(file)


def requires_human_review(
    confidence_score
):

    threshold = RULES[
        "rules"
    ][
        "confidence_threshold"
    ]

    return confidence_score < threshold