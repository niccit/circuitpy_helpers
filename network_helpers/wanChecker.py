# SPDX-License-Identifier: MIT
import ipaddress
import wifi
import time

#
# A set of helpers for simple network operations that may be used across projects
#


# Attempt a ping to see if the LAN is connected to the WAN
# Return True or False
def wan_active(radio):
    ping_ip = ipaddress.IPv4Address("8.8.8.8")
    ping_response = wifi.radio.ping(ping_ip)
    if ping_response is None:
        # Sleep for 5 seconds and try again
        time.sleep(5)
        ping_response = wifi.radio.ping(ping_ip)

    if ping_response is None:
        return False
    else:
        return True