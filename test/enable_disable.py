from gcc import GCC, Keyboard
from gcc.keyboard import Modifier


if __name__ == "__main__":
    GCC.RefreshDevices()
    devices = GCC.GetAllConnectedDevices()
    print(f"Connected Devcies: {list(devices)}")
    GCC.EnalbeAllDevicesNotify()
    print("Press to All")
    Keyboard.press_key('a')
    Keyboard.press_key('b')
    Keyboard.press_key('c')

    GCC.DisalbeAllDevicesNotify()
    print("Press to No one")
    Keyboard.press_key('d')
    Keyboard.press_key('e')
    Keyboard.press_key('f')

    GCC.EnalbeAllDevicesNotify()
    print("Press to All")
    Keyboard.press_key('a')
    Keyboard.press_key('b')
    Keyboard.press_key('c')


    # if len(devices) != 2:
    #     print("We need 2 devices")

    GCC.DisalbeDeviceNotify(devices[-1])
    print(f"Press to only {devices[0]}")
    Keyboard.press_key('g')
    Keyboard.press_key('h')
    Keyboard.press_key('i')

    GCC.EnalbeDeviceNotify(devices[-1])
    GCC.DisalbeDeviceNotify(devices[0])

    print(f"Press to only {devices[-1]}")
    Keyboard.press_key('j')
    Keyboard.press_key('k')
    Keyboard.press_key('l')

    GCC.EnalbeAllDevicesNotify()
    print("Press String")
    Keyboard.send_string("test done", Modifier.LSHIFT)
    