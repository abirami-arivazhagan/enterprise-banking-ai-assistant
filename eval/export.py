import json
import pandas as pd


def export_eval_report():
    with open(
        "reports/eval_results.json",
        "r"
    ) as file:
        data = json.load(file)
    dataframe = pd.DataFrame(
        data
    )
    dataframe.to_csv(
        "reports/eval_results.csv",
        index=False
    )