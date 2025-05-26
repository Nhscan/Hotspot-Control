# Hotspot Control GUI - Wiki

## Overview

**Hotspot Control GUI** is a lightweight GTK-based application for managing Wi-Fi hotspots on Linux systems using NetworkManager. It provides a simple graphical interface to:

* Start and stop Wi-Fi hotspots
* Set SSID and password (or run open/unsecured)
* Choose which wireless interface to use (wlan0, wlan1, etc.)
* Restart hotspot configurations

This is ideal for headless setups (e.g., NanoPi, Raspberry Pi) with VNC access or direct display, and avoids the complexity of CLI `nmcli` use.

---

## Features

* [x] SSID and password configuration
* [x] Toggle between secured and open networks
* [x] Interface selector for multi-wifi systems
* [x] Integrated with NetworkManager (no need for hostapd/dnsmasq)
* [x] Start/Stop/Restart controls
* [x] Auto-handles WEP fallback prevention

---

## System Requirements

* Debian-based Linux (Debian, Ubuntu, Armbian, etc.)
* Python 3
* GTK 3 bindings (`python3-gi`, `gir1.2-gtk-3.0`)
* NetworkManager
* A supported wireless interface that can run in AP mode (check via `iw list`)

---

## Installation

### Step 1: Download the Installer

Download the `.deb` file:

```
wget https://github.com/Nhscan/Hotspot-Control/releases/download/1.0/hotspot-control_1.0_all.deb
```

### Step 2: Install

Run the following:

```bash
sudo dpkg -i hotspot-control_1.0_all.deb
```

The installer will:

* Copy the app to `/usr/local/bin/HotspotControl.py`
* Add a desktop shortcut
* Install required packages
* Disable any conflicting services (hostapd, dnsmasq, isc-dhcp-server)
* Set up passwordless `nmcli` access for user `craig`

---

## Running the App

After install, you can:

* Find it in your Applications menu as **Hotspot Control**
* Or run it manually:

```bash
/usr/bin/python3 /usr/local/bin/HotspotControl.py
```

---

## Permissions

The app uses `sudo nmcli`, and the installer creates this sudoers rule:

```
<user> ALL=(ALL) NOPASSWD: /usr/bin/nmcli
```

This lets the GUI manage connections without password prompts.

---

## Notes

* If you're using the app in a VNC or headless environment, leave the dummy X11 config in place
* For local HDMI output and GUI login, LightDM + XFCE are supported
* Only interfaces capable of AP mode will work (check with `iw list`)

---

## Troubleshooting

* **Green screen or no GUI:** Make sure no dummy Xorg config is interfering with real HDMI
* **Hotspot won’t start:** Check if the interface supports AP mode and is not managed by another tool
* **App won’t reopen:** Use `pkill -f HotspotControl.py` to clear zombie instances

---

## License

MIT License. Free to use and modify.
