import os

def cd(directory_path):
    """
    Change the woking directory
    Command: cd [Options]

    Options:
        directory : change to named directory
        ~         : change to home directory
        ..        : change to parent directory
        (no option provided) : change to home direcotry

    """
    try:
        if directory_path == '~':
            directory_path = os.path.expanduser("~")
        os.chdir(directory_path)
        return os.getcwd()
    except FileNotFoundError:
        return f"Directory not found: {directory_path}"
    except PermissionError:
        return f"Permission denied: {directory_path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


