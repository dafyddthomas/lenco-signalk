# signalk.py
import urequests

class SignalKClient:
    def __init__(self, config):
        self.host = config["signalk_host"]
        self.port = config["signalk_port"]
        self.token = config["signalk_token"]

    def send_position(self, tab, position):
        url = f"http://{self.host}:{self.port}/signalk/v1/api/delta"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        delta = {
            "updates": [{
                "source": {"label": "pico-trimtab"},
                "values": [{
                    "path": f"steering.trimTab.{tab}",
                    "value": round(position, 2)
                }]
            }]
        }
        try:
            r = urequests.post(url, headers=headers, json=delta)
            r.close()
        except Exception as e:
            print("SignalK error:", e)

    def send_diagnostic(self, message):
        url = f"http://{self.host}:{self.port}/signalk/v1/api/delta"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        delta = {
            "updates": [{
                "source": {"label": "pico-trimtab"},
                "values": [{
                    "path": "notifications.trimTab.test",
                    "value": {
                        "state": "normal",
                        "message": message
                    }
                }]
            }]
        }
        try:
            r = urequests.post(url, headers=headers, json=delta)
            r.close()
        except Exception as e:
            print("SignalK diagnostic error:", e)
