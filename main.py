from machine import UART
from machine import Pin, I2C, SPI
import time
import array
from micropygps import MicropyGPS
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from sdcard import SDCard
import uos
import wificonfig
import network
import ntptime
from utime import gmtime, time, sleep
import rp2

def crc_calc(start_bit_, addr, datalen_, data_0, data_1, data_2, stop_bit_):
    crc = datalen_ ^ addr
    crc = crc ^ data_0
    crc = crc ^ data_1
    crc = crc ^ data_2
    crc = 255 - crc
    if crc == start_bit_ or crc == stop_bit_:
        crc = crc + 1
    return crc

def processData(nmea_sentence):
    nmea = MicropyGPS()
    for x in nmea_sentence:
        nmea.update(x)
    if (nmea.valid_sentence):
        if (nmea.gps_segments[0] == 'SDDPT'):
            #lcd.move_to(0, 0)            
            #lcd.putstr("Found $SDDPT... ")
            #lcd.move_to(0, 1)            
            #lcd.putstr(f"{nmea.depth_meter}m.")
            return (nmea.nmea_sentence, nmea.depth_meter,
                    nmea.depth_unit)            
        elif (nmea.gps_segments[0] == 'SDDBT'):
            lcd.move_to(0, 0)            
            lcd.putstr("Found $SDDBT... ")
            val_feet = float(nmea.depth_feet)
            val_meter = 0.3048 * val_feet
            nmea.depth_meter2 = "%.2f" % val_meter
            lcd.move_to(0, 1)            
            lcd.putstr(f"Depth: {nmea.depth_meter2}m.")
            return (nmea.nmea_sentence, nmea.depth_feet,
                    nmea.depth_unit1, nmea.depth_meter,
                    nmea.depth_unit2, nmea.depth_fathom,
                    nmea.depth_unit3)    

    else:
        return None
    
class RS485Serial():
    
    def __init__(self,id=1,baudrate=4800,tx=Pin(8), rx=Pin(9), ctrl_pin=Pin(12,mode=Pin.OUT),timeout=0):
        self.uart= UART(id,baudrate=baudrate,tx=tx,rx=rx,timeout=timeout)
        self.ctrl_pin = ctrl_pin
        self.char_time_ms = 10000 # baudrate 
        if self.ctrl_pin != None:
            self.ctrl_pin.value(0)
 
    def read(self, count=1):
        return self.uart.read()
        
        
    def any(self):
        return self.uart.any()
        

    def write(self, dataString):
        if self.ctrl_pin:
            self.ctrl_pin.value(1)
        self.uart.write(bytes(dataString)) #,"utf-8"))
        while not self.uart.txdone():
            machine.idle()
        if self.ctrl_pin:
            time.sleep_ms(1 + self.char_time_ms)
            self.ctrl_pin.value(0)
        #flush transmitted stuff from rcv
        nb = self.uart.any()
        self.uart.read(nb)

def calc_chksum(raw_nmea):
    # Input raw_nmea is a sentence without $ and *.
    # Initializing our first XOR value
    csum = 0 
    
    # For each char in chksumdata, XOR against the previous 
    # XOR'd char.  The final XOR of the last char will be our 
    # checksum to verify against the checksum we sliced off 
    # the NMEA sentence
    
    for c in raw_nmea:
       # XOR'ing value of csum against the next char in line
       # and storing the new XOR value in csum
       csum ^= ord(c)
    
    return hex(csum)

def build_nmea_sddbt(field_data):
    depth_feet = float(field_data[1])
    depth_meter = depth_feet * 0.3048
    str_meter = "%.2f" % depth_meter
    fdata = list(field_data)
    fdata[3] = str_meter
    #$SDDBT,1.8,f,0.5,M,0.3,F*09
    raw_nmea = ",".join(fdata)
    print(f"raw nmea: {raw_nmea}")
    csum = calc_chksum(raw_nmea)
    print(f"check sum: {csum}")
    return f"${raw_nmea}*{csum[2:].upper()}\r\n"

    
def getnow(UTC_OFFSET=+7):
    return gmtime(time() + UTC_OFFSET * 3600)

#Builtin Led
led =  Pin('LED', Pin.OUT)

#Max3232 RS323 to TTL
uart0 = UART(0, baudrate=4800, bits=8, parity=None, stop=1, tx=Pin(16), rx=Pin(17))

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=100000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)    
sleep(1)
lcd.clear()
lcd.move_to(0,0)
lcd.putstr("Pico Echosounder")
lcd.move_to(0,1)
lcd.putstr("...")

# Connect to network
rp2.country('TH')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Fill in your network name (ssid) and password here:
ssid = wificonfig.ssid1
password = wificonfig.password1
wlan.connect(ssid, password)
wlan.active(True)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
  if wlan.status() < 0 or wlan.status() >= 3:
    break
  max_wait -= 1
  print('waiting for connection...')
  sleep(1)
 
# Handle connection error
if wlan.status() != 3:
   raise RuntimeError('network connection failed')
else:
  print(f'Connected to {ssid}')
  status = wlan.ifconfig()
  print( 'IP = ' + status[0] )
 
#set time by sync NTP
try:
    ntptime.settime()
except:
    raise Exception("npttime.settime() failed. No network connection.")
dt = getnow()
print(f"dt: {dt}")
#now = (dt[0],dt[1],dt[2],1,dt[3],dt[4],dt[5],dt[6])
#print(f'now: {now}')

#Max485
uart1 = RS485Serial(1,ctrl_pin=Pin(12,mode=Pin.OUT),timeout=1)

#SD Card
spi = SPI(0,
          baudrate=1000000,
          polarity=0,
          phase=0,
          bits=8,
          firstbit=machine.SPI.MSB,
          sck=Pin(2),
          mosi=Pin(3),
          miso=Pin(4))
cs = Pin(1)
sd = SDCard(spi, cs)
fs = uos.VfsFat(sd)
uos.mount(sd, '/sd')
print(uos.listdir('/sd/es'))

while True:
    dt = getnow()
    d = "{0:4d}{1:02d}{2:02d}".format(dt[0],dt[1],dt[2])
        
    with open(f'/sd/es/es{d}.txt', 'a') as file:
        while uart1.any() > 0:  
            rxData1 = uart1.read()
            #uart0.write(rxData0)
            try:
                strings = rxData1.decode('utf-8')
                sentences = strings.split("\r\n")
                nmeas = list(filter(None, sentences))
            except:
                print('Error! cannaot decode UTF-8.')
            else:
                if not(nmeas is None):
                    #print(f"NMEA: {nmeas}")
                    for nmea in nmeas:
                        field_data = processData(nmea)
                        if (not (field_data is None)):
                            if (len(field_data) == 3):
                                print("Found $SDDPT NMEA...")
                                #led.on()
                                #thingspeak.WriteMultipleFields(field_data)
                                #file.write(','.join(field_data))
                                #file.write('\n')
                                #file.flush()
                                print(f"data 1: {field_data}")
                                #led.off()
                                #sleep(0.5)
                            if (len(field_data) == 7):
                                led.on()
                                print("Found $SDDBT NMEA...")
                                print(f"data 2: {field_data}")
                                new_nmea = build_nmea_sddbt(field_data)
                                print(f"new nmea: {new_nmea}")
                                uart0.write(new_nmea)
                                file.write(','.join(field_data))
                                file.write('\n')
                                file.flush()                                
                                led.off()
