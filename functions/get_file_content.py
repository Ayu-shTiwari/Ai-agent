import os
from config import MAX_FILE_SIZE
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
            file_content = file.read(MAX_FILE_SIZE)
            if len(file_content) >= MAX_FILE_SIZE:
                file_content += (f'[...File "{file_path}" truncated after {MAX_FILE_SIZE} characters...]')
        return file_content
    except Exception as e:
        return f"Error: Unable to read the file {abs_file_path}. Reason: {str(e)}."
    except UnicodeDecodeError:
        return f"Error: The file {abs_file_path} is not a readable file or contains unsupported characters."
    
schema_get_files_content = types.FunctionDeclaration(
    name="get_files_content",
    description="Retrieves the content of a specific file as a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve content from, relative to the working directory.",
            ),
        },
    ),
)