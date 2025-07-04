# nvs.py (Mock NVS using config file fallback for Pico)
from config import load_config, save_config

def get_config():
    return load_config()

def set_config(data):
    save_config(data)
