import os
import glob

def rm(file, flag):
    """
    remove a file
    Command: rm [Options] file 

    Options:
    -r : recurse into non-empty folder to delete all
    
    Provide filename with wild card character to removes files that match a wildcard
    E.g. fil*e or *file or file*
    """
    result_str = ""

    recursive = False
    force = False

    if flag == '-rf':
        recursive = True
        force = True
    elif flag == '-r':
        recursive = True
    elif flag == '-f':
        flag = True

    try:
        if recursive:
            # Use glob to recursively match files and directories
            entries = glob.glob(file, recursive=True)
        else:
            # Use glob to match files and directories
            entries = glob.glob(file)
        
        if not entries:
            return f"No matching files or directories found for file: {file}"
        for entry in entries:
            if os.path.isfile(entry):
                os.remove(entry)
                result_str += f"Removed file: {entry}\n"
            elif os.path.isdir(entry):
                if recursive:
                    # Remove directory and its contents recursively
                    for root, dirs, files in os.walk(entry, topdown=False):
                        for file in files:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            result_str += f"Removed file: {file_path}\n"
                        for dir_name in dirs:
                            dir_path = os.path.join(root, dir_name)
                            os.rmdir(dir_path)
                            result_str += f"Removed directory: {dir_path}\n"

                    os.rmdir(entry)
                    result_str += f"Removed directory: {entry}\n"
                else:
                    result_str += f"Skipped non-empty directory: {entry}\n"

        return result_str[:-1]
    except Exception as e:
        return f"An error occurred: {str(e)}"

