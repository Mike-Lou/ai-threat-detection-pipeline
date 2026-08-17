import pandas as pd
from sklearn.preprocessing import RobustScaler


def load_logs(path):
    df = pd.read_csv(path)
    return df


def fit_scaler(df):
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    scaler = RobustScaler()
    scaler.fit(df[numeric_cols])
    return scaler, numeric_cols


def transform_with_scaler(df, scaler, numeric_cols):
    scaled = scaler.transform(df[numeric_cols])
    return scaled

