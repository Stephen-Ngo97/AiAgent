import os

def get_files_info(working_directory, directory ="."):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(working_directory_abs, directory))
        #If longest common path is the working directory, then the target directory is valid
        is_valid_target_directory = os.path.commonpath([working_directory_abs, target_directory]) == working_directory_abs
        # Exit if directory is outside of permitted working directory
        if not is_valid_target_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'
        # Get list of files and directories in target directory
        files_and_dirs = os.listdir(target_directory)
        # Get directory contents as a string
        contents_list = []
        for item in files_and_dirs:
            file_size = os.path.getsize(os.path.join(target_directory, item))
            if os.path.isfile(os.path.join(target_directory, item)):
                contents_list.append(f'- {item}: file_size={file_size} bytes, is_dir=False')
            elif os.path.isdir(os.path.join(target_directory, item)):
                contents_list.append(f'- {item}: file_size={file_size} bytes, is_dir=True')
        # Return directory contents as a string
        return '\n'.join(contents_list)
    except Exception as e:
        return f'Error: {e}'
