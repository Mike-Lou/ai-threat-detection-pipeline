import pandas as pd
from model_io import load_model, save_model
from model import Autoencoder
from data_loader import fit_scaler, transform_with_scaler
from pipeline import train_model, compute_anomaly_scores, detect_anomalies
from alerts import create_alert

_cached_model = None
_cached_scaler = None
_cached_numeric_cols = None

def get_or_train_model(df):
    global _cached_model, _cached_scaler, _cached_numeric_cols

    # Try loading saved model
    try:
        model, scaler, numeric_cols = load_model(Autoencoder)
        _cached_model = model
        _cached_scaler = scaler
        _cached_numeric_cols = numeric_cols
        return model, scaler, numeric_cols
    except:
        pass

    # Train new model
    df_train = df.iloc[:3]
    scaler, numeric_cols = fit_scaler(df_train)
    data_train = transform_with_scaler(df_train, scaler, numeric_cols)
    model = train_model(data_train)

    # Save it
    save_model(model, scaler, numeric_cols)

    _cached_model = model
    _cached_scaler = scaler
    _cached_numeric_cols = numeric_cols

    return model, scaler, numeric_cols


def run_scoring(log_dicts):
    df = pd.DataFrame(log_dicts)

    model, scaler, numeric_cols = get_or_train_model(df)

    data_all = transform_with_scaler(df, scaler, numeric_cols)
    scores = compute_anomaly_scores(model, data_all)
    flags, threshold = detect_anomalies(scores, top_n=2)

    alerts = []
    for i, (score, flag) in enumerate(zip(scores, flags)):
        if flag:
            alerts.append(create_alert(i, score, threshold))

    return scores.tolist(), flags.tolist(), alerts
