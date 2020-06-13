import os
import time
import RPi.GPIO as GPIO
##import dronekit

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)

# t = 40 # 40 seconds
#time.sleep(t)

#os.system("python MAVProxy/mavproxy.py --master=/dev/ttyACM0 --baudrate 57600 --aircraft MyCopter --out=udp:37.25.36.17:14550")
os.system("python MAVProxy/mavproxy.py --master=/dev/ttyACM0 --baudrate 57600 --aircraft MyCopter --out=udpbcast:192.168.43.255:14550") # local
#os.system("python ./MAVProxy/mavproxy.py --master=/dev/ttyS0 --baudrate 57600 --aircraft MyCopter --out=udpin:0.0.0.0:14550") # local
#os.system("python ./MAVProxy/mavproxy.py --master=/dev/ttyS0 --baudrate 57600 --aircraft MyCopter --out=udp:37.25.36.17:14550") # public
# Notice that 255 means broadcast in the inner network. 192.168.43.??? is the local ip. 14550 is the QGC port.
# needs to be changed to cellular.
# time.sleep(10)
#GPIO.output(13, GPIO.HIGH) # red LED
 

