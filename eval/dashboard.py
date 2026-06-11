import json
import pandas as pd
import streamlit as st


st.title(
    "Evaluation Dashboard"
)
with open(
    "reports/eval_results.json",
    "r"
) as file:

    data = json.load(file)

dataframe = pd.DataFrame(data)
st.dataframe(dataframe)
st.metric(
    "Average Similarity",
    round(
        dataframe[
            "similarity"
        ].mean(),
        2
    )
)