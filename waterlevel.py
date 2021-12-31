from tuyalinksdk.client import TuyaClient
from tuyalinksdk.console_qrcode import qrcode_generate
from time import sleep
import RPi.GPIO as GPIO
import time




'=================== SENSOR RASPBERRY PI ================'

GPIO.setmode(GPIO.BCM)
client = TuyaClient(
    productid='44ap38xfhukhdzmc',
     uuid='tuya19df382c4bc66384',
      authkey='uFjw3Vqrrf8yOUTziCzjTc9MCnLktzgL')


TRIG = 2
ECHO = 3

i=0

GPIO.setup(TRIG ,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(4 ,GPIO.OUT)

GPIO.output(TRIG, False)
print("Starting.....")
sleep(2)

while True:
   GPIO.output(TRIG, True)
   sleep(0.00001)
   GPIO.output(TRIG, False)

   while GPIO.input(ECHO)==0:
      pulse_start = time.time()

   while GPIO.input(ECHO)==1:
      pulse_stop = time.time()

   pulse_time = pulse_stop - pulse_start

   water_level = pulse_time * 17150
   print(round(water_level, 2))

   time.sleep(1)
   
   if water_level < 4:
       print("Water will overflow")
       GPIO.output(4, True)
       time.sleep(0.5)
       GPIO.output(4, False)
       time.sleep(0.5)
       GPIO.output(4, True)
       time.sleep(0.5)
       GPIO.output(4, False)
       time.sleep(0.5)
   else:
       GPIO.output(4, False)


'=================== TUYA CLOUD ================'

def on_connected():
    print('Connected.')

def on_qrcode(url):
    qrcode_generate(url)

def on_dps(dps):
    print('DataPoints:', dps)
    dps = {'101':True}
    client.push_dps(dps)

client.on_connected = on_connected
client.on_qrcode = on_qrcode
client.on_dps = on_dps
client.connect()
client.loop_start()

while True:
    sleep(0.5)






