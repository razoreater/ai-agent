import os
from os.path import normpath

def get_files_info(working_directory, directory="."):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))

        # Check if the target_dir is within the working_directory
        try:
            common_path = os.path.commonpath([absolute_path, target_dir])
        except ValueError:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if common_path != absolute_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the target_dir exists and is a directory
        if not os.path.exists(target_dir):
            return f'Error: "{target_dir}" does not exist'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # List files and directories in target_dir
        lines = []
        try:
            for item in os.listdir(target_dir):
                item_path = os.path.join(target_dir, item)
                try:
                    size = os.path.getsize(item_path)
                    is_dir = os.path.isdir(item_path)
                    lines.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
                except OSError as e:
                    lines.append(f"- {item}: Error: {str(e)}")
        except OSError as e:
            return f'Error: Could not list contents of "{target_dir}": {str(e)}'

        return "\n".join(lines)

    except Exception as e:
        return f'Error: {str(e)}'
