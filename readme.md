

## Reqirements

- System pakage 

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
sudo apt install python3-dbus libdbus-1-dev libglib2.0-dev pkg-config gcc python3-dev -y

sudo systemctl disable bluetooth
sudo service bluetooth stop
sudo cp ./com.gcc.conf /etc/dbus-1/system.d/
sudo systemctl restart dbus
sudo systemctl restart bluetooth
```

- (Optional) Replace BuleZ for multi HID client control

```bash
git clone https://github.com/sangaje/bluez && cd ./bluez

set -e
sudo sed -i 's/^Types: deb$/Types: deb deb-src/' /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list.d/raspi.sources
grep -R '^Types:' /etc/apt/sources.list.d/*.sources
sudo apt-get update
sudo apt-get -y build-dep bluez
sudo apt-get -y install build-essential autoconf automake libtool pkg-config

sudo apt-get update
sudo apt-get install -y build-dep bluez build-essential autoconf automake libtool pkg-config

./bootstrap
./configure --prefix=/usr --mandir=/usr/share/man \
				--sysconfdir=/etc --localstatedir=/var

make -j"$(nproc)"
sudo make install
sudo cp ./com.gcc.conf /etc/dbus-1/system.d/
```



Change  `/lib/systemd/system/bluetooth.service`
```bash
ExecStart=/usr/libexec/bluetooth/bluetoothd
```
to
```bash
ExecStart=/usr/libexec/bluetooth/bluetoothd -P input
```

Change  `/etc/bluetooth/main.conf`
```bash
#ControllerMode = dual
```
to
```bash
ControllerMode = le
```



reboot.
```bash
sudo reboot
```


## install
```bash
pip install -e .
```

## How to use

> First you have to run ble_hid GATT server

```bash
sudo python3 -m ble_hid
```

> Then you can use gcc module!

```python
from gcc import Keyboard

Keyboard.press_key('a')
```

