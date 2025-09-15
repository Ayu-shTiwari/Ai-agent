import os
from config import MAX_FILE_SIZE

def get_file_content(working_dir,file_path):
    abs_working_dir = os.path.abspath(working_dir)
    abs_file_path = os.path.abspath(os.path.join(working_dir,file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: {file_path} is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f"Error: The file {abs_file_path} does not exist."

    file_content = ""
    try:
        with open(abs_file_path, 'r') as file:
            file_content = file.read(MAX_FILE_SIZE)
            if len(file_content) >= MAX_FILE_SIZE:
                file_content += (f'[...File "{file_path}" truncated after {MAX_FILE_SIZE} characters...]')
        return file_content
    except Exception as e:
        return f"Error: Unable to read the file {abs_file_path}. Reason: {str(e)}."
    except UnicodeDecodeError:
        return f"Error: The file {abs_file_path} is not a readable file or contains unsupported characters."
    
