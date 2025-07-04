# main.py
from config import load_config
from wifi_manager import connect_wifi
from web_server import start_web_server
from trimtab import PortTab, StarboardTab
from signalk import SignalKClient
from tests import run_all_tests
import utime

config = load_config()
connect_wifi(config)
signalk = SignalKClient(config)
port_tab = PortTab(config)
starboard_tab = StarboardTab(config)

# Optional: run tests on boot
# run_all_tests(config, port_tab, starboard_tab, signalk, print)

start_web_server(config, port_tab, starboard_tab, signalk)

while True:
    port_tab.handle_switch()
    starboard_tab.handle_switch()
    signalk.send_position("port", port_tab.position)
    signalk.send_position("starboard", starboard_tab.position)
    utime.sleep(2)
