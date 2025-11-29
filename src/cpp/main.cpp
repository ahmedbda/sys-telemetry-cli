#include <windows.h>
#include <iostream>

// using C naming rules so this C++ code can by called by the python main without errors (name mangling)
extern "C" {    
    //__declspec(dllexport) to export our library in a dll format when compiling 
    __declspec(dllexport) bool IsDebuggerDetected() {
        return IsDebuggerPresent(); 
    }

    //simple testing function to check if the .dll is called properly
    __declspec(dllexport) int Add(int a, int b) {
        return a + b;
    }
}