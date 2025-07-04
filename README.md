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

## Requirements

- Raspberry Pi Pico W running MicroPython 1.20 or later
- Two IBT-2 (BTS7960) motor drivers
- Rocker switches for manual control
- `urequests` module on the Pico for HTTP communication

## Deployment

1. Copy all `.py` files to the Pico W using `mpremote` or Thonny.
2. Edit `config.json` or browse to `http://trimtab.local` after boot to
   configure Wi‑Fi and motor settings.
3. Reboot the board and `main.py` will start automatically.

## Circuit Diagram

```
                Raspberry Pi Pico W
      +-----------------------------+
      | GP2  ------> Port IN1       |
      | GP3  ------> Port IN2       |
      | GP4  --PWM-> Port EN        |
      | GP5  ------> Starboard IN1  |
      | GP6  ------> Starboard IN2  |
      | GP7  --PWM-> Starboard EN   |
      | 5V   ------> IBT-2 VCC      |
      | GND  ------> IBT-2 GND      |
      +-----------------------------+
```

## License

MIT
