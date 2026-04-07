"""
AMCM - Controller Synchronization Module

Description:
    - Simulates sync between SDN controllers in a distributed environment.
    - Ensures policy and flow rule consistency across controllers.
"""

import json

# list of other controller IPs 
peer_controllers = [
    "10.0.0.2",
    "10.0.0.3"
]

def sync_alert(alert_json):
    """
    Simulates broadcasting an alert to all peer SDN controllers.
    In a real implementation, this could be a gRPC or REST push.
    """
    print("[ControllerSync] Broadcasting alert to peers...")
    alert = json.loads(alert_json)
    for peer_ip in peer_controllers:
        print(f" -> Syncing with controller at {peer_ip}...")
        # In practice, send a REST/gRPC POST to peer_ip with alert data
        # Example:
        # requests.post(f"http://{peer_ip}:8181/controller/sync", json=alert)

def sync_policies(policy_dict):
    """
    Sync current mitigation policy rules to peers.
    """
    print("[ControllerSync] Syncing policies to peers...")
    for peer_ip in peer_controllers:
        print(f" -> Syncing policies with controller at {peer_ip}...")
        # Send policies to peer_ip
        # Example:
        # requests.post(f"http://{peer_ip}:8181/controller/policies", json=policy_dict)

if __name__ == "__main__":
    test_alert = json.dumps({
        "src_ip": "10.0.0.6",
        "dst_ip": "10.0.0.3",
        "detection": {
            "threat_label": 1,
            "confidence": 0.91
        }
    })
    sync_alert(test_alert)
    sync_policies({"T_anom": 0.73, "T_cls": 0.8})
