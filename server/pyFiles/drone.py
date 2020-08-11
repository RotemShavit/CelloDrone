from fallback import start_fallback
from server import start_server
import threading

data_list = [0,1,-1, -1, -1]
# [first_connection, client_up, current_latency, fallback GPS lat, fallback GPS lon] 0 - NO, 1 = YES, -1 = starting false value

thread = threading.Thread(target=start_server, args=[data_list])

print "Server is UP"

thread.start()
while(data_list[0] == 0):
    continue

print "Fallback is UP"

start_fallback(data_list)
thread.join()
exit(0)