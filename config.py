# config.py
import ujson

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "ssid": "",
    "password": "",
    "travel_time": 5.0,
    "pwm_duty": 512,
    "signalk_host": "192.168.1.100",
    "signalk_port": 3000,
    "signalk_token": ""
}

def load_config():
    try:
        with open(CONFIG_FILE) as f:
            return ujson.load(f)
    except:
        return DEFAULT_CONFIG

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        ujson.dump(cfg, f)
