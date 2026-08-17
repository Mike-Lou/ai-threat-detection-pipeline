import json
import time

def create_alert(row_index, score, threshold):
    """
    Creates a JSON-style alert dictionary.
    """
    severity = compute_severity(score, threshold)

    alert = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "row_index": row_index,
        "score": float(score),
        "threshold": float(threshold),
        "severity": severity,
        "message": f"Anomaly detected at row {row_index}"
    }

    return alert

def compute_severity(score, threshold):
    """
    Severity increases as score exceeds threshold.
    """
    ratio = score / threshold

    if ratio < 1.2:
        return "low"
    elif ratio < 2.0:
        return "medium"
    else:
        return "high"


def save_alerts(alerts, path="alerts.json"):
    """
    Saves all alerts to a JSON file.
    """
    with open(path, "w") as f:
        json.dump(alerts, f, indent=4)
