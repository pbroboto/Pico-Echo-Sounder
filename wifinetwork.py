import network
from time import sleep
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from machine import Pin, I2C
import rp2

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

class WiFi:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
    
    def ConnectWiFi(self):
        rp2.country('TH')
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wifi_list = wlan.scan()
        print(f'Found AP: {wifi_list}')
        # Turn off wireless power saving
        wlan.config(pm = 0xa11140)
        wlan.connect(self.ssid, self.password)
        sleep(1)

        while wlan.isconnected() == False:
            #print('Waiting for connection...')
            lcd.clear()
            lcd.move_to(0,0)            
            lcd.putstr("Waiting for...")
            lcd.move_to(0,1)            
            lcd.putstr("  Connection...")
            sleep(1)
        ip = wlan.ifconfig()[0]
        #print(f'Pico Connected on IP {ip}')
        lcd.clear()
        lcd.move_to(0,0)            
        lcd.putstr("Pico Connected...")
        lcd.move_to(0,1)            
        lcd.putstr(f"on {ip}")         
        return wlan
