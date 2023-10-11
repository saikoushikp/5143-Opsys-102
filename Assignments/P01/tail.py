def tail(file, n=10):
    """
    Display last few lines of a file
    Command: tail filename [Options]

    Options:
    -n : specify how many lines to display
    """
    try:
        with open(file, 'r') as file:
            lines = file.readlines()
            if n > len(lines):
                n = len(lines)
            
        return ''.join(lines[-n:])
    
    except FileNotFoundError:
        return f"File not found: {file}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
