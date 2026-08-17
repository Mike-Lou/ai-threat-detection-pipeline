import matplotlib.pyplot as plt
import numpy as np


def plot_scores(scores, flags, threshold):
    plt.figure(figsize=(10, 5))

    # normal points
    normal_idx = np.where(flags == False)[0]
    anomaly_idx = np.where(flags == True)[0]

    plt.scatter(normal_idx, scores[normal_idx], color='blue', label='Normal')
    plt.scatter(anomaly_idx, scores[anomaly_idx], color='red', label='Anomaly')

    plt.axhline(threshold, color='green', linestyle='--', label='Threshold')

    plt.title("Anomaly Scores")
    plt.xlabel("Row Index")
    plt.ylabel("Reconstruction Error")
    plt.legend()
    plt.grid(True)
    plt.show()
