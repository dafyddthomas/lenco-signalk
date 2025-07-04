# wifi_manager.py
import network
import utime

def connect_wifi(config):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config['ssid'], config['password'])
    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        utime.sleep(1)
        timeout -= 1
    if wlan.isconnected():
        print("Connected:", wlan.ifconfig())
        try:
            import mdns
            mdns.start("trimtab")
            print("mDNS started: http://trimtab.local")
        except:
            print("mDNS failed or not available.")
    else:
        print("Failed to connect. Consider fallback captive portal.")
