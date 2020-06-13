# TO DO - rerunning the script once the internet has been restored (if crashed)
# To DO - for all scripts try and except for keyboard interrupt

import os
#import RPi.GPIO as GPIO
from line_changer import *
from lcd_script import *
from subprocess import check_output
import time

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
#GPIO.setup(7, GPIO.OUT)

end = False
#state = GPIO.input(7)

#line_change("Cam", "False")
#test_lcd()

#time.sleep(40)

#with open("indication.txt", "r") as fd:
#   lines = fd.readlines()
#fd.close()

#while("False" in lines[0]):
#   with open("indication.txt", "r") as fd:
#           lines = fd.readlines()
#   fd.close()


#line_change("Cam", "False")
#test_lcd()

time.sleep(5)
# wait for internet

line_change("Cam", "True")
test_lcd()
os.system("sudo rm -rf ../../dev/video*")
os.system("sudo uv4l -nopreview --auto-video_nr --driver raspicam --encoding mjpeg --width 200 --height 150 --framerate 12 --server-option '--port=8000' --server-option '--max-queued-connections=30' --server-option '--max-streams=3' --server-option '--max-threads=29' rm ../../dev/video1")

#time.sleep(10)
#GPIO.output(11, GPIO.HIGH)

#def get_pid (name):
#    return check_output(['pidof', name])

#while(end == False):
#    instr = raw_input()
#    if(instr == "end"):
#        pid = get_pid("uv4l")
#        kill_string = "sudo kill " + str(pid)
#        os.system(kill_string)
#        end = True
