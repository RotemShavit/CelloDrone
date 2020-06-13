# Run with python3!!
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
from time import sleep

def test_lcd():
	lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40, 38, 36, 32, 33, 31, 29, 23] , numbering_mode=GPIO.BOARD)
	#GPIO.setmode(GPIO.BOARD)
	lcd.clear()
	status = ["NO", "NO", "NO"]
	with open("indication.txt", "r") as fd:
		lines = fd.readlines()
	for i in range(3):
		if("False" in lines[i]):
			status[i] = "NO"
		else:
			status[i] = "YES"


	lcd.write_string("Inet:" + status[0] + "\n")
	lcd.cursor_pos = (1,0)
	lcd.write_string("Cam:" + status[1] + "\n")
	lcd.cursor_pos = (1,8)
	lcd.write_string("Mav:" + status[2] + "\n")
	fd.close()
	GPIO.cleanup()
