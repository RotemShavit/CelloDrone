from line_changer import *
from lcd_script import *
import time
import os

line_change("Cam", "False")
test_lcd()

with open("indication.txt", "r") as fd:
	lines = fd.readlines()
	fd.close()

if("True" in lines[0]):
	check = True
else:
	check = False

while(not check):
	with open("indication.txt", "r") as fd:
		lines = fd.readlines()
		fd.close()
	if("True" in lines[0]):
		check = True
	time.sleep(5)

time.sleep(60)
os.system("python camera_script.py")


