import network
import time
from machine import Pin
import BlynkLib
from BlynkTimer import BlynkTimer

BLYNK_AUTH = "zPsnwU82xRo8yUIB0Rv6zahqVu9ILbu7"

WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""

devices = {
    "Device1": Pin(14, Pin.OUT),
    "Device2": Pin(12, Pin.OUT),
    "Device3": Pin(21, Pin.OUT),
    "Device4": Pin(19, Pin.OUT)
}

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)
print("Connecting to WiFi...", end="")
while not wlan.isconnected():
    print(".", end="")
    time.sleep(0.1)
print("\nConnected with IP:", wlan.ifconfig()[0])

blynk = BlynkLib.Blynk(BLYNK_AUTH)
timer = BlynkTimer()

@blynk.on("V0")
def v0_handler(value):
    devices["Device1"].value(int(value[0]))
    print("Device1:", "ON" if devices["Device1"].value() else "OFF")

@blynk.on("V1")
def v1_handler(value):
    devices["Device2"].value(int(value[0]))
    print("Device2:", "ON" if devices["Device2"].value() else "OFF")

@blynk.on("V2")
def v2_handler(value):
    devices["Device3"].value(int(value[0]))
    print("Device3:", "ON" if devices["Device3"].value() else "OFF")

@blynk.on("V3")
def v3_handler(value):
    devices["Device4"].value(int(value[0]))
    print("Device4:", "ON" if devices["Device4"].value() else "OFF")

def send_status():
    for i, key in enumerate(devices):
        blynk.virtual_write(i, devices[key].value())

timer.set_interval(2000, send_status)

print("Blynk Smart Home started!")

while True:
    blynk.run()
    timer.run()
    time.sleep(0.1)
