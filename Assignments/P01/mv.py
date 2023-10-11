
import os
import shutil

def mv(source, destination):
    """
    move a file from one locatio to another
    Command: mv source_file moved_file
    """
    try:
        # If the source is a directory, use shutil.move to move the entire directory
        if os.path.isdir(source):
            shutil.move(source, destination)
            print(f"Moved directory '{source}' to '{destination}'")
        else:
            # If the source is a file, use shutil.move to move the file
            shutil.move(source, destination)
            print(f"Moved file '{source}' to '{destination}'")
    except Exception as e:
        print(f"Error: {e}")
