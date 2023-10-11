def head(file, n=10):
    """
    Display first few lines of a file
    Command: head filename [Options]

    Options:
    -n : specify how many lines to display
    """
    try:
        with open(file, 'r') as file:
            lines = file.readlines()
        
        return ''.join(lines[:n])
    
    except FileNotFoundError:
        return f"File not found: {file}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
