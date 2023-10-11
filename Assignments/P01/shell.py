
import keyboard

import commands


commands_history = []

# define function to parse the input command
def parse_command(tokens):
    input_file = None
    output_file = None
    pipe_to = None

    # Check for input redirection ("<" token)
    if "<" in tokens:
        input_index = tokens.index("<")
        input_file = tokens[input_index + 1]
        tokens = tokens[:input_index]  # Remove input redirection tokens

    # Check for output redirection (">" token)
    if ">" in tokens:
        output_index = tokens.index(">")
        output_file = tokens[output_index + 1]
        tokens = tokens[:output_index]  # Remove output redirection tokens

    # Check for pipes ("|" token)
    if "|" in tokens:
        pipe_index = tokens.index("|")
        pipe_to = tokens[pipe_index + 1:]
        tokens = tokens[:pipe_index]  # Remove pipe tokens

    return  input_file, output_file, pipe_to, tokens

# define function to execute the command
def execute_command(tokens, input_str=None):
    """
    function to execute command
    Args:
    tokens: list of tokens as command
    input_str: input for the command(if given)

    Returns result of executed command as string
    """
    result_str = ""
    if tokens[0] == 'ls':
        if len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.ls.__doc__
        else:
            result_str = commands.ls(tokens)
    elif tokens[0] == 'mkdir':
        if (not input_str) and len(tokens) != 2:
            raise Exception("Directory name not provided")
        elif len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.mkdir.__doc__
        elif input_str and len(tokens) == 1:
            result_str = commands.mkdir(input_str)
        else:
            result_str = commands.mkdir(tokens[1])
    elif tokens[0] == 'cd':
        if (not input_str) and len(tokens) == 1:
            result_str = commands.cd('~')
        elif len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.cd.__doc__
        elif input_str and len(tokens) == 1:
            result_str = commands.cd(input_str)
        else:
            result_str = commands.cd(tokens[1])
    elif tokens[0] == 'pwd':
        if len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.pwd.__doc__
        else:
            result_str = commands.pwd()
    elif tokens[0] == 'cp':
        if len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.cp.__doc__
        elif len(tokens) == 3:
            result_str = commands.cp(tokens[1], tokens[2])
        else:
            raise Exception("Invalid number of arguments for cp.")
    elif tokens[0] == 'mv':
        if len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.mv.__doc__
        elif len(tokens) == 3:
            result_str = commands.mv(tokens[1], tokens[2])
        else:
            raise Exception("Invalid number of arguments for mv.")
    elif tokens[0] == 'rm':
        if len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.rm.__doc__
        elif len(tokens) == 3:
            result_str = commands.rm(tokens[2], tokens[1])
        elif (not input_str) and len(tokens) == 2:
            result_str = commands.rm(tokens[1], None)
        elif input_str and len(tokens) == 1:
            result_str = commands.rm(input_str, None)
        elif input_str and len(tokens) == 2:
            result_str = commands.rm(input_str, tokens[1])
        else:
            raise Exception("Invalid number of arguments for rm.")
    elif tokens[0] == 'rmdir':
        if len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.rmdir.__doc__
        elif len(tokens) == 2:
            result_str = commands.rmdir(tokens[1])
        elif input_str and len(tokens) == 1: 
            result_str = commands.rmdir(input_str)
        else:
            raise Exception("Invalid number of arguments for rmdir.")
    elif tokens[0] == 'cat':
        if len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.cat.__doc__
        elif input_str and len(tokens) == 1:
            result_str = commands.cat(input_str.split())
        else:
            result_str = commands.cat(tokens[1:])
    elif tokens[0] == 'less':
        if len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.less.__doc__
        elif (not input_str) and len(tokens) == 2:
            result_str = commands.less(tokens[1])
        elif input_str and len(tokens) == 1:
            result_str = commands.less(input_str, True)
        elif input_str and len(tokens) == 2:
            result_str = commands.less(input_str, True)
        else:
            raise Exception("Invalid number of arguments for less.")
    elif tokens[0] == 'head':
        if len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.head.__doc__
        elif len(tokens) == 2:
            result_str = commands.head(tokens[1])
        elif (not input_str) and len(tokens) == 4:
            if tokens[2] == "-n":
                result_str = commands.head(tokens[1], int(tokens[3]))
            else:
                raise Exception("Invalid arguments for head.")
        elif input_str:
            if len(tokens) == 1:
                result_str = commands.head(input_str)
            elif len(tokens) == 3 and tokens[1] == '-n':
                result_str = commands.head(input_str, int(tokens[2]))
        else:
            raise Exception("Invalid number of arguments for head.")
    elif tokens[0] == 'tail':
        if len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.tail.__doc__
        elif len(tokens) == 2:
            result_str = commands.tail(tokens[1])
        elif (not input_str) and len(tokens) == 4:
            if tokens[2] == "-n":
                result_str = commands.tail(tokens[1], int(tokens[3]))
            else:
                raise Exception("Invalid arguments for tail.")
        elif input_str:
            if len(tokens) == 1:
                result_str = commands.tail(input_str)
            elif len(tokens) == 3 and tokens[1] == '-n':
                result_str = commands.tail(input_str, int(tokens[2]))
        else:
            raise Exception("Invalid number of arguments for tail.")
    elif tokens[0] == 'grep':
        if len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.grep.__doc__
        elif (not input_str) and tokens[1] == '-l':
            result_str = commands.grep(tokens[2], tokens[3:], True)
        elif (not input_str) and tokens[-1] == '-l':
            result_str = commands.grep(tokens[1], tokens[2:-1], True)
        elif '-l' not in tokens:
            if (not input_str):
                result_str = commands.grep(tokens[1], tokens[2:])
            else:
                result_str = commands.grep(tokens[1], None, False, input_str)
        elif input_str and tokens[1] == '-l':
            result_str = commands.grep(tokens[2], None, True, input_str)
        else:
            raise Exception("Invalid arguments for grep.")
    elif tokens[0] == 'wc':
        if len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.wc.__doc__
        elif any('l' in s for s in tokens[1:]) or any('m' in s for s in tokens[1:]) or any('w' in s for s in tokens[1:]):
            if not input_str:
                result_str = commands.wc(tokens[-1], tokens[1:-1])
            else:
                result_str = commands.wc(None, tokens[1:-1], input_str.splitlines())
        else:
            print(tokens)
            raise Exception("No flag provided for wc.")
    elif tokens[0] == 'chmod':
        if len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.chmod.__doc__
        elif len(tokens) == 3:
            if tokens[1].isdigit():
                result_str = commands.chmod(tokens[2], int(tokens[1]))
            else:
                raise Exception("Invlid arugment for chmod.")
        else:
            raise Exception("Invalid argument for chmod.")
    elif tokens[0] == 'sort':
        if len(tokens) == 2 and tokens[1] == "--help":
            result_str = commands.sort.__doc__
        elif (not input_str) and len(tokens) == 2:
            result_str = commands.sort(tokens[1])
        elif input_str and len(tokens) == 1:
            result_str = commands.sort(None, input_str.splitlines())
        else:
            raise Exception("Invalid argument for sort.")
    elif tokens[0] == 'history':
        result_str = '\n'.join(commands_history)
    else:
        raise Exception("No such Command")
    
    return result_str


def main( input_file, output_file, pipe_to, tokens):
    try:        
        if input_file:
            # read from input file
            with open(input_file, 'r') as inp_f:
                input_str = inp_f.read()
            result_str = execute_command(tokens, input_str) 
        elif pipe_to:
            result_to_pipe = execute_command(tokens)
            result_str = execute_command(pipe_to, result_to_pipe)
        else:
            result_str = execute_command(tokens)

        if output_file:
            # open file and write the output
            with open(output_file, 'w+') as out_f:
                out_f.write(result_str)
        else:
            if  result_str:
                # print to stdout
                if tokens[0] == 'ls':
                    if (len(tokens) == 2 and tokens[1] == "--help") or (any(token.startswith('-') and 'l' in token for token in tokens)):
                        print(result_str)

                    else:
                        my_list = result_str.split("\n")
                        sorted_words = sorted(my_list, key=len)

                        # Number of elements to print per line
                        elements_per_line = 10

                        # Loop through the list and print elements in left-aligned format
                        for i in range(0, len(sorted_words), elements_per_line):
                            # Use string formatting to left-align elements and print 6 elements per line
                            line = ' '.join('{:<10}'.format(item) for item in sorted_words[i:i+elements_per_line])
                            print(line)
                                                    
                        
                else:        
                 print(result_str)

        commands_history.append(' '.join(tokens))

      

    except Exception as e:
        print(f"Error: Invalid Command: {tokens[0]}", e)


if __name__ == '__main__':
    while True:
        result_str = ""
        # Display prompt
        print("% ", end='')

        # Read user input
        user_input = input().strip()

        # Handle exit command
        if user_input == "exit":
            break
        if user_input.strip() == "":
            continue
              

        # Split user input into tokens
        tokens = user_input.split()
        input_file, output_file, pipe_to, tokens = parse_command(tokens)
        
        # handle !x command
        if len(tokens) == 1 and tokens[0][0] == '!' and tokens[0][1:].isdigit():
            if len(commands_history) > 0:
                last_command = commands_history[::-1][min(len(commands_history)-1, int(tokens[0][1:]))]
                keyboard.write(last_command)
            continue
        
   
        else:
            main( input_file, output_file, pipe_to, tokens)
