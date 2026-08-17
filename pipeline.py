import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

from model import Autoencoder

# Loaders for different log types
from data_loader import load_logs, fit_scaler, transform_with_scaler
from syslog_loader import load_syslog
from cloudtrail_loader import load_cloudtrail
from windows_event_loader import load_windows_event_log
from netflow_loader import load_netflow

from visualize import plot_scores
from alerts import create_alert, save_alerts


# -----------------------------
#  TRAINING
# -----------------------------
def train_model(data):
    input_dim = data.shape[1]
    model = Autoencoder(input_dim)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    dataset = TensorDataset(torch.tensor(data, dtype=torch.float32))
    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    for epoch in range(50):
        for batch in loader:
            batch = batch[0]

            optimizer.zero_grad()
            output = model(batch)
            loss = criterion(output, batch)
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

    return model


# -----------------------------
#  SCORING
# -----------------------------
def compute_anomaly_scores(model, data):
    model.eval()

    with torch.no_grad():
        inputs = torch.tensor(data, dtype=torch.float32)
        outputs = model(inputs)
        errors = torch.mean((outputs - inputs) ** 2, dim=1)

    return errors.numpy()


def detect_anomalies(scores, top_n=2):
    scores = np.array(scores)
    sorted_idx = np.argsort(scores)
    anomaly_idx = sorted_idx[-top_n:]

    flags = np.zeros_like(scores, dtype=bool)
    flags[anomaly_idx] = True

    threshold = scores[anomaly_idx].min()
    return flags, threshold


# -----------------------------
#  UNIVERSAL LOG LOADER
# -----------------------------
def load_any_logs(path, log_type="csv"):
    if log_type == "csv":
        return load_logs(path)
    elif log_type == "syslog":
        return load_syslog(path)
    elif log_type == "cloudtrail":
        return load_cloudtrail(path)
    elif log_type == "windows":
        return load_windows_event_log(path)
    elif log_type == "netflow":
        return load_netflow(path)
    else:
        raise ValueError(f"Unknown log type: {log_type}")


# -----------------------------
#  MAIN PIPELINE
# -----------------------------
def main():
    # CHANGE THIS TO SWITCH LOG TYPES
    log_type = "csv"
    path = "logs.csv"

    df = load_any_logs(path, log_type)

    # 1. Fit scaler on normal data only
    df_train = df.iloc[:3]
    scaler, numeric_cols = fit_scaler(df_train)

    # 2. Transform training data
    data_train = transform_with_scaler(df_train, scaler, numeric_cols)

    # 3. Train model
    model = train_model(data_train)

    # 4. Transform ALL rows with the SAME scaler
    data_all = transform_with_scaler(df, scaler, numeric_cols)

    # 5. Score and detect anomalies
    scores = compute_anomaly_scores(model, data_all)
    flags, threshold = detect_anomalies(scores, top_n=2)

    print("Scores:", scores)
    print("Threshold:", threshold)

    # 6. Visualization
    plot_scores(scores, flags, threshold)

    # 7. Alerts
    alerts = []
    for i, (score, flag) in enumerate(zip(scores, flags)):
        if flag:
            alert = create_alert(i, score, threshold)
            alerts.append(alert)
            print(f"ALERT: {alert}")

    if alerts:
        save_alerts(alerts)
        print("\nAlerts saved to alerts.json")
    else:
        print("\nNo anomalies detected.")


if __name__ == "__main__":
    main()
