import os
from os.path import exists, isdir

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
    common_path = os.path.commonpath([abs_working_dir, abs_file_path])
    
    try:
        if common_path != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if  os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        #Check if the directory exists, otherwhise create it:
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        #Open the file an read the first max characters from imported file
        with open(abs_file_path, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as error:
        return f"Error: {error}"


