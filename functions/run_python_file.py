import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Runs a python file. In a specified directory relative to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            required=["file_path"],
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
                ),
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file that is requested",
                ),
                "args": types.Schema(
                    type=types.Type.ARRAY,
                    items=types.Schema(type=types.Type.STRING),
                    description="The arguments that we give to the python script"
                ),
            },
        ),
)

def run_python_file(working_directory, file_path, args=None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
    common_path = os.path.commonpath([abs_working_dir, abs_file_path])
    
    try:
        if common_path != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        #create the command
        command = ["python", abs_file_path]
        if args:
            command.extend(args)

        run_process = subprocess.run(
                command,
                cwd=abs_working_dir,
                capture_output=True,
                text=True,
                timeout=30
        )

        output = ""
        if run_process.stdout:
            output += f"STDOUT: {run_process.stdout}"
        if run_process.stderr:
            output += f"STDERR: {run_process.stderr}"
        if run_process.returncode != 0:
            output += f"Process exited with code {run_process.returncode}"
        if not output:
            output = "No output produced."
        
    except Exception as error:
        return f"Error: executing Python file: {error}"
    return output
