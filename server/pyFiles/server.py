import socket
import time
import json
import os
import select
from dronekit import *
from dronekit.mavlink import MAVConnection
from datetime import datetime

TIME = "TIME"
# create the socket
# AF_INET == ipv4
# SOCK_STREAM == TCP
dict_server_to_client = {"ID":"","MAV":"DOWN","CAM":"DOWN","GPS_LAT":"","GPS_LON":"","ARM":""}


def to_dict(s):
    ret_s = ""
    for c in s:
        if(c == '}'):
            ret_s = ret_s + c
            return ret_s
        ret_s = ret_s + c            
    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.settimeout(5)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 12341))
s.listen(5)
s_client_socket, s_address = s.accept()

print("trying mav")
os.system("python mavproxy_link.py &")
print("mav is up")

try:
    cello_drone = connect("/dev/ttyS0", wait_ready=True, baud=57600)
    dict_server_to_client["MAV"] = "UP"
except:
    dict_server_to_client["MAV"] = "DOWN"
s_client_socket.sendall("dronekit connected")
# print("mav is up")
home_location = cello_drone.location.global_frame

print(home_location)

def fall_back():
    cello_drone.mode = VehicleMode("RTL")


#s.setblocking(0)

# accept only our ip
print("Connection from rpi (addr = ", s_address, ") has been established!")
time.sleep(1)
try:
    os.system("python camera_script.py")
    dict_server_to_client["CAM"] = "UP"
    print("cam try")
except:
    dict_server_to_client["CAM"] = "DOWN"
    print("cam except")

start_time = time.time()

active = True

#empty_msg = bytes("", "utf-8") # windows
empty_msg = "" # linux
msg_id = -1
#def_msg = bytes("CD", "utf-8")
timeout_in_seconds = 5
substracted_time = 0
recv_dict = {"ID":"0"}
while True:
    to_send = ""
    if active:
        try:
            ready_to_read, ready_to_write, in_error = \
                           select.select([s_client_socket,], [s_client_socket,], [], 5)
        except select.error:
            print "select error"
            s.shutdown(2)
            s.close()
            active = False
        elapsed_time = time.time() - start_time
        if len(ready_to_read) > 0:
            s_msg = s_client_socket.recv(1024)
            if s_msg == empty_msg:
                continue
            start_time = time.time()
            
            print "s_msg: ", s_msg
            if "connected" not in s_msg:
                s_msg = to_dict(s_msg)
                recv_dict = json.loads(s_msg)
                print ("recv_dict", recv_dict)
                #substracted_time  = float(time.time()) - float(recv_dict['TIME'])
                msg_id = recv_dict["ID"]
                #print "dict -> ", recv_dict
            #print "time elapsed = ", elapsed_time
            
        if len(ready_to_write) > 0:    
            #s_client_socket.sendall(bytes(str(datetime.now()), "utf-8"))
            #s_client_socket.sendall(str(datetime.now()))
            dict_server_to_client['ID'] = str(msg_id)
            dict_server_to_client['GPS_LAT'] = cello_drone.location.global_frame.lat
            dict_server_to_client['GPS_LON'] = cello_drone.location.global_frame.lon
            if(cello_drone.armed):
                dict_server_to_client['ARM'] = "ARMED"
            else:
                dict_server_to_client['ARM'] = "NOT ARMED"
            ##add all of the key of the dictionary  - TODO
            ##send dict as string using json
            str_dict_server_to_client = json.dumps(dict_server_to_client)
            s_client_socket.sendall(str_dict_server_to_client)

        if elapsed_time > 10:
            print "Timeout"
            active = False
            fall_back()            
        #try:
         #   s_msg = s_client_socket.recv(1024)
        #except socket.error:
         #   active = False
          #  continue
        #elapsed_time = time.time() - start_time
        #if(not s_msg):
         #   print "guy"
        #if s_msg != empty_msg:
         #   start_time = time.time()
            ##print str(s_msg) + " " + str(datetime.now())
          #  if "connected" not in s_msg:
           #     recv_dict = json.loads(s_msg)
            #    #print "dict -> ", recv_dict
             #   print "alive = ", recv_dict['alive']
              #  print "time = ", recv_dict['time']
            #print "time elapsed = ", elapsed_time
        #if elapsed_time > 10:
         #   active = False 
    else:
        print("Connection lost")
        s.shutdown(2)
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 12341))
        s.listen(5)
        print("Trying to reconnect...")
        s_client_socket, s_address = s.accept()
        print("Reconnected")
        start_time = time.time()
        s_msg = empty_msg
        active = True

    # if "Battery" in s_msg:
    #     to_send = to_send + str(cello_drone.battery)+";"
    # if "Armed" in s_msg:
    #     to_send = to_send + str(cello_drone.armed) + ";"
    # s_client_socket.sendall(bytes(to_send, "utf-8"))
    # time.sleep(1)
    0
    time.sleep(1)
s_client_socket.sendall("finished")
time.sleep(2)
s.shutdown(socket.SHUT_RDWR)
time.sleep(3)
s.close()



    
    

