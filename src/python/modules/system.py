import ctypes
import os
import sys
from .interface import Probe

# system information fetching
class SystemProbe(Probe):
    def __init__(self):
        # calling the self function to load dll when initializing the class because it is always needed
        self.lib = self._load_dll()
    
    def _load_dll(self):
        # fetching this file"s, the root and  library (dll) path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        dll_path = os.path.join(project_root, "bin", "telemetry.dll")

        try:
            lib = ctypes.CDLL(dll_path) # loading dll library with the path using ctypes and printing the error if one occurs
            # defining the library result/argument types so it is not needed each time it is called
            lib.IsDebuggerDetected.restype = ctypes.c_bool
            lib.GetSystemUserName.argtypes = [ctypes.c_char_p, ctypes.c_int]
            lib.GetSystemComputerName.argtypes = [ctypes.c_char_p, ctypes.c_int]
            return lib 
        except Exception as e:
            print("DLL not found: " + str(e))
            sys.exit(1)

    def _get_username(self):
        try:
            buffer_size = 100 # creating buffer size (max name length)
            buffer = ctypes.create_string_buffer(buffer_size) # buffer adress
            self.lib.GetSystemUserName(buffer, buffer_size)
            return buffer.value.decode("utf-8") # returning and decoding value (bytes b"Admin" to strings "Admin")
        except Exception as e:
            return "User name could not be found: " + str(e)

    def _get_computer_name(self): # same as username
        try:
            buffer_size = 100
            buffer = ctypes.create_string_buffer(buffer_size)
            self.lib.GetSystemComputerName(buffer, buffer_size)
            return buffer.value.decode("utf-8")
        except Exception as e:
            return "Computer name could not be found: " + str(e)

    def _is_debugger_present(self):
        return self.lib.IsDebuggerDetected() # True or False depending on debugger presence

    def run(self):
        # complete report as a dictionnary, public function 
        return {
            "user": self._get_username(),
            "computer": self._get_computer_name(),
            "is_debugger_active": self._is_debugger_present(),
            "status": "Warning" if self._is_debugger_present() else "Safe"
        }