"""
AMCM Action - Update Flow Table
Reroutes or mirrors suspicious flows for DPI or containment.
"""

import requests

CONTROLLER_URL = "http://localhost:8080/flowentry/add"

def update(src_ip, dst_ip):
    print(f"[FlowUpdate] Updating flow from {src_ip} to {dst_ip}")

    flow_rule = {
        "priority": 600,
        "match": {
            "ipv4_src": src_ip,
            "ipv4_dst": dst_ip
        },
        "actions": [
            {"type": "OUTPUT", "port": 3},
            {"type": "SET_QUEUE", "queue_id": 2}
        ]
    }

    try:
        response = requests.post(CONTROLLER_URL, json=flow_rule)
        print(f"[FlowUpdate] Response: {response.status_code} - {response.text}")
        return response.ok
    except Exception as e:
        print(f"[FlowUpdate] Failed to update flow: {e}")
        return False
