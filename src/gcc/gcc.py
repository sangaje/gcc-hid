import dbus
import dbus.bus

from .constants import (
    BUS_NAME,
    KEYBOARD_INTERFACE,
    KEYBOARD_OBJECT_PATH,
    API_INTERFACE,
    API_PATH,
    MOUSE_OBJECT_PATH,
    MOUSE_INTERFACE
)
from .keyboard import Keyboard
from .mouse import Mouse


_is_inited = False


class GCC:
    _iGcc: dbus.Interface | None = None

    def __init__(self):
        global _is_inited
        if _is_inited:
            return

        bus = dbus.SystemBus()

        iKeyboard = dbus.Interface(
            bus.get_object(BUS_NAME, KEYBOARD_OBJECT_PATH), KEYBOARD_INTERFACE
        )
        iMouse = dbus.Interface(
            bus.get_object(BUS_NAME, MOUSE_OBJECT_PATH),
            MOUSE_INTERFACE
        )


        GCC._iGcc = dbus.Interface(bus.get_object(BUS_NAME, API_PATH), API_INTERFACE)

        Keyboard._iKeyboard = iKeyboard
        Mouse._imouse = iMouse
        _is_inited = True

    @staticmethod
    def GetAllConnectedDevices() -> list[str]:
        return GCC._iGcc.GetAllConnectedDevices()

    @staticmethod
    def EnalbeAllDevicesNotify():
        return GCC._iGcc.EnalbeAllDevicesNotify()

    @staticmethod
    def DisalbeAllDevicesNotify():
        return GCC._iGcc.DisalbeAllDevicesNotify()

    @staticmethod
    def EnalbeDeviceNotify(name: str):
        return GCC._iGcc.EnalbeDeviceNotify(dbus.String(name))

    @staticmethod
    def DisalbeDeviceNotify(name: str):
        return GCC._iGcc.DisalbeDeviceNotify(dbus.String(name))

    @staticmethod
    def RefreshDevices():
        return GCC._iGcc.RefreshDevices()
