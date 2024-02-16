#https://github.com/vshymanskyy/blynk-library-python/tree/master

import BlynkLib
import network
import machine
import utime

# Blynk authentication token
BLYNK_AUTH = 'Auth code provided'

# Wi-Fi credentials
WIFI_SSID = 'wifi'
WIFI_PASS = 'password'

# LED pin (replace with your actual pin number)
LED_PIN = 2

def connect_to_blynk():
    """Connects to Wi-Fi and Blynk server."""
    print("Connecting to WiFi...")
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(WIFI_SSID, WIFI_PASS)
    while not wifi.isconnected():
        utime.sleep_ms(250)

    print("Connected to WiFi:", wifi.ifconfig()[0])

    print("Connecting to Blynk...")
    blynk = BlynkLib.Blynk(BLYNK_AUTH)

    @blynk.on("connected")
    def handle_connected(ping):
        print('Blynk ready. Ping:', ping, 'ms')

    @blynk.on("disconnected")
    def handle_disconnected():
        print('Blynk disconnected')

    return blynk

def switch_light(value):
    
    print("Received value:", value)

    if value[0] == '1':
        machine.Pin(LED_PIN, machine.Pin.OUT).value(1)
        print("Turning LED ON")
    else:
        machine.Pin(LED_PIN, machine.Pin.OUT).value(0)
        print("Turning LED OFF")

def run_blynk():
    
    """Connects to Blynk, handles switch changes, and runs the Blynk loop."""
    blynk = connect_to_blynk()

    # Create a Blynk virtual pin for the switch
    @blynk.on("V0")
    def handle_switch_change(value):
        switch_light(value)

    while True:
        blynk.run()
        utime.sleep_ms(250)  # Small delay to avoid overloading network

# Start the Blynk connection
run_blynk()
