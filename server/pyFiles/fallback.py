# from dronekit import *
import dronekit
from time import *
import math
from geopy.distance import distance

FALLBACK_DELAY = 10
HOT_SPOT_CALC_DELAY = 100
SAVED_HOT_SPOTS_LIMIT = 100
EARTH_RADIUS = 6371


testing_latency = [38, 92, 76, 34, 100, 110, 143, 165, 106, 143, 104, 155, 133, 120, 89, 80, 90]
testing_gps = [[32.079341, 34.802888], [32.079336, 34.802708], [32.079560, 34.802128], [32.080028, 34.802182], [32.080214, 34.802552], [32.080287, 34.802911], [32.080268, 34.803295], [32.080568, 34.803628], [32.080350, 34.803875], [32.080045, 34.804014], [32.079759, 34.803665], [32.079470, 34.803408], [32.079693, 34.803059], [32.079798, 34.802528], [32.079503, 34.802008], [32.079434, 34.802539], [32.079334, 34.802909]]

### TODO- Need to add variable in a class - make the counter increament if connection is lost and not only high latency
### TODO- when fallback is activated, stop iterating gps points
### TODO- when fallback is activated, need to make disconnection for server (even if still up) & reconnect it only when reached fallback gps location
### TODO- if reconnection cannot be established after 15 seconds, return home
class FallbackClass:
    def __init__(self):
        self.hot_spot_list = []
        self.distance_list = []
        self.hot_spot_to_return = ["", ""]
        self.fallback_counter = 0

    def change_hot_spot(self, coord):
        self.hot_spot_to_return[0] = coord[0]
        self.hot_spot_to_return[1] = coord[1]

    def count_fallback(self):
        self.fallback_counter = self.fallback_counter + 1


fb = FallbackClass()


def hot_spot_calc(hot_spot_list, distance_list, cur_gps_lat, cur_gps_lon):
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
    print("Current Fallback Location: " + str([hot_spot_lat_to_fallback, hot_spot_lon_to_fallback]))
    print("\n")

i = 0
low_latency_counter = 0
# while True:
while i < len(testing_latency):
    # print("fallback_counter = " + str(fb.fallback_counter))
    # print("low_latency_counter = " + str(low_latency_counter))
    print("Operation Time: " + str(i) + " sec")
    cur_gps_lat_str = str(testing_gps[i][0])  # probably how we get gps by command like vehicle.getgps() or something like this
    cur_gps_lon_str = str(testing_gps[i][1])
    cur_gps_lat = float(cur_gps_lat_str)
    cur_gps_lon = float(cur_gps_lon_str)
    delay_cur_gps_str = str(testing_latency[i])  # the socket delay in seconds for the last message. need to change to real parameter
    delay_cur_gps = int(delay_cur_gps_str)
    i = i + 1
    if delay_cur_gps < HOT_SPOT_CALC_DELAY:
        low_latency_counter = low_latency_counter + 1
        # print("Low latency (" + str(delay_cur_gps) + ")")
        hot_spot_calc(fb.hot_spot_list, fb.distance_list, cur_gps_lat, cur_gps_lon)
        if low_latency_counter > 3:
            fb.fallback_counter = 0
            low_latency_counter = 0
    elif delay_cur_gps >= HOT_SPOT_CALC_DELAY:
        # print("High latency (" + str(delay_cur_gps) + ")")
        fb.fallback_counter = fb.fallback_counter + 1
        low_latency_counter = 0
    if fb.fallback_counter >= FALLBACK_DELAY:  # number of seconds to activate fallback
        print("Fallback Activated")
        fallback_lat = fb.hot_spot_to_return[0]
        fallback_lon = fb.hot_spot_to_return[1]
        print("Returning to GPS Location: " + "[" + str(fb.hot_spot_to_return[0]) + ", " + str(fb.hot_spot_to_return[1]) + "]")
        fallback_location = dronekit.LocationGlobal(fallback_lat, fallback_lon, alt=10) # set location object for dronekit
        fb.fallback_counter = 0
        # REMEMBER TO SWITCH TO GUIDED MODE
        # IF SIGNAL IS RETRIEVED THEN SWITCH TO STABLE
        # vehicle.simple_goto(fallback_location) # simple_goto(location, airspeed=None, groundspeed=None)
    # print("\n")
    sleep(1)

#################################


