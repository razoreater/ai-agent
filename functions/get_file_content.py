import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
    common_path = os.path.commonpath([abs_working_dir, abs_file_path])

    try:
        if common_path != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        #Open the file an read the first max characters from imported file
        with open(abs_file_path, "r") as file:
            data = file.read(MAX_CHARS)
            if file.read(1):
                data += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return data
    except Exception as error:
        return f"Error: {error}"

