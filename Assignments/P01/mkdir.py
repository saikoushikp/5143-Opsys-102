import os 

def mkdir(directory_name):
    """
        Make a directory in the current working directory
        Command: mkdir directory_name
    """
    try:
        os.mkdir(directory_name)
        return f"Directory '{directory_name}' created successfully."
    except FileExistsError:
        return f"Directory '{directory_name}' already exists."
    except PermissionError:
        return f"Permission denied to create directory '{directory_name}'."
    except Exception as e:
        return f"An error occurred: {str(e)}"