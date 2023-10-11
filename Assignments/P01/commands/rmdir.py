import os

def rmdir(directory):
    """
    remove a directory
    Command: rm directory_name 
    """

    try:
        os.rmdir(directory)
        return f"Removed directory: {directory}"
    except FileNotFoundError:
        return f"Directory not found: {directory}"
    except OSError as e:
        return f"Error: {str(e)}"

