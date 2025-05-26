#!/usr/bin/env python3

import gi
import subprocess
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class HotspotApp(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hotspot Control")
        self.set_border_width(10)
        self.set_default_size(350, 240)

        grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        self.add(grid)

        grid.attach(Gtk.Label(label="SSID:"), 0, 0, 1, 1)
        self.ssid_entry = Gtk.Entry()
        self.ssid_entry.set_text("MyHotspot")
        grid.attach(self.ssid_entry, 1, 0, 2, 1)

        grid.attach(Gtk.Label(label="Password:"), 0, 1, 1, 1)
        self.pass_entry = Gtk.Entry()
        self.pass_entry.set_visibility(False)
        grid.attach(self.pass_entry, 1, 1, 2, 1)

        self.open_checkbox = Gtk.CheckButton(label="Open network (no password)")
        self.open_checkbox.connect("toggled", self.toggle_password)
        grid.attach(self.open_checkbox, 1, 2, 2, 1)

        grid.attach(Gtk.Label(label="Wi-Fi Interface:"), 0, 3, 1, 1)
        self.interface_combo = Gtk.ComboBoxText()
        self.load_wifi_interfaces()
        grid.attach(self.interface_combo, 1, 3, 2, 1)

        self.start_btn = Gtk.Button(label="Start")
        self.start_btn.connect("clicked", self.start_hotspot)
        grid.attach(self.start_btn, 0, 4, 1, 1)

        self.stop_btn = Gtk.Button(label="Stop")
        self.stop_btn.connect("clicked", self.stop_hotspot)
        grid.attach(self.stop_btn, 1, 4, 1, 1)

        self.restart_btn = Gtk.Button(label="Restart")
        self.restart_btn.connect("clicked", self.restart_hotspot)
        grid.attach(self.restart_btn, 2, 4, 1, 1)

    def toggle_password(self, widget):
        self.pass_entry.set_sensitive(not widget.get_active())

    def load_wifi_interfaces(self):
        self.interface_combo.remove_all()
        interfaces = os.listdir('/sys/class/net/')
        for iface in interfaces:
            if iface.startswith('wlan'):
                self.interface_combo.append_text(iface)
        self.interface_combo.set_active(0)

    def get_selected_interface(self):
        return self.interface_combo.get_active_text()

    def stop_hotspot(self, button=None):
        subprocess.call(["sudo", "nmcli", "connection", "down", "Hotspot"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def start_hotspot(self, button=None):
        ssid = self.ssid_entry.get_text()
        open_network = self.open_checkbox.get_active()
        password = self.pass_entry.get_text() if not open_network else ""
        interface = self.get_selected_interface()

        subprocess.call(["sudo", "nmcli", "connection", "delete", "Hotspot"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if open_network:
            subprocess.call([
                "sudo", "nmcli", "connection", "add",
                "type", "wifi",
                "con-name", "Hotspot",
                "ifname", interface,
                "ssid", ssid,
                "mode", "ap",
                "ipv4.method", "shared"
            ])
            subprocess.call([
                "sudo", "nmcli", "connection", "modify", "Hotspot",
                "802-11-wireless-security.key-mgmt", ""
            ])
        else:
            subprocess.call([
                "sudo", "nmcli", "device", "wifi", "hotspot",
                "ifname", interface,
                "ssid", ssid,
                "password", password
            ])

        subprocess.call(["sudo", "nmcli", "connection", "up", "Hotspot"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def restart_hotspot(self, button=None):
        self.stop_hotspot()
        self.start_hotspot()

if __name__ == "__main__":
    win = HotspotApp()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
