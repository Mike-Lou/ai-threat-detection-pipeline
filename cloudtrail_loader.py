import json
import pandas as pd


def load_cloudtrail(path):
    rows = []
    with open(path, "r") as f:
        data = json.load(f)
        for event in data["Records"]:
            rows.append(event)
    return pd.DataFrame(rows)
