"""
AMCM Action - Rate Limiting
Applies bandwidth limits to suspicious traffic using controller QoS queues.
"""

import requests

CONTROLLER_URL = "http://localhost:8080/flowentry/add"

def limit(ip_address):
    print(f"[RateLimiter] Applying rate limit to IP: {ip_address}")

    flow_rule = {
        "priority": 500,
        "match": {
            "ipv4_src": ip_address
        },
        "actions": [
            {"type": "SET_QUEUE", "queue_id": 1}
        ]
    }

    try:
        response = requests.post(CONTROLLER_URL, json=flow_rule)
        print(f"[RateLimiter] Response: {response.status_code} - {response.text}")
        return response.ok
    except Exception as e:
        print(f"[RateLimiter] Failed to send rule: {e}")
        return False
