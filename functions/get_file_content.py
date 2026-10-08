import os
from config import MAX_CHARACTERS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        dir_file_path = os.path.normpath(os.path.join(absolute_working_directory, file_path))
        valid_file_path = os.path.commonpath([absolute_working_directory, dir_file_path]) == absolute_working_directory
        if valid_file_path == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(dir_file_path) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(dir_file_path, "r") as f:
            file_content = f.read(MAX_CHARACTERS)
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'
        return file_content
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "reads the files content from specified file, providing files content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, relative to the working directory (default is the working directory itself)",
                },
            },
        "required": ["file_path"],
        },
    },
}