import dbus
import dbus.service

from ..constants import KEYBOARD_API_PATH, KEYBOARD_API_NAME
from ..hid.services import (
    KeyboardInputReportCharacteristic,
    MouseInputReportCharacteristic,
)
from .keymap import HID_MAP, HDI_MOD_KEYS


class KeyboardApiService(dbus.service.Object):
    def __init__(
        self,
        bus,
        keyboard_input: KeyboardInputReportCharacteristic,
    ):
        self._keyboard_input = keyboard_input
        super().__init__(bus, KEYBOARD_API_PATH)

    @dbus.service.method(dbus_interface=KEYBOARD_API_NAME, in_signature="asyi")
    def press_keys(self, keys: list[str], modifier: dbus.Byte, opt: dbus.Int32):
        hid_keys = [HID_MAP.get(key.lower(), 0) for key in keys]
        self._keyboard_input.send_keys(modifier, hid_keys)
        if opt == 0x1:
            self.releas_all()

    @dbus.service.method(dbus_interface=KEYBOARD_API_NAME, in_signature="syi")
    def press_key(self, key: str, modifier: dbus.Byte, opt: dbus.Int32):
        hid_keys = [HID_MAP.get(key.lower(), 0)]
        self._keyboard_input.send_keys(modifier, hid_keys)
        if opt == 0x1:
            self.releas_all()

    @dbus.service.method(dbus_interface=KEYBOARD_API_NAME)
    def releas_all(self):
        self._keyboard_input.send_keys(0x0, [])

    @dbus.service.method(dbus_interface=KEYBOARD_API_NAME, in_signature="sy")
    def send_string(self, string, modifier: dbus.Byte):
        for c in list(string):
            self.press_key(c, modifier, 0x1)

    # TODO It dosen't work :(
    @dbus.service.method(dbus_interface=KEYBOARD_API_NAME, in_signature="s")
    def send_cmd(self, arr):
        arr = [HID_MAP.get(c.lower(), 0) for c in arr]
        self._keyboard_input.send_keys(0x02, arr)
        self.releas_all()
