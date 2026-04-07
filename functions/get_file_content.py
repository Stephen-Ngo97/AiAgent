import os
from config import MAX_CHARS_TO_READ_FROM_FILE
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))
        #If longest common path is the working directory, then the target directory is valid
        is_valid_target_path = os.path.commonpath([working_directory_abs, target_file_path]) == working_directory_abs
        # Exit if directory is outside of permitted working directory
        if not is_valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        # Read first 10000 characters from file - append truncation message if more than max chars available in file
        with open(target_file_path, "r") as f:
            file_content = f.read(MAX_CHARS_TO_READ_FROM_FILE)
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS_TO_READ_FROM_FILE} characters]'
        return file_content
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file at the provided path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be read, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"]
    ),
)