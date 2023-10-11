def cat(files):
    """
    Display a file or multiple files as cancatenated
    Command: cat [file1 file2 ...]
    """
    result_str = ""
    try:
        for file in files:
            with open(file, 'r') as f:
                for line in f:
                    result_str += line
        return result_str   
    except FileNotFoundError as e:
        return f"File not found: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
