# SPDX-License-Identifier: MIT
import time

#
# A set of helpers for simple network operations that may be used across projects
#


# Attempt a ping to see if the LAN is connected to the WAN
# Return True or False
# For CircuitPython
def cpy_wan_active():
    import ipaddress
    import wifi
    ping_ip = ipaddress.IPv4Address("8.8.8.8")
    ping_response = wifi.radio.ping(ping_ip)
    if ping_response is None:
        # Sleep for 5 seconds and try again
        time.sleep(1)
        ping_response = wifi.radio.ping(ping_ip)

    if ping_response is None:
        return False
    else:
        return True

# Attempt a ping to see if the LAN is connected to the WAN
# Return True or False
# For Python
def py_wan_active():
    from scapy.sendrecv import sr
    from scapy.layers.inet import IP
    ping =  IP(dst='8.8.8.8')
    response = sr(ping)
    return response

