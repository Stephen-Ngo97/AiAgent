import os

def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))
        #If longest common path is the working directory, then the target directory is valid
        is_valid_target_path = os.path.commonpath([working_directory_abs, target_file_path]) == working_directory_abs
        # Exit if directory is outside of permitted working directory
        if not is_valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        # Read first 10000 characters from file

    except Exception as e:
        return f'Error: {e}'