import os
import sys
import subprocess
from google.genai import types

def run_python_file(working_directory: str, file_path: str, args=None):
    if args is None:
        args = []
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: {file_path} is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} does not exist."
    
    if not file_path.endswith(".py"):
        return f"Error: {file_path} is not a python file"
    
    try:
        final_args = [sys.executable, abs_file_path]
        final_args.extend(args)
        env_vars = os.environ.copy()
        env_vars['PYTHONIOENCODING'] = 'utf-8'
        
        output = subprocess.run(
            final_args,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True,
            text=True,
            encoding='utf-8',
            env=env_vars
        )
        response = f"Process exited with code {output.returncode}\n"
        
        if output.stdout:
            response += f"STDOUT:\n{output.stdout}\n"
        
        if output.stderr:
            response += f"STDERR:\n{output.stderr}\n"
        
        if not output.stdout and not output.stderr:
            response += "No output produced\n"
        
        return response
    
    except Exception as e:
        return f'Error: executing python file: {e}'
    
