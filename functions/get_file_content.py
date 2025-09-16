import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory: str,file_path: str):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: {file_path} is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f"Error: The file {abs_file_path} does not exist."

    file_content = ""
    try:
        with open(abs_file_path, 'r') as file:
            file_content = file.read(MAX_CHARS)
            if len(file_content) >= MAX_CHARS:
                file_content += (f'[...File "{file_path}" truncated after {MAX_CHARS} characters...]')
        return file_content
    except Exception as e:
        return f"Error: Unable to read the file {abs_file_path}. Reason: {str(e)}."
    except UnicodeDecodeError:
        return f"Error: The file {abs_file_path} is not a readable file or contains unsupported characters."


