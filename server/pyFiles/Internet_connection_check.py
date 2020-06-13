import time
import os
#import RPi.GPIO as GPIO
from lcd_script import *
from line_changer import * 

# setting up the GPIO of the rpi:
#GPIO.setwarnings(False)
#GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)
#GPIO.setmode(GPIO.BOARD)
#


time.sleep(10)
line_change("Internet", "False")
test_lcd()
time.sleep(30)

#def line_change(type, status):
#	with open("indication.txt", "r") as fd:
#		lines = fd.readlines()
#	with open("indication.txt", "w") as fd:
#		for line in lines:
#			if(type in line):
#				fd.write(type + ": " + status + "\n")
#			else:
#				fd.write(line)
#	fd.close()

while(True):
	os.system("sudo ping -c 1 8.8.8.8 > ./tem_ping_connection_check.txt")
	if os.stat("./tem_ping_connection_check.txt").st_size != 0:
		line_change("Internet", "True")
		test_lcd()
		#GPIO.output(7, GPIO.HIGH)
		os.system("sudo rm ./tem_ping_connection_check.txt")
		time.sleep(20)
 		#os.system("chromium-browser &")
	else:
		line_change("Internet", "False")
		test_lcd()
		count = 0
		check = False
		while(check == False):
			#GPIO.output(7, GPIO.HIGH)
			time.sleep(1)
			#GPIO.output(7, GPIO.LOW)
			time.sleep(1)
			count += 2
			if(count % 20 == 0):
				os.system("ping -c 1 8.8.8.8 > ./tem_ping_connection_check.txt")
 				if os.stat("./tem_ping_connection_check.txt").st_size != 0:
					line_change("Internet", "True")
					test_lcd()
					check = True
					#GPIO.output(7, GPIO.HIGH)
 				os.system("sudo rm ./tem_ping_connection_check.txt")


# TO DO - checking the intensity og cellulaer reception and blink the led
