"""
AMCM - Mitigation Policy Engine
Author: 
Description:
    - Accepts alert messages (JSON).
    - Matches against policies.
    - Triggers appropriate mitigation actions (rate-limit, quarantine, update table).
"""

import json
from amcm.actions import rate_limit, quarantine_flow, update_flow_table

# Sample policy thresholds
THREAT_CONFIDENCE_THRESHOLD = 0.75

def apply_mitigation(alert_json):
    """
    Apply mitigation based on alert content.
    """
    alert = json.loads(alert_json)
    src_ip = alert.get("src_ip")
    dst_ip = alert.get("dst_ip")
    detection = alert.get("detection", {})
    label = detection.get("threat_label", 0)
    confidence = detection.get("confidence", 0)

    if label == 1 and confidence >= THREAT_CONFIDENCE_THRESHOLD:
        print(f"[AMCM] High confidence threat detected from {src_ip} to {dst_ip}.")

        # Policy rule 1: quarantine high-risk IPs
        quarantine_flow.quarantine(src_ip)

        # Policy rule 2: apply rate limit
        rate_limit.limit(src_ip)

        # Policy rule 3: update flow table
        update_flow_table.update(src_ip, dst_ip)

    else:
        print("[AMCM] No action needed (benign or low-confidence alert).")

# Example usage
if __name__ == "__main__":
    test_alert = {
        "src_ip": "10.0.0.5",
        "dst_ip": "10.0.0.2",
        "detection": {
            "threat_label": 1,
            "confidence": 0.82
        }
    }
    apply_mitigation(json.dumps(test_alert, indent=2))
