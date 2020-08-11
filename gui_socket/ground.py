from gui import start_gui
from client import start_socket
import threading

data_list = [0, "DOWN", "DOWN", 0, 0, "NOT ARMED", "", 0, "0.0.0.0", "0000"]
# [travel_time, MAV, CAM, GPS_LAT, GPS_LON, ARM, SERVER_MSG, PRESSED_CONNECT, DRONE_IP, DRONE_PORT]

thread = threading.Thread(target=start_gui, args=[data_list])
thread.start()
while(data_list[7] == 0):
    continue
start_socket(data_list)
thread.join()
exit(0)
