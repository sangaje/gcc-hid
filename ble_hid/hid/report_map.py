"""HID report descriptor (Report Map) for keyboard + mouse combo device."""


def build_hid_report_map() -> bytes:
    """Keyboard + mouse combined report descriptor.

    Report ID 1: keyboard input / output(LED)
    Report ID 2: mouse input
    """
    return bytes([
        0x05, 0x01,  # Usage Page (Generic Desktop)
        0x09, 0x06,  # Usage (Keyboard)
        0xA1, 0x01,  # Collection (Application)
        0x85, 0x01,  # Report ID (1)

        0x05, 0x07,  # Usage Page (Keyboard/Keypad)
        0x19, 0xE0,  # Usage Minimum (Left Control)
        0x29, 0xE7,  # Usage Maximum (Right GUI)
        0x15, 0x00,  # Logical Minimum (0)
        0x25, 0x01,  # Logical Maximum (1)
        0x75, 0x01,  # Report Size (1 bit)
        0x95, 0x08,  # Report Count (8)
        0x81, 0x02,  # Input ; 8 modifier bits

        0x75, 0x08,  # Report Size (8 bits)
        0x95, 0x01,  # Report Count (1)
        0x81, 0x01,  # Input ; reserved 1 byte

        0x05, 0x08,  # Usage Page (LEDs)
        0x19, 0x01,  # Usage Minimum (Num Lock)
        0x29, 0x05,  # Usage Maximum (Kana)
        0x15, 0x00,  # Logical Minimum (0)
        0x25, 0x01,  # Logical Maximum (1)
        0x75, 0x01,  # Report Size (1 bit)
        0x95, 0x05,  # Report Count (5)
        0x91, 0x02,  # Output ; 5 LED bits

        0x75, 0x03,  # Report Size (3 bits)
        0x95, 0x01,  # Report Count (1)
        0x91, 0x01,  # Output ; 3-bit padding

        0x05, 0x07,  # Usage Page (Keyboard/Keypad)
        0x19, 0x00,  # Usage Minimum (No Event)
        0x29, 0xff,  # Usage Maximum (0x65) ; 일반 키 usage 범위의 끝
        0x15, 0x00,  # Logical Minimum (0)
        0x25, 0x65,  # Logical Maximum (0x65)
        0x75, 0x08,  # Report Size (8 bits)
        0x95, 0x06,  # Report Count (6)
        0x81, 0x00,  # Input ; 6 keycode bytes
        # 0x05, 0x01,
        # 0x09, 0x06,
        # 0xA1, 0x01,
        # 0x85, 0x01,
        # 0x05, 0x07,
        # 0x19, 0xE0,
        # 0x29, 0xE7,
        # 0x15, 0x00,
        # 0x25, 0x01,
        # 0x75, 0x01,
        # 0x95, 0x08,
        # 0x81, 0x02,
        # 0x75, 0x08,
        # 0x95, 0x01,
        # 0x81, 0x01,
        # 0x05, 0x08,
        # 0x19, 0x01,
        # 0x29, 0x05,
        # 0x15, 0x00,
        # 0x25, 0x01,
        # 0x75, 0x01,
        # 0x95, 0x05,
        # 0x91, 0x02,
        # 0x75, 0x03,
        # 0x95, 0x01,
        # 0x91, 0x01,
        # 0x05, 0x07,
        # 0x19, 0x00,
        # 0x29, 0x65,
        # 0x15, 0x00,
        # 0x25, 0x65,
        # 0x75, 0x08,
        # 0x95, 0x06,
        # 0x81, 0x00,
        # 0xC0,
        # 0x05, 0x01,
        # 0x09, 0x02,
        # 0xA1, 0x01,
        # 0x85, 0x02,
        # 0x09, 0x01,
        # 0xA1, 0x00,
        # 0x05, 0x09,
        # 0x19, 0x01,
        # 0x29, 0x03,
        # 0x15, 0x00,
        # 0x25, 0x01,
        # 0x95, 0x03,
        # 0x75, 0x01,
        # 0x81, 0x02,
        # 0x95, 0x01,
        # 0x75, 0x05,
        # 0x81, 0x01,
        # 0x05, 0x01,
        # 0x09, 0x30,
        # 0x09, 0x31,
        # 0x09, 0x38,
        # 0x15, 0x81,
        # 0x25, 0x7F,
        # 0x75, 0x08,
        # 0x95, 0x03,
        # 0x81, 0x06,
        # 0xC0,
        # 0xC0,
        0xC0,                   # END_COLLECTION
                                # 앞에 열려 있던 이전 COLLECTION 종료

        0x05, 0x01,             # USAGE_PAGE (Generic Desktop)
        0x09, 0x02,             # USAGE (Mouse)
        0xA1, 0x01,             # COLLECTION (Application)

        0x85, 0x02,             #   REPORT_ID (2)

        0x09, 0x01,             #   USAGE (Pointer)
        0xA1, 0x00,             #   COLLECTION (Physical)

        0x05, 0x09,             #     USAGE_PAGE (Button)
        0x19, 0x01,             #     USAGE_MINIMUM (Button 1)
        0x29, 0x03,             #     USAGE_MAXIMUM (Button 3)
        0x15, 0x00,             #     LOGICAL_MINIMUM (0)
        0x25, 0x01,             #     LOGICAL_MAXIMUM (1)
        0x95, 0x03,             #     REPORT_COUNT (3)       -> 버튼 3개
        0x75, 0x01,             #     REPORT_SIZE (1)        -> 각 버튼 1비트
        0x81, 0x02,             #     INPUT (Data, Var, Abs) -> 버튼 상태 3비트

        0x95, 0x01,             #     REPORT_COUNT (1)
        0x75, 0x05,             #     REPORT_SIZE (5)
        0x81, 0x01,             #     INPUT (Const, Array, Abs)
                                #     -> padding 5비트
                                #        버튼 3비트 + 패딩 5비트 = 총 1바이트

        0x05, 0x01,             #     USAGE_PAGE (Generic Desktop)
        0x09, 0x30,             #     USAGE (X)
        0x09, 0x31,             #     USAGE (Y)
        0x09, 0x38,             #     USAGE (Wheel)

        0x15, 0x81,             #     LOGICAL_MINIMUM (-127)
        0x25, 0x7F,             #     LOGICAL_MAXIMUM (127)
        0x75, 0x08,             #     REPORT_SIZE (8)
        0x95, 0x03,             #     REPORT_COUNT (3)       -> X, Y, Wheel
        0x81, 0x06,             #     INPUT (Data, Var, Rel)
                                #     -> 8비트 signed relative 값
                                #        즉 X/Y/Wheel 모두 음수 가능

        0xC0,                   #   END_COLLECTION           -> Physical
        0xC0,                   # END_COLLECTION             -> Application
    ])
