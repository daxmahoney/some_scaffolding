import os.path


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return (f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory")

        information = os.listdir(target_dir)
        information_holder = {}
        for info in information:
            information_holder[info] = (os.path.getsize(os.path.join(target_dir,info)), str(os.path.isdir(os.path.join(target_dir,info))))

        giant_string_answer = []
        if directory == ".":
            directory = "current"
        giant_string_answer.append(f"Result for '{directory}' directory:")
        for k,v in information_holder.items():
            giant_string_answer.append(f" - {k}: file_size={v[0]}, is_dir={v[1]}")
        return "\n".join(giant_string_answer)
        #return f'Success: "{directory}" is within the working directory'
    except Exception as err:
        return f"Error: {err}"