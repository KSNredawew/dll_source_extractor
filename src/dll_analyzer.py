import os
import pefile
from utils import is_likely_source_code
from file_saver import save_source_file, create_demo_files

def extract_dll_sources(dll_path, output_dir):
    """
    Extracts C/C++ source files from DLL
    """
    try:
        print(f"\nProcessing DLL: {os.path.basename(dll_path)}")
        pe = pefile.PE(dll_path)
        
        dll_name = os.path.splitext(os.path.basename(dll_path))[0]
        source_dir = os.path.join(output_dir, dll_name + "_sources")
        
        if not os.path.exists(source_dir):
            os.makedirs(source_dir)
        
        found_sources = False
        for section in pe.sections:
            section_name = section.Name.decode('utf-8').rstrip('\x00')
            section_data = section.get_data()
            
            if is_likely_source_code(section_data):
                save_source_file(section_data, source_dir, f"section_{section_name}")
                found_sources = True
                print(f"  Found source code in section: {section_name}")
        
        if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
            for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                if hasattr(resource_type, 'directory'):
                    for resource_id in resource_type.directory.entries:
                        if hasattr(resource_id, 'directory'):
                            for resource_lang in resource_id.directory.entries:
                                try:
                                    resource_data = pe.get_data(
                                        resource_lang.data.struct.OffsetToData,
                                        resource_lang.data.struct.Size
                                    )
                                    
                                    if is_likely_source_code(resource_data):
                                        if resource_type.name is not None:
                                            type_name = str(resource_type.name)
                                        else:
                                            type_name = f"res_{resource_type.struct.Id}"
                                        
                                        resource_id_name = f"id_{resource_id.struct.Id}"
                                        if resource_id.name is not None:
                                            resource_id_name = str(resource_id.name)
                                        
                                        save_source_file(resource_data, source_dir, f"{type_name}_{resource_id_name}")
                                        found_sources = True
                                        print(f"  Found source code in resource: {type_name}_{resource_id_name}")
                                        
                                except Exception as e:
                                    continue
        
        if not found_sources:
            print("  No C/C++ source code found in DLL")
            create_demo_files(source_dir, dll_name)
            
    except Exception as e:
        print(f"Error processing file {os.path.basename(dll_path)}: {e}")
