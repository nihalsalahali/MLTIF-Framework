"""
MLTIF Runtime Controller
Author: 
Description:
    - Orchestrates detection and mitigation pipeline in MLTIF.
    - Interfaces with ATDM detector and AMCM mitigation engine.
    - Accepts input features, generates alerts, triggers mitigation.
"""

import json
import numpy as np
from atdm import online_detector
from amcm import mitigation_policy_engine, controller_sync

def process_packet_features(feature_vector, src_ip, dst_ip):
    print("[MLTIF] Processing new feature vector...")

    # Step 1: Generate detection alert
    alert_data = online_detector.generate_alert(feature_vector, src_ip, dst_ip)
    alert_json = json.dumps(alert_data, indent=2)

    # Step 2: Apply mitigation policy
    mitigation_policy_engine.apply_mitigation(alert_json)

    # Step 3: Sync to peer controllers
    controller_sync.sync_alert(alert_json)

# Example test
if __name__ == "__main__":
    test_features = np.random.rand(12)  # dummy feature vector
    process_packet_features(test_features, "10.0.0.8", "10.0.0.1")
