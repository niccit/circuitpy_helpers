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
    import subprocess
    import platform
    hostname = "google.com"
    parameter = '-n' if platform.system() == 'Windows' else '-c'
    try:
        subprocess.check_output(["ping", parameter, "1", hostname],
                                stderr=subprocess.STDOUT,
                                timeout=2)
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        return False

