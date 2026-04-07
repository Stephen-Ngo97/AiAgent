from ntpath import isdir
import os

def write_file(working_directory, file_path, content):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))
        #If longest common path is the working directory, then the target directory is valid
        is_valid_target_path = os.path.commonpath([working_directory_abs, target_file_path]) == working_directory_abs
        # Exit if directory is outside of permitted working directory
        if not is_valid_target_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        # Create parent directory if not already existing
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
        with open(target_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'