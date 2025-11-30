import os
import sys    
import json
import datetime

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
    sys_res = sys_probe.run()
    net_res = net_probe.run()
    
    # printing all the information

    # using f strings instead of normal strings because they handle variable types automatically 
    # (like for the debugger bool in the string, a simple print with a concatenation (+) would give an error)
    print("-"*20)
    print("System Report")
    print(f"User name: {sys_res["user"]}")
    print(f"Computer name: {sys_res["computer"]}")
    print(f"Debugger active: {sys_res["is_debugger_active"]}")
    print(f"System status: {sys_res["status"]}")

    print("-"*20)
    print("Network Report")
    print(f"Number of scanned ports: {net_res["scanned_ports_count"]}")
    print(f"Open ports: {net_res["open"]}")
    print(f"Closed ports: {net_res["closed"]}")
    print(f"Ports returning an error: {net_res["error"]}")
    print(f"Network status: {net_res["status"]}")

    # reporting (/output) and logging (/logs)

    # file paths
    current_path = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.dirname(os.path.dirname(current_path))
    
    output_file = os.path.join(root_path, "output", "report.json")
    logs_file = os.path.join(root_path, "logs", "activity.log")

    # current time in iso (wikipedia: "ISO 8601 is an international standard [...] communication of date and time-related data"
    now = datetime.datetime.now().isoformat()

    # global report dictionnary
    global_rep = {
        "time": now,
        "system_report": sys_res,
        "network_report": net_res
    }

    print("-"*20)

    try:
        # 'w' for write, so we clear the entire file before writing the new report
        with open(output_file, 'w') as f:
            json.dump(global_rep, f, indent=4) # using the json library to write in the file f and 4 for the indent (PEP8 standard)
        print(f"Report saved to: " + (output_file))
    except Exception as e:
        print("Failed to write report: " + str(e))

    # determining risk level by checking that both reports are all safe
    risk_level = "Warning" if sys_res["status"] == "Warning" or net_res["status"] == "Warning" else "Safe"

    # written line that will be added to the log file, f strings for the same reason as cited before
    log_line = f"[{now}] [{risk_level}] Scan complete, ports open: {len(net_res['open'])-1}, debugger: {sys_res['is_debugger_active']}\n"

    try:
        # 'a' for append, meaning we keep the file as is and just add a new line at the bottom
        with open(logs_file, 'a') as f:
            f.write(log_line)
        print("Log sent to (SIEM simulation): " + str(logs_file))
    except Exception as e:
        print("Failed to write logs: " + str(e))