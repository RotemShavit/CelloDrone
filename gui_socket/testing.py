from dronekit import *

FALLBACK_DELAY = 10
HOT_SPOT_CALC_DELAY = 100
SAVED_HOT_SPOTS_LIMIT = 100


class FallbackClass:
    def __init__(self):
        self.hot_spot_list = []
        self.distance_list = []
        hot_spot_to_return = ["", ""]
        fallback_counter = 0

    def change_hot_spot(self, coord):
        self.hot_spot_to_return[0] = coord[0]
        self.hot_spot_to_return[1] = coord[1]

    def count_fallback(self):
        self.fallback_counter = self.fallback_counter + 1


fb = FallbackClass()


def hot_spot_calc(hot_spot_list, distance_list, cur_gps_lat, cur_gps_lon):
    hot_spot_list.append([cur_gps_lat, cur_gps_lon])
    for location in hot_spot_list:
        if len(hot_spot_list) > SAVED_HOT_SPOTS_LIMIT:
            hot_spot_list = hot_spot_list[1:]
            distance_list = distance_list[1:]
        distance_to_current = sqrt(pow(cur_gps_lat-hot_spot_list[location][0]) + pow(cur_gps_lon-hot_spot_list[location][1]))
        distance_list.append(distance_to_current)
    min_distance = distance_list[0]
    for distance_idx in distance_list:
        if distance_list[distance_idx] < min_distance:
            min_distance = distance_list[distance_idx]
            hot_spot_lat_to_fallback = hot_spot_list[distance_idx][0]
            hot_spot_lon_to_fallback = hot_spot_list[distance_idx][1]
            fb.change_hot_spot([hot_spot_lat_to_fallback, hot_spot_lon_to_fallback])
    return fb.hot_spot_to_return


while True:
    sleep(1)
    cur_gps_lat_str = str(111111.111111)  # probably how we get gps by command like vehicle.getgps() or something like this
    cur_gps_lon_str = str(222222.222222)
    cur_gps_lat = int(cur_gps_lat_str)
    cur_gps_lon = int(cur_gps_lon_str)
    delay_cur_gps_str = str(68)  # the socket delay in seconds for the last message. need to change to real parameter
    delay_cur_gps = int(delay_cur_gps_str)
    if delay_cur_gps < HOT_SPOT_CALC_DELAY:
        fb.hot_spot_to_return = hot_spot_calc(hot_spot_list, distance_list, cur_gps_lat, cur_gps_lon, delay_cur_gps)
    elif delay_cur_gps > HOT_SPOT_CALC_DELAY & fb.fallback_counter > 3:
        fb.fallback_counter = fb.fallback_counter + 1
    if fb.fallback_counter > FALLBACK_DELAY:  # number of seconds to activate fallback
        fallback_lat = fb.hot_spot_to_return[0]
        fallback_location = LocationGlobal(fb.hot_spot_to_return[0], fb.hot_spot_to_return[1], None, None) # change this accordingly
        vehicle.simple_goto(fallback_location) # simple_goto(location, airspeed=None, groundspeed=None)

#################################
