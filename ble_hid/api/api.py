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
    DBUS_PROP_IFACE,
    DEVICE_IFACE,
    NOTIFY_CTRL_IFACE,
)
from ..hid.services import HIDService


class ApiService(dbus.service.Object):

    def __init__(self, bus: dbus.bus, hid_service: HIDService):
        self.bus: dbus.bus = bus
        bus_name = dbus.service.BusName(BUS_NAME, bus=bus)
        self.load_devices(self.bus)
        self.keyboard_api = KeyboardApiService(bus_name, hid_service.keyboard_input)
        super().__init__(bus_name, API_PATH)

    # TODO Optimization this
    # @dbus.service.signal(API_NAME, signature="a{sv}")
    # def ConnetedDevicesChanged(self, devices):
    #     pass

    @dbus.service.method(API_NAME, out_signature="as")
    def GetAllConnectedDevices(self):
        result = []

        for name, path in self.devices.items():
            try:
                obj = self.bus.get_object(BLUEZ_SERVICE_NAME, path)
                props = dbus.Interface(obj, DBUS_PROP_IFACE)
                if bool(props.Get(DEVICE_IFACE, "Connected")):
                    result.append(dbus.types.String(name))

            except dbus.exceptions.DBusException as e:
                print(f"[API] ERROR : {e}")
            finally:
                continue

        return dbus.types.Array(result)
        

    @dbus.service.method(API_NAME)
    def EnalbeAllDevicesNotify(self):
        for name, path in self.devices.items():
            try:
                obj = self.bus.get_object(BLUEZ_SERVICE_NAME, "/org/bluez/hci0")
                iface = dbus.Interface(obj, NOTIFY_CTRL_IFACE)
                iface.EnableNotifyDevice(dbus.ObjectPath(path))
            except dbus.exceptions.DBusException as e:
                print(f"[API] ERROR : {e}")

    @dbus.service.method(API_NAME)
    def DisalbeAllDevicesNotify(self):
        for name, path in self.devices.items():
            try:
                obj = self.bus.get_object(BLUEZ_SERVICE_NAME, "/org/bluez/hci0")
                iface = dbus.Interface(obj, NOTIFY_CTRL_IFACE)
                iface.DisableNotifyDevice(dbus.ObjectPath(path))
            except dbus.exceptions.DBusException as e:
                print(f"[API] ERROR : {e}")

    @dbus.service.method(API_NAME, in_signature="s")
    def EnalbeDeviceNotify(self, name):
        path = self.devices.get(name, None)
        if not path:
            raise dbus.exceptions.DBusException(f'Unavilable Device name |{name}|')
        try:
            obj = self.bus.get_object(BLUEZ_SERVICE_NAME, "/org/bluez/hci0")
            iface = dbus.Interface(obj, NOTIFY_CTRL_IFACE)
            iface.EnableNotifyDevice(dbus.ObjectPath(path))
        except dbus.exceptions.DBusException as e:
            print(f"[API] ERROR : {e}")

    @dbus.service.method(API_NAME, in_signature="s")
    def DisalbeDeviceNotify(self, name):
        path = self.devices.get(name, None)
        if not path:
            raise dbus.exceptions.DBusException(f'Unavilable Device name |{name}|')
        try:
            obj = self.bus.get_object(BLUEZ_SERVICE_NAME, "/org/bluez/hci0")
            iface = dbus.Interface(obj, NOTIFY_CTRL_IFACE)
            iface.DisableNotifyDevice(dbus.ObjectPath(path))
        except dbus.exceptions.DBusException as e:
            print(f"[API] ERROR : {e}")

    @dbus.service.method(API_NAME)
    def RefreshDevices(self):
        self.load_devices(self.bus)

    # def load_devices(self, bus: dbus.Bus, adapter="/org/bluez/hci0"):
    def load_devices(self, bus: dbus.Bus):
        om_iface = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, "/"), DBUS_OM_IFACE
        )
        objects = om_iface.GetManagedObjects()

        result = {}
        prefix = "/org/bluez/hci0" + "/dev_"

        for path, iface in objects.items():
            if not path.startswith(prefix):
                continue

            dev = iface.get(DEVICE_IFACE)
            if not dev:
                continue
            print(
                f"[API] {dev['Alias']:<20} Found -> {dev['Address']} "
                f"{"Paried" if dev['Paired'] else "Not Paired"}, "
                f"{"Connected" if dev['Connected'] else "Not connected"}"
            )
            if dev["Paired"]:
                result[str(dev["Alias"])] = str(path)
        self.devices = result
