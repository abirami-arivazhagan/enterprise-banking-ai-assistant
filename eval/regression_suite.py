import json
import os
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from graph.workflow import (
    app_graph
)

from eval.custom_metrics import (
    EvaluationMetrics
)


metrics = EvaluationMetrics()


with open(
    PROJECT_ROOT / "eval" / "golden_set.json",
    "r"
) as file:

    dataset = json.load(file)


results = []


for item in dataset:
    result = app_graph.invoke({
        "query": item["query"],
        "user_role": "l1_agent",
        "metadata": {}
    })

    generated = result[
        "final_response"
    ]

    similarity = (
        metrics.answer_similarity(
            item["expected"],
            generated
        )
    )

    citation_score = (
        int(
            bool(
                result.get(
                    "citations"
                )
            )
        )
    )

    results.append({
        "query": item["query"],
        "expected":
            item["expected"],
        "generated":
            generated,
        "similarity":
            similarity,
        "citation_score":
            citation_score
    })


report = {
    "generated_at": datetime.utcnow().isoformat(),
    "total_cases": len(results),
    "results": results
}


os.makedirs(
    PROJECT_ROOT / "reports",
    exist_ok=True
)


with open(
    PROJECT_ROOT / "reports" / "eval_results.json",
    "w"
) as file:

    json.dump(
        report,
        file,
        indent=4
    )
