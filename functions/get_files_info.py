import os

def get_files_info(working_dir, dir = "."):
    abs_working_dir = os.path.abspath(working_dir)
    abs_dir = os.path.abspath(os.path.join(working_dir,dir))
        
    if not abs_dir.startswith(abs_working_dir):
        return f'Error: {dir} is outside the permitted working directory'
    
    if not os.path.isdir(abs_dir):
        return f"Error: The directory {abs_dir} doesn not exist."
    response = ""
    contents = os.listdir(abs_dir)
    try:
        for content in contents:
            path = os.path.join(abs_dir,content)
            is_dir = os.path.isdir(path)
            size = os.path.getsize(path) if not is_dir else "N/A"
            response += f"\n- {content}: file_size= {size} bytes, is_dir= {is_dir}\n"
    except OSError as e:
        return f"Error: Could not access directory {abs_dir}. Reason: {e}"
            
    return response    
    
    