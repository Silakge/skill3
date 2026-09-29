"""HTTP client for the dashboard service."""
import json
import time
from http import client as hc


def _connect(config):
    host, _, port = str(config["service_endpoint"]).partition(":")
    return hc.HTTPConnection(host, int(port or 443), timeout=6)


def send_heartbeat(config):
    """POST a short liveness beacon; returns True on HTTP 200."""
    try:
        conn = _connect(config)
        body = json.dumps({"type": "beacon", "tool": config["name"],
                           "at": int(time.time())}).encode()
        conn.request("POST", config["heartbeat_route"], body=body,
                     headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        resp.read()
        conn.close()
        return resp.status == 200
    except OSError:
        return False
