# 🧠 AI Threat Detection Pipeline

AI-powered anomaly detection pipeline for security logs.

---

## 🚀 Overview
A modular, Python-based AI system for detecting anomalies in multi-source security logs.  
It demonstrates a complete end-to-end workflow: ingestion → preprocessing → feature extraction → ML inference → alert generation → API exposure.

---

## 🔍 Features
- Multi-source log ingestion (CloudTrail, Syslog, NetFlow, Windows Event Logs)
- Unified preprocessing pipeline
- PyTorch-based anomaly detection model
- Scaler + model persistence (`saved_model.pth`, `saved_scaler.pth`)
- Metadata tracking (`model_metadata.json`)
- FastAPI microservice for real-time scoring
- JSON alert generation with severity scoring
- Modular architecture for easy extension

---

## 🧩 Architecture Overview

```text
+-----------------------+
|   Log Sources         |
|-----------------------|
| CloudTrail            |
| Syslog                |
| NetFlow               |
| Windows Event Logs    |
+-----------+-----------+
            |
            v
+-----------------------+
|   Data Loaders        |
| cloudtrail_loader.py  |
| syslog_loader.py      |
| netflow_loader.py     |
| windows_event_loader.py|
+-----------+-----------+
            |
            v
+-----------------------+
|   Pipeline            |
| pipeline.py           |
| - preprocessing       |
| - feature extraction  |
| - inference           |
+-----------+-----------+
            |
            v
+-----------------------+
|   ML Model (PyTorch)  |
| model.py / model_io.py|
+-----------+-----------+
            |
            v
+-----------------------+
|   Alerts              |
| alerts.py / alerts.json|
+-----------+-----------+
            |
            v
+-----------------------+
|   FastAPI Server      |
| api_server.py         |
+-----------------------+


## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/Mike-Lou/ai-threat-detection-pipeline.git
cd ai-threat-detection-pipeline

### 2. Create a virtual environment
python -m venv .venv
.\.venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

🧠 Example: Batch Scoring
from pipeline import ThreatPipeline
from cloudtrail_loader import load_cloudtrail

pipeline = ThreatPipeline()
logs = load_cloudtrail("logs.csv")

results = pipeline.score_batch(logs)
print(results)

🧩 Extending the System
To add a new log source:

Create newsource_loader.py

Implement load_newsource(path)

Add mapping in pipeline.py

Replace or retrain the ML model

Save new model via model_io.py

Update model_metadata.json

📁 Project Structure
ai-threat-detection-pipeline/
│
├── api_server.py
├── api_models.py
├── api_utils.py
│
├── pipeline.py
├── model.py
├── model_io.py
│
├── cloudtrail_loader.py
├── syslog_loader.py
├── netflow_loader.py
├── windows_event_loader.py
│
├── alerts.py
├── alerts.json
│
├── saved_model.pth
├── saved_scaler.pth
├── model_metadata.json
│
├── visualize.py
├── logs.csv
│
├── .gitignore
└── README.md

🧭 Roadmap
Add LLM-based anomaly explanations

Add dashboard (Streamlit)

Add Kafka ingestion

Add real-time streaming mode

Add ensemble anomaly detection models

👤 Author
Mikhail Loutsenko  
Principal Software Engineer — AI Security & Risk Analytics
Glen Cove, NY
