# tests.py
import utime

def motor_test(tab, name, log, sk=None):
    msg = f"Testing {name} tab motor..."
    log(msg)
    if sk: sk.send_diagnostic(msg)
    tab.move_down()
    utime.sleep(1)
    tab.stop()
    utime.sleep(0.5)
    tab.move_up()
    utime.sleep(1)
    tab.stop()
    msg = f"{name} motor test complete."
    log(msg)
    if sk: sk.send_diagnostic(msg)

def position_test(tab, name, log, sk=None):
    msg = f"Testing {name} position tracking..."
    log(msg)
    if sk: sk.send_diagnostic(msg)
    tab.position = 0.5
    tab.move_down()
    utime.sleep(tab.travel_time / 2)
    tab.update_position()
    msg = f"{name} position after half-down: {tab.position:.2f}"
    log(msg)
    if sk: sk.send_diagnostic(msg)
    tab.move_up()
    utime.sleep(tab.travel_time / 2)
    tab.update_position()
    msg = f"{name} position after half-up: {tab.position:.2f}"
    log(msg)
    if sk: sk.send_diagnostic(msg)

def signalk_test(signalk, log):
    msg = "Sending test data to Signal K..."
    log(msg)
    signalk.send_diagnostic(msg)
    signalk.send_position("port", 0.25)
    signalk.send_position("starboard", 0.75)
    msg = "Signal K test complete."
    log(msg)
    signalk.send_diagnostic(msg)

def run_all_tests(config, port_tab, starboard_tab, signalk, log):
    msg = "Running full test sequence..."
    log(msg)
    if signalk: signalk.send_diagnostic(msg)
    motor_test(port_tab, "Port", log, signalk)
    motor_test(starboard_tab, "Starboard", log, signalk)
    position_test(port_tab, "Port", log, signalk)
    position_test(starboard_tab, "Starboard", log, signalk)
    signalk_test(signalk, log)
    msg = "All tests completed."
    log(msg)
    if signalk: signalk.send_diagnostic(msg)
