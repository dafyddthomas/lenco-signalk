# trimtab.py
"""Simple trim tab classes for Raspberry Pi Pico W.

These classes model a trim tab driven by an H-bridge style motor driver.
The implementation here is a lightweight simulation so the code can run
on standard Python for testing purposes. On real hardware you would
replace the print statements with control of ``machine.Pin`` and ``PWM``
objects.
"""

import utime

class TrimTab:
    """Base class tracking position using elapsed time."""

    def __init__(self, config, name, in1=None, in2=None, pwm=None):
        self.name = name
        self.in1 = in1
        self.in2 = in2
        self.pwm = pwm
        self.travel_time = config.get("travel_time", 5.0)
        self.pwm_duty = config.get("pwm_duty", 512)
        self.position = 0.0
        self._direction = 0  # -1 up, 1 down, 0 stopped
        self._last_move = utime.ticks_ms()

    def move_up(self):
        self._update_position()
        self._direction = -1
        self._last_move = utime.ticks_ms()
        print(f"{self.name} moving up")

    def move_down(self):
        self._update_position()
        self._direction = 1
        self._last_move = utime.ticks_ms()
        print(f"{self.name} moving down")

    def stop(self):
        self._update_position()
        self._direction = 0
        print(f"{self.name} stopped")

    def _update_position(self):
        now = utime.ticks_ms()
        elapsed = (now - self._last_move) / 1000
        if self._direction:
            delta = elapsed / self.travel_time * self._direction
            self.position += delta
            self.position = max(0.0, min(1.0, self.position))
        self._last_move = now

    # Method used by tests
    def update_position(self):
        self._update_position()

class PortTab(TrimTab):
    def __init__(self, config):
        # Default pins for documentation purposes
        super().__init__(config, "Port", in1="GP2", in2="GP3", pwm="GP4")

class StarboardTab(TrimTab):
    def __init__(self, config):
        # Default pins for documentation purposes
        super().__init__(config, "Starboard", in1="GP5", in2="GP6", pwm="GP7")
