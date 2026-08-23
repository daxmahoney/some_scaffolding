import os
# from config import MAX_CHARS

MAX_CHARS = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
    # is file path in working directory
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_path_abs]) == working_dir_abs
        if not valid_target_dir:
            raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_path_abs):
            raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')

        with open(target_path_abs, 'r') as f:
            contents = f.read(MAX_CHARS)
            if f.read(1):
                contents += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return contents

    except Exception as err:
        return f"Error: {err}"
