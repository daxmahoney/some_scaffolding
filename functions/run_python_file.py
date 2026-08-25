import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "executes a specified python file to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path to python file",},
                "args": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "list of arguments that are strings for the python file",},
        },
      "required": ["file_path"]},
}}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:      
        working_dir_abs = os.path.abspath(working_directory)
        target_path_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_path_abs]) == working_dir_abs
        if not valid_target_dir:
            return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_path_abs.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path_abs]
        if args:
            command.extend(args)
        creation = subprocess.run(command, capture_output=True, text=True, timeout=30)
        error_string = ""
        if creation.returncode != 0:
            error_string +=  f"Process exited with code {creation.returncode}\n"
        if not creation.stderr and not creation.stdout:
            error_string += f"No output produced"
        else:
            if creation.stdout:
                error_string += f"STDOUT: {creation.stdout}"
            if creation.stderr:
                error_string += f"STDERR: {creation.stderr}"

        return error_string
    
    except Exception as e:
        return f"Error: {e}"