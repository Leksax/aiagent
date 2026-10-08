import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        dir_file_path = os.path.normpath(os.path.join(absolute_working_directory, file_path))
        valid_file_path = os.path.commonpath([absolute_working_directory, dir_file_path]) == absolute_working_directory
        if valid_file_path == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(dir_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(dir_file_path), exist_ok=True)
        with open(dir_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "overwrites the contents of a file or creates a new file with a given file_path and content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "contents of a rewritten file",
                }
            },
        "required": ["file_path", "content"],
        },
    },
}