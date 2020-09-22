import socket
import time
import json
import os
import select
from dronekit import *
from dronekit.mavlink import MAVConnection
from datetime import datetime
from geopy.distance import distance
from mavproxy_link import start_mav
import math
import threading

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
    

def start_server(data_list):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.settimeout(5)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 12341))
    s.listen(5)
    s_client_socket, s_address = s.accept()

    thread = threading.Thread(target=start_mav)
    thread.start()
    print("Ready to connect the GCS software.")

    try:
        cello_drone = connect("/dev/ttyS0", wait_ready=True, baud=57600)
        #cello_drone = connect("tcp:192.168.1.30:11010", wait_ready=True, baud=57600)
        dict_server_to_client["MAV"] = "UP"
        print("Connected to the flight controller via Dronekit.")
        data_list[6] = cello_drone
        data_list[6].armed = True
        print("Drone is ARMED")
        data_list[6].simple_takeoff(40) # Relevant for simulation only
        print("Taking off...")
    except:
        dict_server_to_client["MAV"] = "DOWN"
        print("Could not connect to flight controller via Dronekit.")
    s_client_socket.sendall("dronekit connected")
    
    # print("mav is up")
    #home_location = cello_drone.location.global_frame

    #print(home_location)


    #s.setblocking(0)

    # accept only our ip
    print("PC has been connected with IP: " + str(s_address) + ".")
    data_list[0] = 1
    time.sleep(1)
    try:
        os.system("python camera_script.py")
        dict_server_to_client["CAM"] = "UP"
    except:
        dict_server_to_client["CAM"] = "DOWN"

    start_time = time.time()

    active = True

    #empty_msg = bytes("", "utf-8") # windows
    empty_msg = "" # linux
    msg_id = -1
    #def_msg = bytes("CD", "utf-8")
    timeout_in_seconds = 5
    substracted_time = 0
    recv_dict = {"ID":"0"}
    i = 0
    while True:
        #print("Current Location: (" + str(cello_drone.location.global_frame.lat) + "," + str(cello_drone.location.global_frame.lon) + ")")
#         if i == 8:
#             data_list[1] = 0
        i = i + 1
        to_send = ""
        if active & data_list[1] == 1:
            try:
                ready_to_read, ready_to_write, in_error = \
                               select.select([s_client_socket,], [s_client_socket,], [], 5)
            except select.error:
                s.shutdown(2)
                s.close()
                active = False
            elapsed_time = time.time() - start_time
            if len(ready_to_read) > 0:
                s_msg = s_client_socket.recv(1024)
                if s_msg == empty_msg:
                    continue
                start_time = time.time()
                
                if "connected" not in s_msg:
                    s_msg = to_dict(s_msg)
                    recv_dict = json.loads(s_msg)
                    #print ("recv_dict", recv_dict)
                    #substracted_time  = float(time.time()) - float(recv_dict['TIME'])
                    msg_id = recv_dict["ID"]
                    data_list[2] = recv_dict["LATENCY"]
                    #print("Current Latency: " + str(data_list[2]) + " ms")
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
                data_list[1] = 0
                print "Timeout."
                active = False            
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
            s.shutdown(2)
            s.close()
            print("Connection lost.")
            while ((cello_drone.location.global_frame.lat != data_list[3]) & (cello_drone.location.global_frame.lon != data_list[4])):
                if data_list[7] == 1:
                    break
                d = distance((data_list[3], data_list[4]), (cello_drone.location.global_frame.lat, cello_drone.location.global_frame.lon))
                print("Distance to fallback destination: " + str(d.m) + " m.")
                #print("Current Location: (" + str(cello_drone.location.global_frame.lat) + "," + str(cello_drone.location.global_frame.lon) + ")")
                #print("lat and lon are: ", cello_drone.location.global_frame.lat, cello_drone.location.global_frame.lon)
                print("\n")
                time.sleep(1)
                if(d.m < 10):
                    break
                continue
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', 12341))
            s.listen(5)
            print("Trying to reconnect...")
            s.settimeout(10)
            try:
                s_client_socket, s_address = s.accept()
                print("Reconnected.")
                #cello_drone.mode = dronekit.VehicleMode("STABLE")
                #cello_drone.mode = VehicleMode("AUTO")
                data_list[1] = 1
                data_list[5] = 1
                start_time = time.time()
                s_msg = empty_msg
                active = True
            except:
                print("Could not reestablish communication. Returning to launch")
                cello_drone.mode = VehicleMode("RTL")
                break

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



    
    

