from __future__ import annotations
import dbus
import dbus.bus
import dbus.service

from .keyboard import KeyboardApiService
from ..constants import (
    API_PATH,
    BUS_NAME,
    API_NAME,
    BLUEZ_SERVICE_NAME,
    DBUS_OM_IFACE,
    DEVICE_IFACE,
)
from ..hid.services import HIDService


class ApiService(dbus.service.Object):

    def __init__(self, bus: dbus.bus, hid_service: HIDService):
        self.bus: dbus.bus = bus
        bus_name = dbus.service.BusName(BUS_NAME, bus=bus)
        self.devices = self.load_devices(self.bus)
        print(self.devices)
        self.keyboard_api = KeyboardApiService(bus_name, hid_service.keyboard_input)
        super().__init__(bus_name, API_PATH)

    @dbus.service.signal(API_NAME, signature="a{sv}")
    def ConnetedDevicesChanged(self, devices):
        pass

    def load_devices(self, bus: dbus.Bus, adapter="/org/bluez/hci0"):
        om_iface = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, "/"), DBUS_OM_IFACE
        )
        objects = om_iface.GetManagedObjects()

        result = []
        prefix = adapter + "/dev_"

        for path, iface in objects.items():
            if not path.startswith(prefix):
                continue

            dev = iface.get(DEVICE_IFACE)
            if not dev:
                continue
            print(f"{dev['Name']} - {"Paried" if dev['Paired'] else "Not Paired"}")
            if dev["Paired"]:
                result.append(str(path))
        return result
