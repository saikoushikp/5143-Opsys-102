import re

def grep(keyword, files, return_filename=False, content=None):
    """
    Search a file(s) files for keywords and print lines where pattern is found
    Command: grep [Options] keyword file
    
    Options:
    -l :  only return file names where the word or pattern is found

    """
    result_str = ""
    try:
        matching_files = []
        if content:
            lines = content.split('\n')  # Split the content into lines

            for line_number, line in enumerate(lines, start=1):
                if re.search(keyword, line):
                    if return_filename:
                        result_str += "(Standard input )" + '\n'
                    else:
                        result_str += f" {line}"+ '\n'
        else:
            for file_name in files:
                with open(file_name, 'r') as file:
                    lines = file.readlines()
                    for line_number, line in enumerate(lines, start=1):
                        if re.search(keyword, line):
                            if return_filename:
                                result_str += file_name + '\n'
                            else:
                                result_str += f"{file_name}:{line_number}: {line}"+ '\n'
        
        return result_str[:-1]
    except FileNotFoundError as e:
        print(f"File not found: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


    """
    
    'd r----x--x athulsajikumar staff 64  abc\n- rwxrwxrwx athulsajikumar staff 54  requirements.txt\nd r----x--x athulsajikumar staff 64  athul2\nd rwxr-xr-x athulsajikumar staff 288  cass\nd rwxr-xr-x athulsajikumar staff 96  abcde\nd rwxr-xr-x athulsajikumar staff 96  test1\n- rwxrwxrwx athulsajikumar staff 11777  shell.py\nd rwxr-xr-x athulsajikumar staff 64  cff\n- rw-r--r-- athulsajikumar staff 4839  a.txt\nd rwxr-xr-x athulsajikumar staff 64  abc4\n- rw-r--r-- athulsajikumar staff 4839  d.txt\n- rw-r--r-- athulsajikumar staff 9678  s.txt\n- rw-r--r-- athulsajikumar staff 9678  f.txt\n- rw-r--r-- athulsajikumar staff 9678  g.txt\n- rw---x--x athulsajikumar staff 115  readme.txt\nd rwxrwxrwx athulsajikumar staff 672  commands\nd rwxr-xr-x athulsajikumar staff 64  test2\nd rwxr-xr-x athulsajikumar staff 64  jass\nd rwxr-xr-x athulsajikumar staff 64  athul\nd r----x--x athulsajikumar staff 64  atul'
    """