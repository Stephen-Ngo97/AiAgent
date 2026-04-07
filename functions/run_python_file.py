import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))
        #If longest common path is the working directory, then the target directory is valid
        is_valid_target_path = os.path.commonpath([working_directory_abs, target_file_path]) == working_directory_abs
        # Exit if directory is outside of permitted working directory, not a file, or not a python file
        if not is_valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        # Construct list of commands to run
        command = ["python", target_file_path]
        if args:
            command.extend(args)
        # Run command as a subprocess
        process = subprocess.run(command, cwd=working_directory_abs, capture_output=True, text=True,  timeout=30)
        output = []
        # Generate output string
        if process.returncode != 0:
            output.append(f"Process exited with code {process.returncode}")
        if process.stdout:
            output.append(f"STDOUT: {process.stdout}")
        if process.stderr:
            output.append(f"STDERR: {process.stderr}")
        if not process.stdout and not process.stderr:
            output.append("No output produced")
        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"