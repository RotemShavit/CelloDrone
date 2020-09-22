# from dronekit import *
import dronekit
from time import *
import math
from geopy.distance import distance

FALLBACK_DELAY = 5
HOT_SPOT_CALC_DELAY = 100
SAVED_HOT_SPOTS_LIMIT = 100
EARTH_RADIUS = 6371


#testing_latency = [25, 33, 62, 19, 42, 168, 215, 12, 33, 82, 45, 91, 189, 9, 3, 86, 22, 120, 210, 250, 189, 156, 225]
#testing_gps = [[31.7764973, 35.1983572], [31.7774236, 35.198836], [31.7772409, 35.1987201], [31.7774899, 35.1985116], [31.7781795, 35.198624], [31.7786637, 35.1986385], [31.7789308, 35.1979564], [31.7790324, 35.1965297], [31.7782517, 35.196409], [31.7783573, 35.1954475], [31.7776658, 35.1959596], [31.7771649, 35.195539], [31.7771649, 35.195539], [31.777339, 35.1955645], [31.7762992, 35.1975628], [31.7761411, 35.1967182], [31.7757884, 35.1981088], [31.7751069, 35.1979823], [31.7750948, 35.1989418], [31.7750948, 35.1989418], [31.7757594, 35.1990273], [31.7750543, 35.1989047]]

class FallbackClass:
    def __init__(self):
        self.hot_spot_list = []
        self.distance_list = []
        self.hot_spot_to_return = ["",""]
        self.fallback_counter = 0

    def change_hot_spot(self, coord):
        self.hot_spot_to_return[0] = coord[0]
        self.hot_spot_to_return[1] = coord[1]

    def count_fallback(self):
        self.fallback_counter = self.fallback_counter + 1


def hot_spot_calc(fb, hot_spot_list, distance_list, cur_gps_lat, cur_gps_lon):
    hot_spot_list.append([cur_gps_lat, cur_gps_lon])
    distance_list.append(0)
    if len(hot_spot_list) > SAVED_HOT_SPOTS_LIMIT:
        hot_spot_list = hot_spot_list[1:]
        distance_list = distance_list[1:]
    min_distance = -1
    for location_idx in range(len(hot_spot_list)):
        #distance_to_current = sqrt(pow((cur_gps_lat-hot_spot_list[location_idx][0]), 2) + pow((cur_gps_lon-hot_spot_list[location_idx][1]), 2))
        # calculation of distance:
        # a = (math.sin(math.radians((cur_gps_lat-hot_spot_list[location_idx][0])/2)))**2 + math.cos(math.radians((cur_gps_lat)*math.cos(hot_spot_list[location_idx][0])))*(math.sin(math.radians((cur_gps_lon-hot_spot_list[location_idx][1])/2)))**2
        # c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        # d = EARTH_RADIUS*c
        d = distance((cur_gps_lat, cur_gps_lon), (hot_spot_list[location_idx][0], hot_spot_list[location_idx][1]))
        ####
        distance_list[location_idx] = d.km
        if ((distance_list[location_idx] < min_distance) & (distance_list[location_idx] > 0)) | (min_distance == -1):
            min_distance = distance_list[location_idx]
            hot_spot_lat_to_fallback = hot_spot_list[location_idx][0]
            hot_spot_lon_to_fallback = hot_spot_list[location_idx][1]
            fb.change_hot_spot([hot_spot_lat_to_fallback, hot_spot_lon_to_fallback])
    #print("Current Fallback Location: " + str([hot_spot_lat_to_fallback, hot_spot_lon_to_fallback]))
    print("\n")

def start_fallback(data_list):
    fb = FallbackClass()
    low_latency_counter = 0
    is_fallback_active = 1
    # while True:
    while True:
        if(data_list[5] == 1):
            is_fallback_activated = 1
        if(is_fallback_active==1):
            # print("fallback_counter = " + str(fb.fallback_counter))
            # print("low_latency_counter = " + str(low_latency_counter))
            #print("Operation Time: " + str(i) + " sec")
            #cur_gps_lat_str = str(testing_gps[i][0])  # probably how we get gps by command like vehicle.getgps() or something like this
            #cur_gps_lon_str = str(testing_gps[i][1])
            cur_gps_lat = data_list[6].location.global_frame.lat
            cur_gps_lon = data_list[6].location.global_frame.lon
            #delay_cur_gps = float(testing_latency[i])  # the socket delay in seconds for the last message. need to change to real parameter
            delay_cur_gps = float(data_list[2]) # reak delay
            if int(delay_cur_gps) != -1:
                print("Current latency: " + str(delay_cur_gps) + " ms.")
                print("Current GPS: " + cur_gps_lat_str + ", " + cur_gps_lon_str)
            #print(data_list)
            # delay_cur_gps = int(delay_cur_gps_str)
            if delay_cur_gps < HOT_SPOT_CALC_DELAY:
                low_latency_counter = low_latency_counter + 1
                # print("Low latency (" + str(delay_cur_gps) + ")")
                hot_spot_calc(fb, fb.hot_spot_list, fb.distance_list, cur_gps_lat, cur_gps_lon)
                if low_latency_counter > 3:
                    fb.fallback_counter = 0
                    low_latency_counter = 0
            elif delay_cur_gps >= HOT_SPOT_CALC_DELAY:
                # print("High latency (" + str(delay_cur_gps) + ")")
                fb.fallback_counter = fb.fallback_counter + 1
                low_latency_counter = 0
            if (fb.fallback_counter >= FALLBACK_DELAY) | (data_list[1] == 0):  # number of seconds to activate fallback
                print("Fallback Activated.")
                print("Hot spot GPS destination: " + str(fb.hot_spot_to_return))
                if fb.hot_spot_to_return[0] == "":
                        fb.hot_spot_to_return[0] = data_list[6].home_location.lat
                        fb.hot_spot_to_return[1] = data_list[6].home_location.lon
                fallback_lat = fb.hot_spot_to_return[0]
                fallback_lon = fb.hot_spot_to_return[1]
                fallback_location = dronekit.LocationGlobal(fallback_lat, fallback_lon, alt=40) # set location object for dronekit
                fb.fallback_counter = 0
                data_list[1] = 0
                data_list[3] = fallback_lat
                data_list[4] = fallback_lon
                data_list[5] = 0
                is_fallback_active = 0
                #data_list[6].mode = dronekit.VehicleMode("STABILIZE")
                #data_list[6].armed = True
                #while data_list[6].armed != True:
                    #data_list[6].armed = True
                    #data_list[6].flush()
                    #print ("mode?", str(data_list[6].mode))
                    #print ("is armable?", data_list[6].is_armable)
                    #print("is armed?", data_list[6].armed)
                    #print ("not armed yet")
                    #sleep(1)
                #print("is armed?", data_list[6].armed)
                data_list[6].mode = dronekit.VehicleMode("GUIDED")
                #print("is guided?", str(data_list[6].mode))
                #data_list[6].flush()
                # REMEMBER TO SWITCH TO GUIDED MODE
                # IF SIGNAL IS RETRIEVED THEN SWITCH TO STABLE
                
                #data_list[6].airspeed=300
                try:
                    data_list[6].simple_goto(fallback_location, airspeed = 12) # simple_goto(location, airspeed=None, groundspeed=None) | speed = 8 m/s
                except:
                    data_list[6].mode = dronekit.VehicleMode("RTL")
                    print("Unexpected Error: Please try again.")
                    data_list[7] = 1
                    break
                    
                #point1 = dronekit.LocationGlobal(-35.361354, 149165218, 20)
                #data_list[6].simple_goto(point1, 300) # simple_goto(location, airspeed=None, groundspeed=None)
                #sleep(10)
                #data_list[6].mode = dronekit.VehicleMode("RTL")
            # print("\n")
        sleep(1)

#################################