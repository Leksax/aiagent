import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        dir_file_path = os.path.normpath(os.path.join(absolute_working_directory, file_path))
        valid_file_path = os.path.commonpath([absolute_working_directory, dir_file_path]) == absolute_working_directory
        if valid_file_path == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(dir_file_path) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path.endswith(".py") == False:
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", dir_file_path]
        if args:
            command.extend(args)
        result = subprocess.run(command, cwd=absolute_working_directory, capture_output=True, text=True, timeout=30)
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes (runs) a python file and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file that needs to be executed (run)",
                },
                "args":{
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "optional command-line arguments to pass to the script"
                }
            },
        "required": ["file_path"],
        },
    },
}