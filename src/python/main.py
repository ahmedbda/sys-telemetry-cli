import os
import sys    

# importing modules with their paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from modules.system import SystemProbe
from modules.network import NetworkProbe

if __name__ == "__main__":
    print("Starting Telemetry CLI")
    # initializing the class
    sys_probe = SystemProbe()
    net_probe = NetworkProbe()

    # calling the publics functions for the complete reports
    sysres = sys_probe.run()
    netres = net_probe.run()
    
    # printing all the information

    # using f strings instead of normal strings because they handle variable types automatically 
    # (like for the debugger bool in the string, a simple print with a concatenation (+) would give an error)
    print("-"*20)
    print("System Report")
    print(f"User name: {sysres['user']}")
    print(f"Computer name: {sysres['computer']}")
    print(f"Debugger active: {sysres['is_debugger_active']}")

    print("-"*20)
    print("Network Report")
    print(f"Number of scanned ports: {netres['scanned_ports_count']}")
    print(f"Open ports: {netres['open']}")
    print(f"Closed ports: {netres['closed']}")
    print(f"Ports returning an error: {netres['error']}")
    print(f"Network status: {netres['status']}")