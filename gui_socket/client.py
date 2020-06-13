import socket
import time
import json
import select
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
from json import *
from random import randint
import random
import webbrowser
import threading
import time
import ctypes


def start_gui(data_list):
    def clock():
        localtime = time.localtime()
        cur_time = time.strftime("%I:%M:%S", localtime)
        time.sleep(1)
        return cur_time

    # creating a new tkinter window
    window = tk.Tk()

    # assigning a title
    window.title("CelloDrone User Interface")

    # specifying geomtery for window size
    window.geometry("596x520")

    # set window color
    window['background'] = 'DeepSkyBlue3'

    # set window unresizable
    window.resizable(False, False)


    # # functions for dialog bar
    # def onOpen():
    #     print(filedialog.askopenfilename(initialdir = "/",title = "Open file",filetypes = (("Python files","*.py;*.pyw"),("All files","*.*"))))
    #
    # def onSave():
    #     print(filedialog.asksaveasfilename(initialdir = "/",title = "Save as",filetypes = (("Python files","*.py;*.pyw"),("All files","*.*"))))


    # class to pop up message while hovering over widget with mouse
    class CreateToolTip(object):
        """
        create a tooltip for a given widget
        """
        def __init__(self, widget, text='widget info'):
            self.waittime = 500     #miliseconds
            self.wraplength = 180   #pixels
            self.widget = widget
            self.text = text
            self.widget.bind("<Enter>", self.enter)
            self.widget.bind("<Leave>", self.leave)
            self.widget.bind("<ButtonPress>", self.leave)
            self.id = None
            self.tw = None

        def enter(self, event=None):
            self.schedule()

        def leave(self, event=None):
            self.unschedule()
            self.hidetip()

        def schedule(self):
            self.unschedule()
            self.id = self.widget.after(self.waittime, self.showtip)

        def unschedule(self):
            id = self.id
            self.id = None
            if id:
                self.widget.after_cancel(id)

        def showtip(self, event=None):
            x = y = 0
            x, y, cx, cy = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 20
            # creates a toplevel window
            self.tw = tk.Toplevel(self.widget)
            # Leaves only the label and removes the app window
            self.tw.wm_overrideredirect(True)
            self.tw.wm_geometry("+%d+%d" % (x, y))
            label = tk.Label(self.tw, text=self.text, justify='left',
                           background="#ffffff", relief='solid', borderwidth=1,
                           wraplength = self.wraplength)
            label.pack(ipadx=1)

        def hidetip(self):
            tw = self.tw
            self.tw= None
            if tw:
                tw.destroy()


    def string_to_list(string):
        lst = list(string.split(" "))

        return lst


    # function to send ip & port arguments
    def process_server(ip, port):
        print("IP:", ip + " , Port: " + port)


    # function to send command to drone argument
    def process_com_to_drone(command):
        print("Command:", command)


    def empty_com_to_drone_entry(event):
        com_to_drone_entry.delete(0, "end")
        return None


    # open web for camera connection
    def open_cam_web(addr):
        address = addr + "/stream"
        # print("address to connect: http://" + ip + ":" + port + "/stream")
        webbrowser.open_new("http://" + address)


    # saved drones
    def popup_drones_updated(win):
            def close_popup_window():
                win.destroy()
            win = tk.Toplevel()
            win.geometry("520x80")
            # set help_window color
            win['background'] = 'DeepSkyBlue3'
            win.title("Address Refresh.")
            # set help_window unresizable
            win.resizable(False, False)
            win_txt = tk.Label(win, text="Drone addresses have been refreshed. Press 'Connect to Drone' to proceed.", bg="DeepSkyBlue3", fg="white", font='Helvetica 10 bold')
            win_txt.place(x=15, y=10)
            win_close_button = tk.Button(win, text="Close", bg="LightBlue3", command=close_popup_window)
            win_close_button.place(x=240, y=45)


    def popup_drone_exists(win):
            def close_popup_window():
                win.destroy()
            win = tk.Toplevel()
            win.geometry("260x80")
            # set help_window color
            win['background'] = 'DeepSkyBlue3'
            win.title("Drone Creation Message")
            # set help_window unresizable
            win.resizable(False, False)
            win_txt = tk.Label(win, text="Address already exists.", bg="DeepSkyBlue3", fg="white", font='Helvetica 10 bold')
            win_txt.place(x=15, y=10)
            win_close_button = tk.Button(win, text="Close", bg="LightBlue3", command=close_popup_window)
            win_close_button.place(x=130, y=45)


    def popup_no_drones_in_list(win):
            def close_popup_window():
                win.destroy()
            win = tk.Toplevel()
            win.geometry("260x80")
            # set help_window color
            win['background'] = 'DeepSkyBlue3'
            win.title("Drone Deletion Message")
            # set help_window unresizable
            win.resizable(False, False)
            win_txt = tk.Label(win, text="There are no drones to delete.", bg="DeepSkyBlue3", fg="white", font='Helvetica 10 bold')
            win_txt.place(x=15, y=10)
            win_close_button = tk.Button(win, text="Close", bg="LightBlue3", command=close_popup_window)
            win_close_button.place(x=130, y=45)


    def make_default_drone(cur_window, saved_drones_to_txt, chosen_drone, just_deleted):
        def close_create_window(win_to_close):
            win_to_close.destroy()
        file = open("saved_drones.txt", "w+")
        for i in range(2):
                if i == 0:
                    file.write(saved_drones_to_txt)
                if i == 1:
                    file.write(str(chosen_drone))
        file.close()
        if not just_deleted:
            # default_label = tk.Label(cur_window, text="Default Registered.", bg="DeepSkyBlue3", fg="black", width=17, font='Helvetica 8')
            # default_label.place(x=326, y=64)
            popup_drones_updated(cur_window)
            close_create_window(cur_window)


    def add_drone(win, ip_to_add, port_to_add):
        def close_create_window(win_to_close):
            win_to_close.destroy()
        print("IP:", ip_to_add + " , Port: " + port_to_add + " to add")
        with open("saved_drones.txt", "r") as file:
            saved_drones_txt = file.readline()
            default_drone = file.readline()
        file.close()
        saved_drones_list = string_to_list(str(saved_drones_txt))
        address_to_add = ip_to_add + ":" + port_to_add
        saved_drones_list[-1] = saved_drones_list[-1].replace('\n', '')
        enable_add_drone = 1
        enable_popup = 1
        if address_to_add in saved_drones_list:
            popup_drone_exists(win)
            enable_add_drone = 0
        saved_drones_to_txt = ""
        if enable_add_drone:
            file = open("saved_drones.txt", "w")
            for i in range(2):
                if i == 0:
                    for j in range(len(saved_drones_list)):
                        if j == 0:
                            saved_drones_to_txt = saved_drones_to_txt + str(saved_drones_list[j])
                        else:
                            if (len(saved_drones_list) == 1) & (saved_drones_list[0] == ""):
                                pass
                            else:
                                saved_drones_to_txt = saved_drones_to_txt + " " + str(saved_drones_list[j])
                    if saved_drones_list[0] == "":
                        saved_drones_list.append(ip_to_add + ":" + port_to_add)
                        saved_drones_to_txt = saved_drones_to_txt + str(saved_drones_list[-1]) + "\n"
                        make_default_drone(win, saved_drones_to_txt, saved_drones_list[-1], 0)
                        enable_popup = 0
                    else:
                        saved_drones_list.append(ip_to_add + ":" + port_to_add)
                        saved_drones_to_txt = saved_drones_to_txt + " " + str(saved_drones_list[-1]) + "\n"
                    file.write(saved_drones_to_txt)
                if i == 1:
                    file.write(str(default_drone))
            file.close()
        if enable_popup:
            popup_drones_updated(win)
            close_create_window(win)


    def del_drone(win, address_to_del):
        def close_create_window(win_to_close):
            win_to_close.destroy()
        print("IP:", address_to_del, " to del")
        with open("saved_drones.txt", "r") as file:
            saved_drones_txt = file.readline()
            default_drone = file.readline()
        file.close()
        saved_drones_list = string_to_list(str(saved_drones_txt))
        saved_drones_list[-1] = saved_drones_list[-1].replace('\n', '')
        enable_del_drone = 1
        # if list is empty
        if address_to_del == '':
            popup_no_drones_in_list(win)
            enable_del_drone = 0
        saved_drones_to_txt = ""
        if enable_del_drone:
            file = open("saved_drones.txt", "w")
            for i in range(2):
                if i == 0:
                    for drone in saved_drones_list:
                        if drone == address_to_del:
                            saved_drones_list.remove(address_to_del)
                            saved_drones_to_txt = ' '.join(map(str, saved_drones_list))
                            if len(saved_drones_list) == 0:
                                make_default_drone(win, saved_drones_to_txt, '', 1)
                            else:
                                make_default_drone(win, saved_drones_to_txt, saved_drones_list[0], 1)
                if i == 1:
                    file.write(str(default_drone))
            file.close()
        popup_drones_updated(win)
        close_create_window(win)


    # create new window for drone connection
    def create_drone_window(cur_window):
        ip_create_input = tk.StringVar()
        port_create_input = tk.StringVar()
        ip_create_label = tk.Label(cur_window, text="IP :", bg="sky blue", width=17, font='Helvetica 9', relief="groove")
        ip_create_label.place(x=10, y=76)
        port_create_label = tk.Label(cur_window, text="Port :", bg="sky blue", width=17, font='Helvetica 9', relief="groove")
        port_create_label.place(x=10, y=98)
        ip_create_entry = tk.Entry(cur_window, textvariable=ip_create_input)
        ip_create_entry.place(x=141, y=76)
        port_create_entry = tk.Entry(cur_window, textvariable=port_create_input)
        port_create_entry.place(x=141, y=98)
        # send command to drone button
        create_button = tk.Button(cur_window, text="Create", bg="LightBlue3", command=lambda: add_drone(cur_window, ip_create_entry.get(), port_create_entry.get()))
        create_button.place(x=270, y=82)

    def conn_window():
        def close_conn_window(win_to_close):
            win_to_close.destroy()
        def process_saved_drones():
            with open("saved_drones.txt", "r") as file:
                saved_drones_txt = file.readline()
                default_drone = file.readline()
            file.close()
            saved_drones_list = string_to_list(str(saved_drones_txt))
            return saved_drones_list, default_drone, saved_drones_txt
        conn_win = tk.Toplevel(window)
        conn_win.geometry("480x155")
        # set con_window color
        conn_win['background'] = 'DeepSkyBlue3'
        conn_win.title("Connection to Drone")
        # set conn_window unresizable
        conn_win.resizable(False, False)
        drones_label = tk.Label(conn_win, text="Drones :", bg="sky blue", width=13, font='Helvetica 9', relief="groove")
        drones_label.place(x=10, y=10)
        saved_drones_list, default_drone, saved_drones_txt = process_saved_drones()
        variable = tk.StringVar(conn_win)
        variable.set(default_drone)
        opt = tk.OptionMenu(conn_win, variable, *saved_drones_list)
        opt.config(width=16, font=('Helvetica', 10))
        opt.place(x=115, y=8)
        def update_pressed(selected_drone):
            drone_addr = selected_drone.split(":")
            data_list[7] = 1
            data_list[8] = drone_addr[0]
            data_list[9] = drone_addr[1]
            if data_list[9][-1] == "\n":
                data_list[9] = data_list[9][:-1]
        def selection_actions(*args):
            selected_drone = format(variable.get())
            make_default_button = tk.Button(conn_win, text="Make Default", bg="LightBlue3", command=lambda: make_default_drone(conn_win, saved_drones_txt, selected_drone, 0))
            make_default_button.place(x=339, y=8)
            delete_drone_button = tk.Button(conn_win, text="Delete", bg="LightBlue3", command=lambda: del_drone(conn_win, selected_drone))
            delete_drone_button.place(x=423, y=8)
            return selected_drone
        variable.trace("w", selection_actions)
        # selected_drone = selection_actions()
        connect_button = tk.Button(conn_win, text="Connect", bg="lime green", command=lambda: update_pressed(selection_actions()))
        connect_button.place(x=280, y=8)
        create_new_button = tk.Button(conn_win, text="Create New", bg="LightBlue3", command=lambda: create_drone_window(conn_win))
        create_new_button.place(x=210, y=45)
        close_win_button = tk.Button(conn_win, text="Close", bg="LightBlue3", command=lambda: close_conn_window(conn_win))
        close_win_button.place(x=225, y=125)
        selection_actions()


    ###########################################################################################
    # saved cameras
    def popup_cameras_updated(win):
            def close_popup_window():
                win.destroy()
            win = tk.Toplevel()
            win.geometry("520x80")
            # set help_window color
            win['background'] = 'DeepSkyBlue3'
            win.title("Address Refresh.")
            # set help_window unresizable
            win.resizable(False, False)
            win_txt = tk.Label(win, text="Camera addresses have been refreshed. Press 'Open Camera' to proceed.", bg="DeepSkyBlue3", fg="white", font='Helvetica 10 bold')
            win_txt.place(x=15, y=10)
            win_close_button = tk.Button(win, text="Close", bg="LightBlue3", command=close_popup_window)
            win_close_button.place(x=240, y=45)


    def popup_camera_exists(win):
            def close_popup_window():
                win.destroy()
            win = tk.Toplevel()
            win.geometry("260x80")
            # set help_window color
            win['background'] = 'DeepSkyBlue3'
            win.title("Camera Creation Message")
            # set help_window unresizable
            win.resizable(False, False)
            win_txt = tk.Label(win, text="Address already exists.", bg="DeepSkyBlue3", fg="white", font='Helvetica 10 bold')
            win_txt.place(x=15, y=10)
            win_close_button = tk.Button(win, text="Close", bg="LightBlue3", command=close_popup_window)
            win_close_button.place(x=130, y=45)


    def popup_no_cameras_in_list(win):
            def close_popup_window():
                win.destroy()
            win = tk.Toplevel()
            win.geometry("260x80")
            # set help_window color
            win['background'] = 'DeepSkyBlue3'
            win.title("Camera Deletion Message")
            # set help_window unresizable
            win.resizable(False, False)
            win_txt = tk.Label(win, text="There are no cameras to delete.", bg="DeepSkyBlue3", fg="white", font='Helvetica 10 bold')
            win_txt.place(x=15, y=10)
            win_close_button = tk.Button(win, text="Close", bg="LightBlue3", command=close_popup_window)
            win_close_button.place(x=130, y=45)


    def make_default_camera(cur_window, saved_cameras_to_txt, chosen_camera, just_deleted):
        def close_create_window(win_to_close):
            win_to_close.destroy()
        file = open("saved_cameras.txt", "w+")
        for i in range(2):
                if i == 0:
                    file.write(saved_cameras_to_txt)
                if i == 1:
                    file.write(str(chosen_camera))
        file.close()
        if not just_deleted:
            # default_label = tk.Label(cur_window, text="Default Registered.", bg="DeepSkyBlue3", fg="black", width=17, font='Helvetica 8')
            # default_label.place(x=326, y=64)
            popup_cameras_updated(cur_window)
            close_create_window(cur_window)

    def add_camera(win, ip_to_add, port_to_add):
        def close_create_window(win_to_close):
            win_to_close.destroy()
        print("IP:", ip_to_add + " , Port: " + port_to_add + " to add")
        with open("saved_cameras.txt", "r") as file:
            saved_cameras_txt = file.readline()
            default_camera = file.readline()
        file.close()
        saved_cameras_list = string_to_list(str(saved_cameras_txt))
        address_to_add = ip_to_add + ":" + port_to_add
        saved_cameras_list[-1] = saved_cameras_list[-1].replace('\n', '')
        print("saved_camera_list[-1]: ", saved_cameras_list[-1], "blabla")
        enable_add_camera = 1
        enable_popup = 1
        if address_to_add in saved_cameras_list:
            popup_camera_exists(win)
            enable_add_camera = 0
        saved_cameras_to_txt = ""
        if enable_add_camera:
            file = open("saved_cameras.txt", "w")
            for i in range(2):
                if i == 0:
                    for j in range(len(saved_cameras_list)):
                        if j == 0:
                            saved_cameras_to_txt = saved_cameras_to_txt + str(saved_cameras_list[j])
                        else:
                            if (len(saved_cameras_list) == 1) & (saved_cameras_list[0] == ""):
                                pass
                            else:
                                saved_cameras_to_txt = saved_cameras_to_txt + " " + str(saved_cameras_list[j])
                    if saved_cameras_list[0] == "":
                        saved_cameras_list.append(ip_to_add + ":" + port_to_add)
                        saved_cameras_to_txt = saved_cameras_to_txt + str(saved_cameras_list[-1]) + "\n"
                        make_default_camera(win, saved_cameras_to_txt, saved_cameras_list[-1], 0)
                        enable_popup = 0
                    else:
                        saved_cameras_list.append(ip_to_add + ":" + port_to_add)
                        saved_cameras_to_txt = saved_cameras_to_txt + " " + str(saved_cameras_list[-1]) + "\n"
                    file.write(saved_cameras_to_txt)
                if i == 1:
                    file.write(str(default_camera))
            file.close()
        if enable_popup:
            popup_cameras_updated(win)
            close_create_window(win)


    def del_camera(win, address_to_del):
        def close_create_window(win_to_close):
            win_to_close.destroy()
        print("IP:", address_to_del, " to del")
        with open("saved_cameras.txt", "r") as file:
            saved_cameras_txt = file.readline()
            default_camera = file.readline()
        file.close()
        saved_cameras_list = string_to_list(str(saved_cameras_txt))
        saved_cameras_list[-1] = saved_cameras_list[-1].replace('\n', '')
        enable_del_camera = 1
        # if list is empty
        if address_to_del == '':
            popup_no_cameras_in_list(win)
            enable_del_camera = 0
        saved_cameras_to_txt = ""
        if enable_del_camera:
            file = open("saved_cameras.txt", "w")
            for i in range(2):
                if i == 0:
                    for camera in saved_cameras_list:
                        if camera == address_to_del:
                            saved_cameras_list.remove(address_to_del)
                            saved_cameras_to_txt = ' '.join(map(str, saved_cameras_list))
                            if len(saved_cameras_list) == 0:
                                make_default_camera(win, saved_cameras_to_txt, '', 1)
                            else:
                                make_default_camera(win, saved_cameras_to_txt, saved_cameras_list[0], 1)
                if i == 1:
                    file.write(str(default_camera))
            file.close()
        popup_cameras_updated(win)
        close_create_window(win)


    def create_camera_window(cur_window):
        ip_create_input = tk.StringVar()
        port_create_input = tk.StringVar()
        ip_create_label = tk.Label(cur_window, text="IP :", bg="sky blue", width=17, font='Helvetica 9', relief="groove")
        ip_create_label.place(x=10, y=76)
        port_create_label = tk.Label(cur_window, text="Port :", bg="sky blue", width=17, font='Helvetica 9', relief="groove")
        port_create_label.place(x=10, y=98)
        ip_create_entry = tk.Entry(cur_window, textvariable=ip_create_input)
        ip_create_entry.place(x=141, y=76)
        port_create_entry = tk.Entry(cur_window, textvariable=port_create_input)
        port_create_entry.place(x=141, y=98)
        # send command to camera button
        create_button = tk.Button(cur_window, text="Create", bg="LightBlue3", command=lambda: add_camera(cur_window, ip_create_entry.get(), port_create_entry.get()))
        create_button.place(x=270, y=82)


    # create new window for camera connection
    def cam_window():
        def close_cam_window(win_to_close):
            win_to_close.destroy()
        def process_saved_cameras():
            with open("saved_cameras.txt", "r") as file:
                saved_cameras_txt = file.readline()
                default_camera = file.readline()
            file.close()
            saved_cameras_list = string_to_list(str(saved_cameras_txt))
            return saved_cameras_list, default_camera, saved_cameras_txt
        conn_win = tk.Toplevel(window)
        conn_win.geometry("480x155")
        # set con_window color
        conn_win['background'] = 'DeepSkyBlue3'
        conn_win.title("Connection to Camera")
        # set conn_window unresizable
        conn_win.resizable(False, False)
        cameras_label = tk.Label(conn_win, text="Cameras :", bg="sky blue", width=13, font='Helvetica 9', relief="groove")
        cameras_label.place(x=10, y=10)
        saved_cameras_list, default_camera, saved_cameras_txt = process_saved_cameras()
        variable = tk.StringVar(conn_win)
        variable.set(default_camera)
        opt = tk.OptionMenu(conn_win, variable, *saved_cameras_list)
        opt.config(width=16, font=('Helvetica', 10))
        opt.place(x=115, y=8)
        def selection_actions(*args):
            selected_camera = format(variable.get())
            print("Selected camera is: " + selected_camera)
            make_default_button = tk.Button(conn_win, text="Make Default", bg="LightBlue3", command=lambda: make_default_camera(conn_win, saved_cameras_txt, selected_camera, 0))
            make_default_button.place(x=339, y=8)
            delete_camera_button = tk.Button(conn_win, text="Delete", bg="LightBlue3", command=lambda: del_camera(conn_win, selected_camera))
            delete_camera_button.place(x=423, y=8)
            return selected_camera
        variable.trace("w", selection_actions)
        #selected_camera = selection_actions()
        #print("ffffff", selected_camera)
        connect_button = tk.Button(conn_win, text="Connect", bg="lime green", command=lambda: open_cam_web(selection_actions()))
        connect_button.place(x=280, y=8)
        create_new_button = tk.Button(conn_win, text="Create New", bg="LightBlue3", command=lambda: create_camera_window(conn_win))
        create_new_button.place(x=210, y=45)
        close_win_button = tk.Button(conn_win, text="Close", bg="LightBlue3", command=lambda: close_cam_window(conn_win))
        close_win_button.place(x=225, y=125)
        selection_actions()
    #################################################################################


    # create new window for help - near command to drone
    def help_window():
        def close_help_window():
            help_win.destroy()
        help_win = tk.Toplevel(window)
        help_win.geometry("500x200")
        # set help_window color
        help_win['background'] = 'DeepSkyBlue3'
        help_win.title("Help - Admin Commands")
        # set help_window unresizable
        help_win.resizable(False, False)
        help_text0 = tk.Label(help_win, text="Please type in the entry box the desired command from the following list:", bg="DeepSkyBlue3", font='Helvetica 11 underline')
        help_text0.place(x=10, y=10)
        help_text1 = tk.Label(help_win, text="rtl_com - Manual activation for returning to launch (failure protocol)", bg="DeepSkyBlue3", font='Helvetica 9')
        help_text1.place(x=10, y=35)
        help_text2 = tk.Label(help_win, text="command_2 - does bla bla", bg="DeepSkyBlue3", font='Helvetica 9')
        help_text2.place(x=10, y=55)
        help_text3 = tk.Label(help_win, text="command_3 - does bla bla bla", bg="DeepSkyBlue3", font='Helvetica 9')
        help_text3.place(x=10, y=75)
        # close button
        help_close_button = tk.Button(help_win, text="Close", bg="LightBlue3", command=close_help_window)
        help_close_button.place(x=230, y=160)


    # create new window for about - menu bar
    def about_window():
        def close_about_window():
            about_win.destroy()
        about_win = tk.Toplevel(window)
        about_win.geometry("610x200")
        # set about_window color
        about_win['background'] = 'DeepSkyBlue3'
        about_win.title("About")
        # set about_window unresizable
        about_win.resizable(False, False)
        about_text0 = tk.Label(about_win, text="This is the GUI of CelloDrone", bg="DeepSkyBlue3", font='Helvetica 11 underline bold')
        about_text0.place(x=10, y=10)
        about_text1 = tk.Label(about_win, text="Semi-automated controllability platform for drone control over public LTE cellular network.", bg="DeepSkyBlue3", fg="white", font='Helvetica 10 bold')
        about_text1.place(x=10, y=35)
        about_text2 = tk.Label(about_win, text="Final Project - Hebrew University of Jerusalem", bg="DeepSkyBlue3", fg="white", font='Helvetica 10 bold')
        about_text2.place(x=10, y=55)
        about_text3 = tk.Label(about_win, text="Hagai Bar-Halevy", bg="DeepSkyBlue3", fg="white", font='Helvetica 10 bold')
        about_text3.place(x=10, y=75)
        about_text4 = tk.Label(about_win, text="Rotem Shavit", bg="DeepSkyBlue3", fg="white", font='Helvetica 10 bold')
        about_text4.place(x=10, y=95)
        about_text5 = tk.Label(about_win, text="Guy Kochmeister", bg="DeepSkyBlue3", fg="white", font='Helvetica 10 bold')
        about_text5.place(x=10, y=115)
        # close button
        about_close_button = tk.Button(about_win, text="Close", bg="LightBlue3", command=close_about_window)
        about_close_button.place(x=285, y=160)


    # # create new window for drone connection
    # def cam_window():
    #     cam_win = tk.Toplevel(window)
    #     cam_win.geometry("350x65")
    #     # set con_window color
    #     cam_win['background'] = 'DeepSkyBlue3'
    #     cam_win.title("Connection to Camera")
    #     # set cam_window unresizable
    #     cam_win.resizable(False, False)
    #     cam_ip = tk.StringVar()
    #     cam_port = tk.StringVar()
    #     ip_label = tk.Label(cam_win, text="Camera IP :", bg="sky blue", width=17, font='Helvetica 9', relief="groove")
    #     ip_label.place(x=10, y=10)
    #     port_label = tk.Label(cam_win, text="Camera Port :", bg="sky blue", width=17, font='Helvetica 9', relief="groove")
    #     port_label.place(x=10, y=32)
    #     cam_ip_entry = tk.Entry(cam_win, textvariable=cam_ip)
    #     cam_ip_entry.place(x=141, y=10)
    #     cam_port_entry = tk.Entry(cam_win, textvariable=cam_port)
    #     cam_port_entry.place(x=141, y=33)
    #     # send command to drone button
    #     connect_button = tk.Button(cam_win, text="Connect", bg="LightBlue3", command=lambda: open_cam_web(cam_ip_entry.get(), cam_port_entry.get()))
    #     connect_button.place(x=275, y=19)


    # pops up message if user is willing to quit
    def on_closing(window_to_close):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            window_to_close.destroy()


    # menu dialog
    menu_bar = tk.Menu(window)
    file_menu = tk.Menu(menu_bar, tearoff=False)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=lambda: on_closing(window))
    edit_menu = tk.Menu(menu_bar, tearoff=False)
    menu_bar.add_cascade(label="Info", menu=edit_menu)
    edit_menu.add_command(label="About", command=about_window)
    window.config(menu=menu_bar)

    # cellodrone logo in parts
    logo = ImageTk.PhotoImage(Image.open("logo_for_gui_small.jpg"))
    img_logo = tk.Label(window, image=logo, borderwidth=0)
    img_logo.place(x=0, y=0)

    # connect to drone button
    connect_to_drone_button = tk.Button(window, text="Connect to Drone", bg="dark orange", width=18, command=conn_window)
    connect_to_drone_button.place(x=230, y=122)

    # camera connection button
    cam_conn_button = tk.Button(window, text="Open Camera", bg="LightBlue3", command=cam_window)
    cam_conn_button.place(x=203, y=155)

    # command to drone label
    com_to_drone_label = tk.Label(window, text="Command to Drone :", bg="DeepSkyBlue3", fg="black", width=20, font='Helvetica 9 bold', relief="groove")
    com_to_drone_label.place(x=127, y=197)

    # entry for command to drone
    com_to_drone = tk.StringVar()
    com_to_drone_entry=tk.Entry(window, textvariable=com_to_drone, width=20)
    com_to_drone_entry.insert(0, "Type Command Here")
    com_to_drone_entry.bind("<Button-1>", empty_com_to_drone_entry)
    com_to_drone_entry.place(x=277, y=197)


    # send command to drone button
    send_com_to_drone_button = tk.Button(window, text="Send", bg="LightBlue3", command=lambda: process_com_to_drone(com_to_drone.get()))
    send_com_to_drone_button.place(x=407, y=194)

    # help button - list of commands
    help_com_to_drone_button = tk.Button(window, text=" ? ", bg="grey", command=help_window)
    help_com_to_drone_button.place(x=447, y=194)

    # pop up help message on help button
    CreateToolTip(help_com_to_drone_button, text = 'Press to view all admin commands for drone.')

    # labels in table
    parameter_title = tk.Label(window, text="Parameter (On Drone)", bg="DeepSkyBlue3", width=23, font='Helvetica 9 bold', relief="groove")
    parameter_title.place(x=131, y=235)
    inet_param_label = tk.Label(window, text="Internet Connection Delay", bg="sky blue", width=23, font='Helvetica 9', relief="groove")
    inet_param_label.place(x=131, y=257)
    mav_param_label = tk.Label(window, text="MAVLink Connection", bg="sky blue", width=23, font='Helvetica 9', relief="groove")
    mav_param_label.place(x=131, y=277)
    cam_param_label = tk.Label(window, text="Camera Connection", bg="sky blue", width=23, font='Helvetica 9', relief="groove")
    cam_param_label.place(x=131, y=297)

    # data in table
    def update_inet_data(inet_lbl):
        #inet_delay = str(randint(1, 150))
        inet_str = str(data_list[0]) + " ms"
        if (int(data_list[0]) > 100):
            inet_lbl.config(fg="red")
        elif int(data_list[0] == -1):
            inet_str = "N/A"
            inet_lbl.config(fg="red")
        else:
            inet_lbl.config(fg="green")
        inet_lbl.config(text=inet_str)
        inet_lbl.after(1000, lambda: update_inet_data(inet_lbl))
    def update_mav_data(mav_lbl):
        # mav_str = random.choice(["UP", "DOWN"])
        if (data_list[1] == "UP"):
            mav_lbl.config(fg="green")
        else:
            mav_lbl.config(fg="red")
        mav_lbl.config(text=data_list[1])
        mav_lbl.after(1000, lambda: update_mav_data(mav_lbl))
    def update_cam_data(cam_lbl):
        # cam_str = random.choice(["UP", "DOWN"])
        if (data_list[2] == "UP"):
            cam_lbl.config(fg="green")
        else:
            cam_lbl.config(fg="red")
        cam_lbl.config(text=data_list[2])
        cam_lbl.after(1000, lambda: update_cam_data(cam_lbl))
    status_title = tk.Label(window, text="Status", bg="DeepSkyBlue3", width=23, font='Helvetica 9 bold', relief="groove")
    status_title.place(x=297, y=235)
    inet_param_data = tk.Label(window, fg="green", bg="white", width=23, font='Helvetica 9', relief="groove")
    inet_param_data.place(x=297, y=257)
    mav_param_data = tk.Label(window, fg="green", bg="white", width=23, font='Helvetica 9', relief="groove")
    mav_param_data.place(x=297, y=277)
    cam_param_data = tk.Label(window, fg="red", bg="white", width=23, font='Helvetica 9', relief="groove")
    cam_param_data.place(x=297, y=297)

    # gps latitude label
    gps_latitude = tk.Label(window, text="GPS Latitude :", bg="DeepSkyBlue3", fg="black", width=20, font='Helvetica 9 bold', relief="groove")
    gps_latitude.place(x=92, y=340)

    # gps latitude data
    gps_latitude_data = tk.Label(window, text="", fg="black", bg="white", width=12, font='Helvetica 9', relief="groove")
    gps_latitude_data.place(x=247, y=340)

    # gps latitude refresh button
    gps_latitude_ref_button = tk.Button(window, text="Refresh", bg="LightBlue3", command=lambda: update_gps_data(gps_latitude_data, gps_longitude_data))
    gps_latitude_ref_button.place(x=347, y=352)


    # copy gps latitude to clipboard
    def copy_lat_clipboard():
        lat_to_copy = gps_latitude_data['text']
        window.clipboard_clear()
        window.clipboard_append(lat_to_copy)


    # gps latitude copy button
    gps_latitude_copy_button = tk.Button(window, text="Copy to Clipboard", bg="LightBlue3", command=copy_lat_clipboard)
    gps_latitude_copy_button.place(x=400, y=337)

    # gps longitude label
    gps_longitude = tk.Label(window, text="GPS Longitude :", bg="DeepSkyBlue3", fg="black", width=20, font='Helvetica 9 bold', relief="groove")
    gps_longitude.place(x=92, y=370)

    # gps longitude data
    gps_longitude_data = tk.Label(window, text="", fg="black", bg="white", width=12, font='Helvetica 9', relief="groove")
    gps_longitude_data.place(x=247, y=370)


    # copy gps longitude to clipboard
    def copy_lon_clipboard():
        lon_to_copy = gps_longitude_data['text']
        window.clipboard_clear()
        window.clipboard_append(lon_to_copy)


    # gps longitude copy button
    gps_longitude_copy_button = tk.Button(window, text="Copy to Clipboard", bg="LightBlue3", command=copy_lon_clipboard)
    gps_longitude_copy_button.place(x=400, y=367)

    def update_gps_data(gps_lat_lbl, gps_lon_lbl):
        # cam_str = random.choice(["UP", "DOWN"])
        gps_lat_lbl.config(text=data_list[3])
        gps_lon_lbl.config(text=data_list[4])

    # armed label
    gps_longitude = tk.Label(window, text="Arm Mode :", bg="DeepSkyBlue3", fg="black", width=20, font='Helvetica 9 bold', relief="groove")
    gps_longitude.place(x=92, y=410)

    # armed data
    def update_armed_data(armed_lbl):
        if (data_list[5] == "ARMED"):
            armed_lbl.config(fg="green")
        else:
            armed_lbl.config(fg="red")
        armed_lbl.config(text=data_list[5])
        armed_lbl.after(1000, lambda: update_armed_data(armed_lbl))
    armed_data = tk.Label(window, fg="red", bg="white", width=12, font='Helvetica 9', relief="groove")
    armed_data.place(x=247, y=410)


    # class to make a text handler for flight logger
    class AdminLogger:
        def __init__(self):
            self.data_status = 1
            self.data_history = []
            self.action()

        def add_data(self, string, buffer):
            while self.txt:
                if self.data_status == 1:
                    # msg = str(randint(1, 100)) + " - " + string+"\n"
                    if len(data_list[6]) > 0:
                        msg = data_list[6] + "\n\n"
                    else:
                        msg = ""
                    self.txt.insert(tk.END, msg)
                    self.txt.yview(tk.END)
                    time.sleep(1)
                else:
                    continue

        def pop_up_save_log_msg(self):
            def close_popup_window():
                popup_log.destroy()
            popup_log = tk.Toplevel(window)
            popup_log.geometry("260x80")
            # set help_window color
            popup_log['background'] = 'DeepSkyBlue3'
            popup_log.title("Save Log")
            # set help_window unresizable
            popup_log.resizable(False, False)
            popup_log_txt = tk.Label(popup_log, text="This is a future optional feature.", bg="DeepSkyBlue3", fg="white", font='Helvetica 10 bold')
            popup_log_txt.place(x=15, y=10)
            popup_log_close_button = tk.Button(popup_log, text="Close", bg="LightBlue3", command=close_popup_window)
            popup_log_close_button.place(x=130, y=45)

        def clear_log(self):
            self.txt.delete('1.0', tk.END)

        def close_log_window(self):
            self.data_status = 0
            self.txt = None
            self.log_win.destroy()

        def log_save(self):
            self.data_status = 0
            self.f = filedialog.asksaveasfile(mode='w', initialdir = "/", title = "Save as", defaultextension=".txt", filetypes = (("Text File",".txt"),("All files","*.*")))
            if self.f is None: # asksaveasfile return `None` if dialog closed with "cancel".
                print("some error")
                pass
            text2save = str(self.txt.get(1.0, tk.END))
            self.f.write(text2save)
            self.f.close()
            self.data_status = 1

        def change_data_status_to_0(self):
            self.data_status = 0

        def change_data_status_to_1(self):
            self.data_status = 1

        def save_file(self):
            print(filedialog.asksaveasfilename(initialdir = "/",title = "Save as",filetypes = (("Python files","*.txt"),("All files","*.*"))))

        def action(self):
            self.log_win = tk.Toplevel()
            self.log_win.geometry("700x375")
            self.log_win['background'] = 'DeepSkyBlue3'
            self.log_win.title("Admin Flight Log")
            # set log_window unresizable
            self.log_win.resizable(False, False)
            self.txt = tk.Text(self.log_win)
            self.txt.place(x=68, y=0)
            # buttons
            log_pause_button = tk.Button(self.log_win, text="Pause", bg="LightBlue3", width=7, command=self.change_data_status_to_0)
            log_pause_button.place(x=5, y=10)
            log_resume_button = tk.Button(self.log_win, text="Resume", bg="LightBlue3", width=7, command=self.change_data_status_to_1)
            log_resume_button.place(x=5, y=40)
            log_clear_button = tk.Button(self.log_win, text="Clear Log", bg="LightBlue3", width=7, command=self.clear_log)
            log_clear_button.place(x=5, y=310)
            log_save_button = tk.Button(self.log_win, text="Save Log", bg="LightBlue3", width=7, command=self.log_save)
            log_save_button.place(x=5, y=340)
            # threading
            self.log_thread = threading.Thread(target=self.add_data, args=("Data Printed Here", None))
            self.log_thread.setDaemon(True)
            self.log_thread.start()
            self.log_win.protocol("WM_DELETE_WINDOW", self.close_log_window)


    # create new window for admin logger
    def log_window():
        a = AdminLogger()


    # flight log button
    flight_log_button = tk.Button(window, text="Admin Flight Log", bg="LightBlue3", command=log_window)
    flight_log_button.place(x=293, y=155)

    # exit button
    exit_button = tk.Button(window, text="Send", bg="LightBlue3", command=lambda: process_com_to_drone(com_to_drone.get()))
    exit_icon = ImageTk.PhotoImage(file="exit_icon_small.jpg")
    exit_button.config(image=exit_icon,width="48",height="32",bd=0,borderwidth=0,command=lambda: on_closing(window))
    exit_button.place(x=540, y=480)


    #window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window))

    update_inet_data(inet_param_data)
    update_mav_data(mav_param_data)
    update_cam_data(cam_param_data)
    update_armed_data(armed_data)
    # mainloop
    window.mainloop()
    return window

#start_gui()


# Parameters to edit:
# inet_delay, cam_str, mav_str

#############################################################################
#----------------------------------Client-----------------------------------#
#############################################################################
# create the socket
# AF_INET == ipv4
# SOCK_STREAM == TCP

"""
print("Rotem")
# This part will be before the gui
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('147.234.54.189', 12341)) # net stick
#s.connect(('10.0.0.10', 12341))

print("connected\n")
s.sendall(bytes("connected", "utf-8"))
# This part will be after the gui


start_time = time.time()

active = True

to_send = "CD"

empty_msg = bytes("", "utf-8")

dict = {'ALIVE': to_send, 'TIME': ''}
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
        print("elapsed", elapsed_time)
        print("ready_to_read", ready_to_read)
        if len(ready_to_read) > 0:
            recv_msg = s.recv(1024)
            if recv_msg == empty_msg:
                continue
            start_time = time.time()
            print("begin")
            print("server msg: ", recv_msg)
            # translate recv_msg to dictionary
            # inet_delay = 0
            # mav_str = "DOWN"
            # cam_str = "DOWN"
            print('end')
        if len(ready_to_write) > 0:
            dict['time'] = str(time.time())
            print("dict:", dict)
            str_dict = json.dumps(dict)
            print("str dict: ", str_dict)
            s.sendall(bytes(str_dict, "utf-8"))
        if elapsed_time > 10:
            active = False
        # try:
        #     print('begin')
        #     recv_msg = s.recv(32)
        #     print("end")
        #     print("server msg: ", recv_msg)
        #     dict['time'] = str(time.time())
        #     str_dict = json.dumps(dict)
        #     s.sendall(bytes(str_dict, "utf-8"))
        #     print(dict)
        #     elapsed_time = time.time() - start_time
        #     if recv_msg != empty_msg:
        #         start_time = time.time()
        #     print(elapsed_time)
        #     if elapsed_time > 10:
        #         print("Connection lost")
        #         active = False
        # except TimeoutError:
        #     print("Connection lost")
        #     active = False
    else:
        print("Trying to reconnect")
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect((socket.gethostname(), 12341)) same pc
        try:
            #s.connect(('147.234.54.189', 12341)) # net stick
            s.connect(('10.0.0.10', 12341))
        except OSError:
            time.sleep(1)
            continue
        print("Reconnected")
        active = True
        start_time = time.time()
    time.sleep(1)

# time.sleep(2)
# s.shutdown(socket.SHUT_RDWR)
# time.sleep(3)
s.close()
"""


