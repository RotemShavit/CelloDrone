import socket
import time
import json
import select
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
from json import *

# CONNECT_ADDR = '147.234.54.189'
CONNECT_IP = '192.168.43.49'
# CONNECT_IP = '147.234.54.189'
CONNECT_PORT = 12341


def to_dict(s):
    ret_s = ""
    for c in s:
        if (c == 125): # 125=ASCII of '}'
            ret_s = ret_s + chr(c)
            return ret_s
        ret_s = ret_s + chr(c)


def start_socket(data_list):
    # TODO - FIX THIS: (remider - port is int and ip is str)
    CONNECT_IP = str(data_list[8])
    CONNECT_PORT = str(data_list[9])
    msg_id = 1
    delay_dict = {}
    recv_msg_single_dict = "{'ID': '-1'}"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    check = 0
    while check == 0:
        if data_list[8] != None:
            try:
                print("Trying to connect...")
                s.connect((CONNECT_IP, CONNECT_PORT)) # net stick
                print('Connection established. Retrieving MAVLink data & socket connection...')
                check = 1
            except:
                print("Connection not established.")
                data_list[8] = None
                #exit(1)
    dronekit_msg = s.recv(1024)
    dronekit_wanted_msg = bytes("dronekit connected", "utf-8")
    print(dronekit_wanted_msg)
    print(dronekit_msg)
    while(dronekit_msg != dronekit_wanted_msg):
        dronekit_msg = s.recv(1024)
        print(dronekit_msg)
    s.sendall(bytes("connected", "utf-8"))
    start_time = time.time()
    active = True
    empty_msg = bytes("", "utf-8")
    dict = {'ID': str(msg_id)}
    i = 0
    while True:
        if active:
            try:
                ready_to_read, ready_to_write, in_error = select.select([s, ],
                                                                        [s, ],
                                                                        [], 5)
            except select.error:
                s.shutdown(2)
                s.close()
                active = False
            elapsed_time = time.time() - start_time
            if len(ready_to_read) > 0:
                recv_msg = s.recv(1024)
                print("recv_msg: ", recv_msg)
                return_msg_time = time.time()
                if recv_msg == empty_msg:
                    time.sleep(1)
                    continue
                start_time = time.time()
                recv_msg_single_dict = to_dict(recv_msg)
                recv_dict = json.loads(recv_msg_single_dict)
                data_list[6] = recv_msg_single_dict
                original_send_time = delay_dict.get(recv_dict['ID'], -1)
                if original_send_time != -1:
                    data_list[0] = float("{:.2f}".format((((return_msg_time - original_send_time)/2) * 1000) - 500))
                    data_list[1] = recv_dict["MAV"]
                    data_list[2] = recv_dict["CAM"]
                    data_list[3] = recv_dict["GPS_LAT"]
                    data_list[4] = recv_dict["GPS_LON"]
                    data_list[5] = recv_dict["ARM"]
                    # print("delay_dict_before_del: ", delay_dict)
                    # print("curr ID: ", recv_dict['ID'])
                    del delay_dict[recv_dict['ID']]
                    # print("delay_dict_after_del: ", delay_dict)
                    #print("travel time of ", recv_dict['ID'], " is: ", travel_time, " ms")
                # translate recv_msg to dictionary
                # inet_delay = 0
                # mav_str = "DOWN"
                # cam_str = "DOWN"
            if len(ready_to_write) > 0:
                dict['ID'] = str(msg_id)
                str_dict = json.dumps(dict)
                s.sendall(bytes(str_dict, "utf-8"))
                delay_dict[str(msg_id)] = time.time()
                msg_id = msg_id + 1
            if elapsed_time > 10:
                active = False
        else:
            print("Trying to reconnect...")
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.connect((socket.gethostname(), 12341)) same pc
            data_list[0] = -1
            try:
                #s.connect(('147.234.54.189', 12341)) # net stick
                s.connect((CONNECT_IP, CONNECT_PORT))
            except OSError:
                time.sleep(1)
                continue
            print("Reconnected.")
            active = True
            start_time = time.time()
        time.sleep(1)

    # time.sleep(2)
    # s.shutdown(socket.SHUT_RDWR)
    # time.sleep(3)
    s.close()
