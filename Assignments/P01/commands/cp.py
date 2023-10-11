
    
import os
import shutil

def cp(source, destination):
    """
        Create copy of a file
        Command: cp source_file copied_file

     """
    try:
        # If the source is a directory, use shutil.copytree to copy the entire directory
        if os.path.isdir(source):
            shutil.copytree(source, destination)
            print(f"Copied directory '{source}' to '{destination}'")
        else:
            # If the source is a file, use shutil.copy2 to copy the file
            shutil.copy2(source, destination)
            print(f"Copied file '{source}' to '{destination}'")
    except Exception as e:
        print(f"Error: {e}")
