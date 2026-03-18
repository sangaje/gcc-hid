import dbus
import dbus.service

from ..constants import MOUSE_API_NAME, MOUSE_API_PATH
from ..hid.services import (
    KeyboardInputReportCharacteristic,
    MouseInputReportCharacteristic,
)

class MouseInput(dbus.service.Object):
    def __init__(self, bus, mouse_input: MouseInputReportCharacteristic):
        self._mouse_input = mouse_input
        super().__init__(bus, MOUSE_API_PATH)


    @dbus.service.method(MOUSE_API_NAME, in_signature="iiii")
    def mouse(self, buttons, dx, dy, wheel):
        self._mouse_input.send_mouse(buttons, dx, dy, wheel)
        # self._mouse_input.send_mouse(0, dx, dy, wheel)