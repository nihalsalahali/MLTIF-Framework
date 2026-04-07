"""
AMCM Action - Quarantine Flow
Blocks traffic from a malicious IP by installing a high-priority DROP rule.
"""

import requests

CONTROLLER_URL = "http://localhost:8080/flowentry/add"

def quarantine(ip_address):
    print(f"[Quarantine] Blocking all flows from IP: {ip_address}")

    flow_rule = {
        "priority": 1000,
        "match": {
            "ipv4_src": ip_address
        },
        "actions": [
            {"type": "DROP"}
        ]
    }

    try:
        response = requests.post(CONTROLLER_URL, json=flow_rule)
        print(f"[Quarantine] Response: {response.status_code} - {response.text}")
        return response.ok
    except Exception as e:
        print(f"[Quarantine] Failed to send rule: {e}")
        return False
