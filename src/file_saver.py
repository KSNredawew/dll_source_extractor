import os

def save_source_file(data, output_dir, base_name):
    """
    Saves data as source file with proper extension
    """
    try:
        text = data.decode('utf-8', errors='ignore')
        
        if '#include' in text or 'int main(' in text or 'void main(' in text:
            extension = '.cpp'
        elif '#define' in text or '#ifdef' in text or '#ifndef' in text:
            extension = '.h'
        else:
            extension = '.c'
          
        file_path = os.path.join(output_dir, f"{base_name}{extension}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
            
    except:
        file_path = os.path.join(output_dir, f"{base_name}.bin")
        with open(file_path, 'wb') as f:
            f.write(data)

def create_demo_files(output_dir, dll_name):
    """
    Creates demo source files if no real ones were found
    """
    with open(os.path.join(output_dir, f"{dll_name}.h"), 'w') as f:
        f.write(f"#ifndef {dll_name.upper()}_H\n")
        f.write(f"#define {dll_name.upper()}_H\n\n")
        f.write("// Header file for DLL\n")
        f.write("// In a real DLL this file might look different\n\n")
        f.write("#ifdef __cplusplus\n")
        f.write('extern "C" {\n')
        f.write("#endif\n\n")
        f.write("__declspec(dllexport) void example_function();\n\n")
        f.write("#ifdef __cplusplus\n")
        f.write("}\n")
        f.write("#endif\n\n")
        f.write(f"#endif // {dll_name.upper()}_H\n")
    
    with open(os.path.join(output_dir, f"{dll_name}.cpp"), 'w') as f:
        f.write(f'#include "{dll_name}.h"\n')
        f.write('#include <windows.h>\n\n')
        f.write('BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {\n')
        f.write('    switch (ul_reason_for_call) {\n')
        f.write('    case DLL_PROCESS_ATTACH:\n')
        f.write('    case DLL_THREAD_ATTACH:\n')
        f.write('    case DLL_THREAD_DETACH:\n')
        f.write('    case DLL_PROCESS_DETACH:\n')
        f.write('        break;\n')
        f.write('    }\n')
        f.write('    return TRUE;\n')
        f.write('}\n\n')
        f.write('__declspec(dllexport) void example_function() {\n')
        f.write('    // Example function\n')
        f.write('}\n')
    
    print(f"  Created demo files for {dll_name}")
