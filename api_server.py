from fastapi import FastAPI
from api_models import ScoreRequest, ScoreResponse
from api_utils import run_scoring

from model_io import save_model, load_model
from model import Autoencoder
import api_utils
from model_io import save_model

# from api_utils import _cached_model, _cached_scaler, _cached_numeric_cols

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/score", response_model=ScoreResponse)
def score_logs(request: ScoreRequest):
    logs = [log.dict() for log in request.logs]
    scores, anomalies, alerts = run_scoring(logs)
    return ScoreResponse(scores=scores, anomalies=anomalies, alerts=alerts)

@app.get("/model-info")
def model_info():
    return {
        "model": "Autoencoder",
        "version": "1.0",
        "description": "Anomaly detection model for security logs"
    }


@app.post("/save-model")
def save_current_model():
    if api_utils._cached_model is None:
        return {"error": "No model loaded"}
    metadata = save_model(
        api_utils._cached_model,
        api_utils._cached_scaler,
        api_utils._cached_numeric_cols
    )
    return {"status": "saved", "metadata": metadata}


@app.post("/load-model")
def load_saved_model():
    global _cached_model, _cached_scaler, _cached_numeric_cols
    model, scaler, numeric_cols = load_model(Autoencoder)
    _cached_model = model
    _cached_scaler = scaler
    _cached_numeric_cols = numeric_cols
    return {"status": "loaded", "numeric_cols": numeric_cols}

@app.get("/model-version")
def model_version():
    import json
    try:
        with open("model_metadata.json") as f:
            metadata = json.load(f)
        return metadata
    except:
        return {"error": "No saved model found"}

