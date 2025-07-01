import machine
from machine import SoftI2C, Pin
import time
import urequests
import network
import umqtt.simple
from machine import Pin, SoftI2C
from pico_i2c_lcd import I2cLcd
from time import sleep

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = SoftI2C(sda=Pin(4), scl=Pin(5), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
lcd.putstr("What mode do you want?")


ssid = 'MahesPKP'
password = 'dadadododo'


USERNAME='PICOGOD'
KEY='aio_QQWH22FatXeoS06Y6u7BPjVp7JVo'
SERVER='io.adafruit.com'
CLIENT_ID='raghav-pico'



abc_url = "https://maker.ifttt.com/trigger/Epilepsy detected/with/key/f2bslppuK5uhg9M7aRkcj2KVH1Diy_Onf1I9yrbYjXm"
bcd_url = "https://maker.ifttt.com/trigger/Cardiac Arrest/with/key/f2bslppuK5uhg9M7aRkcj2KVH1Diy_Onf1I9yrbYjXm"
FEED=['PICOGOD/feeds/ecg','PICOGOD/feeds/emg','PICOGOD/feeds/name']


ecg_pin = machine.ADC(27)
emg_pin = machine.ADC(26)

 
 
ECG_THRESHOLD = 100
EMG_THRESHOLD = 33000


a = input("What mode do you want?: ")


def mqtt_connect():
    address=umqtt.simple.MQTTClient(CLIENT_ID,SERVER,user=USERNAME,password=KEY)
    address.connect()
    print("mqtt is connect")
    return address

def publish_data(path):
    name = 'Epilepsy and Health risk monitoring system'
    ecg_value = read_sensor(ecg_pin)
    emg_value = read_sensor(emg_pin)
    path.publish(FEED[0],str(ecg_value))
    path.publish(FEED[1],str(emg_value))
    path.publish(FEED[2],str(name))
    print("data published")
    
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Connected to Wi-Fi:', wlan.ifconfig())
    
def send_alertepilepsy():
    try:
        response = urequests.get(abc_url)  
        print("Alert sent:", response.text)
        response.close()
    except Exception as e:
        print("Failed to send alert:", e)
        print("call:  https://maker.ifttt.com/trigger/Epilepsy detected/with/key/f2bslppuK5uhg9M7aRkcj2KVH1Diy_Onf1I9yrbYjXm")
        
def send_alertcardiac():
    try:
        response = urequests.get(bcd_url)  
        print("Alert sent:", response.text)
        response.close()
    except Exception as e:
        print("Failed to send alert:", e)
        print("call:  https://maker.ifttt.com/trigger/Cardiac Arrest/with/key/f2bslppuK5uhg9M7aRkcj2KVH1Diy_Onf1I9yrbYjXm")
        
        
connect_wifi()
path=mqtt_connect()
timer=0
if a == "Epilepsy":
    def read_sensor(sensor):
        return sensor.read_u16()

    
     
    try:
        print("* Readings *")
     
        while True:
            
            
            
            ecg_value = read_sensor(ecg_pin)
            emg_value = read_sensor(emg_pin)
     
            ecg_lcd = str(ecg_value)
            emg_lcd = str(emg_value)
            
            print( "EMG:   ",emg_value," ecg:   ", ecg_value)
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("ECG:")
            lcd.move_to(0, 1)
            lcd.putstr(ecg_lcd)
            lcd.move_to(9,0)
            lcd.putstr("EMG:")
            lcd.move_to(9, 1)
            lcd.putstr(emg_lcd)
            
            print("-" * 60)
            path.check_msg()
            if timer>=10:
                publish_data(path)
                timer=0
            timer=timer+1
            time.sleep(1)
            
            
            if (emg_value > EMG_THRESHOLD or ecg_value < ECG_THRESHOLD ):
                print("Epilepsy detected")
                send_alertepilepsy()
                while True:
                    lcd.clear()
                    lcd.move_to(0,0)
                    lcd.putstr("EpilepsyDetected")
                    print("alert sent")
                    time.sleep(2)
                
     
    except KeyboardInterrupt:
        
        print('\nScript stopped by user')
        lcd.clear()
     
    finally:
        
        print('Goodbye!')
        
else:
    ECG_THRESHOLD = 239
    def read_sensor(sensor):
        return sensor.read_u16()
    while True:
        ecg_value = read_sensor(ecg_pin)
        emg_value = read_sensor(emg_pin)
     
        
        print(" ecg:   ", ecg_value)
        print("-" * 60)  
        
        if (ecg_value < ECG_THRESHOLD):
                print("Cardiac Arrest detected")
                send_alertcardiac()
                while True:
                    print("alert sent")
                    
        time.sleep(1)



        
