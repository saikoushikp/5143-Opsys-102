def sort(file, content=None):
    """
    Display sorted content from a file
    Command: sort filename
    """
    try:
        if not content:
            with open(file, 'r') as file:
                lines = file.readlines()
        else:
            lines = content

        lines.sort()
        
        return '\n'.join(lines)
    except FileNotFoundError:
        return f"File not found: {file}"
    except Exception as e:
        return f"An error occurred: {str(e)}"