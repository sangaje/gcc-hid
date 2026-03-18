from __future__ import annotations
from difflib import diff_bytes
import dbus
from enum import IntEnum
from .exception import NoDbusConnectionError, check_type


class MouseKey(IntEnum):
    LCLICK = 1
    RCLICK = 2
    MCLICK = 4


class Mouse:
    _imouse: dbus.Interface | None = None

    @staticmethod
    def mouse(buttons: MouseKey = 0, dx = 0, dy = 0, wheel = 0):
        Mouse._imouse.mouse(
            buttons,
            dx,
            dy,
            wheel,
        )
