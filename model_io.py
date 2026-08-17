import torch
import json
from datetime import datetime


def save_model(model, scaler, numeric_cols, path="saved_model.pth"):
    # Convert numeric_cols to a plain list before saving
    numeric_cols = list(numeric_cols)

    payload = {
        "model_state": model.state_dict(),
        "numeric_cols": numeric_cols,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    torch.save(payload, path)
    torch.save(scaler, "saved_scaler.pth")

    metadata = {
        "version": "1.0",
        "saved_at": payload["timestamp"],
        "numeric_cols": numeric_cols
    }

    with open("model_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)

    return metadata



def load_model(model_class, model_path="saved_model.pth", scaler_path="saved_scaler.pth"):
    payload = torch.load(model_path)
    scaler = torch.load(scaler_path)

    model = model_class(len(payload["numeric_cols"]))
    model.load_state_dict(payload["model_state"])
    model.eval()

    return model, scaler, payload["numeric_cols"]
