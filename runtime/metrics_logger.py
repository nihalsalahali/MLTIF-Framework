"""
Runtime Metrics Logger for MLTIF
Author: 
Logs detection and mitigation events for audit and analysis.
"""

import datetime

LOG_FILE = "/tmp/mltif_metrics.log"

def log_event(event_type, details):
    timestamp = datetime.datetime.now().isoformat()
    log_line = f"[{timestamp}] [{event_type.upper()}] {details}\n"
    print(log_line.strip())

    # Optionally write to file
    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_line)
    except Exception as e:
        print(f"[Logger Error] {e}")

# Example usage
if __name__ == "__main__":
    log_event("detection", "Threat detected from 10.0.0.1")
    log_event("mitigation", "Rate limit applied to 10.0.0.1")
