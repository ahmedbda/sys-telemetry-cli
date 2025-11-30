import socket
from .interface import Probe

# system information fetching
class NetworkProbe(Probe):
    def __init__(self):
        # 21 : FTP port, file transfer protocol
        # 80 : HTTP port, unsecure web
        # 443 : HTTPS port, secure web
        # 22 : SSH port, secure shell and admin entry
        # 3389 : windows remote desktop protocol, primary targer for ransomwares
        self.ports = [21, 80, 443, 22, 3389]

    def _check_port(self, port: int):
        # initializing socket, AF_INET for Adress Family ipv4 and SOCK_STREAM for TCP (more secure than UDP)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 0.5 second max checking time to not block the code when calling a silent port
        sock.settimeout(0.5)

        try:            
            # using connect_ex instead of connect to have an error code instead of a bug in case of a problem
            result = sock.connect_ex(("127.0.0.1", port)) # 127.0.0.1 for the local host
            if result == 0: # if all went well and port open   
                return "O"
            else:
                return "C"
        except Exception as e:
            return str(port) + ": " + str(e)
        finally:
            sock.close() # closing sock when not needed anymore

    def run(self):
        open_ports = []
        closed_ports = []
        error_ports = []

        # checking every port with the self function and storing them in the right place
        for port in self.ports:
            status = self._check_port(port)
            if status == "O":
                open_ports.append(port)
            elif status == "C":
                closed_ports.append(port)
            else:
                error_ports.append(status)
        
        return {
            "scanned_ports_count": len(self.ports),
            "open": open_ports if len(open_ports) > 0 else ["None"],
            "closed": closed_ports if len(closed_ports) > 0 else ["None"],
            "error": error_ports if len(error_ports) > 0 else ["None"],
            "status": "Warning" if len(open_ports) > 0 else "Safe"
        }