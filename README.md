# Trim Tab Controller for Raspberry Pi Pico W

This project controls Lenco-style trim tabs using IBT-2 motor drivers with a Raspberry Pi Pico W.

## Features

- Manual rocker switch input (1-0-1)
- PWM-controlled motor speed
- Estimated position tracking (based on time)
- Wi-Fi configuration with fallback captive portal
- mDNS support (`http://trimtab.local`)
- Web UI for tab control and configuration
- Signal K integration (via HTTP delta updates)
- NVS-style config persistence
- Web-triggered test diagnostics

## Configuration

Accessible via onboard web server:

- SSID & Password
- Travel time (seconds)
- PWM duty cycle (0–65535)
- Signal K host, port, and access token

## Signal K Integration

Delta updates and test logs are sent to Signal K:

```json
{
  "updates": [{
    "source": {"label": "pico-trimtab"},
    "values": [{
      "path": "steering.trimTab.port",
      "value": 0.52
    }]
  }]
}
```

## Project Files

- `main.py`: Entry point and loop
- `wifi_manager.py`: Connects to Wi-Fi and mDNS
- `web_server.py`: HTML UI and endpoints
- `trimtab.py`: Motor + tab logic
- `signalk.py`: Sends data to SK
- `tests.py`: Self-test routines
- `config.py`: Config storage and defaults
- `nvs.py`: Simple NVS-style wrapper

## License

MIT
