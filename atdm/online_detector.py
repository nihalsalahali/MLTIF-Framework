"""
ATDM Online Detector - MLTIF Framework
Description:
    - Loads pre-trained models (Decision Tree, Q-CNN, SNN, Meta).
    - Predicts threat labels from input feature vectors.
    - Outputs detection result and confidence.
"""

import joblib
import numpy as np
import os
import json

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

# Load models
decision_tree = joblib.load(os.path.join(MODEL_DIR, "decision_tree.pkl"))
qcnn = joblib.load(os.path.join(MODEL_DIR, "qcnn_mock.pkl"))
snn = joblib.load(os.path.join(MODEL_DIR, "snn_mock.pkl"))
meta_learner = joblib.load(os.path.join(MODEL_DIR, "meta_learner.pkl"))

def predict_threat(feature_vector):
    """
    Accepts a numpy array of features [1D] and returns prediction results.
    """
    if len(feature_vector.shape) == 1:
        feature_vector = feature_vector.reshape(1, -1)

    pred_dt = decision_tree.predict(feature_vector)
    pred_qcnn = qcnn.predict(feature_vector)
    pred_snn = snn.predict(feature_vector)

    meta_input = np.column_stack([pred_dt, pred_qcnn, pred_snn])
    final_pred = meta_learner.predict(meta_input)
    prob = meta_learner.predict_proba(meta_input)[0][1]  # confidence for class 1 (attack)

    result = {
        "threat_label": int(final_pred[0]),
        "confidence": round(float(prob), 4)
    }

    return result

def generate_alert(feature_vector, src_ip="10.0.0.1", dst_ip="10.0.0.2"):
    detection = predict_threat(np.array(feature_vector))
    alert = {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "detection": detection
    }

    alert_json = json.dumps(alert, indent=2)
    print("[ALERT]", alert_json)
    return alert

# Example usage
if __name__ == "__main__":
    # Dummy vector: replace with real-time feature vector from ITAM
    sample = np.random.rand(12)
    generate_alert(sample)
