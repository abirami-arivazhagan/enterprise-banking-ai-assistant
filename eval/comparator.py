import json


class ResultComparator:
    def compare_runs(
        self,
        old_file,
        new_file
    ):
        with open(
            old_file,
            "r"
        ) as file:

            old_results = json.load(
                file
            )
        with open(
            new_file,
            "r"
        ) as file:
            new_results = json.load(
                file
            )
        comparison = []
        for old, new in zip(
            old_results,
            new_results
        ):
            comparison.append({
                "query":
                    old["query"],

                "old_score":
                    old["similarity"],

                "new_score":
                    new["similarity"]
            })

        return comparison