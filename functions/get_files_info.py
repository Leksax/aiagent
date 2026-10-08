import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_working_directory, directory))
        valid_target_dir = os.path.commonpath([absolute_working_directory, target_dir]) == absolute_working_directory
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        results = []
        try:
            for item in os.listdir(target_dir):
                name = item
                full_path = os.path.join(target_dir, item)
                size = os.path.getsize(full_path)
                isdir = os.path.isdir(full_path)
                name_string = f"- {name}:"
                size_string = f"file_size={size} bytes,"
                isdir_string = f"is_dir={isdir}"
                result_string = " ".join([name_string, size_string, isdir_string])
                results.append(result_string)   
            return "\n".join(results)
        except Exception as e:
            return f"Error: {e}"
    except:
        return f'Error: tried and failed'

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