import os
def chmod(file, mode):
    """
    Change modify permission
    Command: chmod xxx file
    """
    try:
        os.chmod(file, int(str(mode),8))
        return f"Changed permissions of {file} to {mode}"
    except FileNotFoundError:
        return f"File not found: {file}"
    except Exception as e:
        return f"An error occurred: {str(e)}"