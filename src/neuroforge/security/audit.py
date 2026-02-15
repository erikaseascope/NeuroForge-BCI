"""
Audit trail logger - append-only, timestamped entries
Future: hash + blockchain anchor
"""

import json
from datetime import datetime
from pathlib import Path

AUDIT_LOG = Path("audit_trail.jsonl")  # one line per entry

def log_audit(message: str, extra: dict = None):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "message": message,
        **(extra or {}),
    }
    with AUDIT_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"[AUDIT] {entry['timestamp']} - {message}")
