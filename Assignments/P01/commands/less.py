import os

def less(file, fileContent=False):
    """ 
    This command used to open and backward/forward movement of files.
    Press Enter to continue, 'q' to quit, 'u' to move up, 'd' to move down: 
    """
    try:
        if fileContent:
            lines = file
        else:
            with open(file, 'r') as f:
                lines = f.readlines()
        
        page_size = 10 # Number of lines to display per page
        current_line = 0
        total_lines = len(lines)
        
        while current_line < total_lines:
            #os.system('cls')
            end_line = min(current_line + page_size, total_lines)
            page = lines[current_line:end_line]
            
            for line in page:
                print(line, end='')
            
            user_input = input(
                "Press Enter to continue, 'q' to quit, 'u' to move up, 'd' to move down: "
            ).strip().lower()
            
            if user_input == 'q':
                break
            elif user_input == 'u':
                current_line = max(0, current_line - page_size)
            elif user_input == 'd':
                current_line = min(current_line + page_size, total_lines - 1)
            else:
                current_line = min(current_line + page_size, total_lines)
    except FileNotFoundError:
        print(f"File not found: {file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")