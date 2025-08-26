import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dll_analyzer import extract_dll_sources

def main():
    """
    Main function for processing DLL files
    """
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(script_dir, "extracted_sources")
    
    print("=" * 50)
    print("DLL Source Extractor")
    print("=" * 50)
    print(f"Searching for DLL files in: {script_dir}")
    print(f"Results will be saved in: {output_dir}")
    print("=" * 50)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    dll_files = []
    for filename in os.listdir(script_dir):
        if filename.lower().endswith('.dll'):
            dll_files.append(os.path.join(script_dir, filename))
    
    if not dll_files:
        print("No DLL files found in the current folder!")
        print("Place DLL files in the same folder as this script and run again.")
        input("Press Enter to exit...")
        return
    
    print(f"Found DLL files: {len(dll_files)}")
    
    for dll_path in dll_files:
        extract_dll_sources(dll_path, output_dir)
    
    print("=" * 50)
    print("Processing completed!")
    print("=" * 50)
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
