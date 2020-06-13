import socket
import time
from dronekit import *
from datetime import datetime

# create the socket
# AF_INET == ipv4
# SOCK_STREAM == TCP

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 12341))
s.listen(5)

# cello_drone = connect("/dev/ttyS0", wait_ready=True, baud=57600)

# print("mav is up")

s_client_socket, s_address = s.accept()

# accept only our ip
print("Connection from rpi (addr = ", s_address, ") has been established!")
time.sleep(1)

start_time = time.time()

active = True

empty_msg = bytes("", "utf-8")

def_msg = bytes("CD", "utf-8")

while True:
    to_send = ""
    if active:
        s_client_socket.sendall(bytes(str(datetime.now()), "utf-8"))
        s_msg = s_client_socket.recv(1024)
        elapsed_time = time.time() - start_time
        if s_msg != empty_msg:
            start_time = time.time()
            print(str(s_msg) + " " + str(datetime.now()))
            print("time elapsed = ", elapsed_time)
        if elapsed_time > 20:
            print("Connection lost")
            s.close()
            active = False
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 12341))
        s.listen(5)
        print("Trying to reconnect...")
        s_client_socket, s_address = s.accept()
        print("Reconnected")
        start_time = time.time()
        active = True

    # if "Battery" in s_msg:
    #     to_send = to_send + str(cello_drone.battery)+";"
    # if "Armed" in s_msg:
    #     to_send = to_send + str(cello_drone.armed) + ";"
    # s_client_socket.sendall(bytes(to_send, "utf-8"))
    # time.sleep(1)

s_client_socket.sendall("finished")
time.sleep(2)
s.shutdown(socket.SHUT_RDWR)
time.sleep(3)
s.close()
