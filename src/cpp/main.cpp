#include <windows.h>

// using C naming rules so this C++ code can by called by the python main without errors (name mangling)
extern "C" {    
    // __declspec(dllexport) to export our library in a dll format when compiling 
    __declspec(dllexport) bool IsDebuggerDetected(){
        return IsDebuggerPresent(); // from the windows header
    }

    __declspec(dllexport) void GetSystemUserName(char* buffer, int size) {
    // typecasting the int (python) to a DWORD (the unsigned int of windows, so we get no errors when calling the function) 
    DWORD bufferSize = size;
    GetUserNameA(buffer, &bufferSize); // from the windows header 
    }

    // works the same as GetUserNameA
    __declspec(dllexport) void GetSystemComputerName(char* buffer, int size) {
    DWORD bufferSize = size;
    GetComputerNameA(buffer, &bufferSize);  
    }
}