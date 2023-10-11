import os
import humanize
import re
try:
    import pwd
    import grp
except ImportError:
    import win32api
    import win32security
import stat

def get_permissions(file_path):
    mode = os.stat(file_path).st_mode
    permissions = ''
    permissions += 'd' if stat.S_ISDIR(mode) else '-'
    permissions += 'r' if mode & stat.S_IRUSR else '-'
    permissions += 'w' if mode & stat.S_IWUSR else '-'
    permissions += 'x' if mode & stat.S_IXUSR else '-'
    permissions += 'r' if mode & stat.S_IRGRP else '-'
    permissions += 'w' if mode & stat.S_IWGRP else '-'
    permissions += 'x' if mode & stat.S_IXGRP else '-'
    permissions += 'r' if mode & stat.S_IROTH else '-'
    permissions += 'w' if mode & stat.S_IWOTH else '-'
    permissions += 'x' if mode & stat.S_IXOTH else '-'
    return permissions
	#return permission_string

def ls(tokens):
    """
    List files and directories with specified options.
    Command: ls [Options]

    Options:
        -a	list all hidden files
        -l	long listing
        -h	human readable sizes
    """
    l = False
    a = False
    h = False

    result_str = ""
    #print(tokens)
    # extract parameters
    if len(tokens) > 1:
        for param in tokens[1:]:
            if re.match(r'^-.*l', param):
                l = True
            if re.match(r'^-.*a', param):
                a = True
            if re.match(r'^-.*h', param):
                h = True

    if not (l or a or h) and len(tokens) > 1:
        path = tokens[-1]
    elif len(tokens) > 2:
        path = tokens[-1]
    else:
        path=  os.getcwd()  
    with os.scandir(path) as entries:
        for entry in entries:
            
            if not a and entry.name.startswith('.') and entry.name != '.':
                continue
            if l:
                file_info = ""
                if entry.is_file():
                    file_info += "-"
                elif entry.is_dir():
                    file_info += "d"
                file_info += " "
                file_info += get_permissions(os.path.join(os.getcwd(), entry))
                
                if 'pwd' in globals():
                    file_info += f" {pwd.getpwuid(entry.stat().st_uid).pw_name}"
                    file_info += f" {grp.getgrgid(entry.stat().st_gid).gr_name}"
                else:
                    owner_sid = win32security.GetFileSecurity(entry.path, win32security.OWNER_SECURITY_INFORMATION).GetSecurityDescriptorOwner()
                    group_sid = win32security.GetFileSecurity(entry.path, win32security.GROUP_SECURITY_INFORMATION).GetSecurityDescriptorGroup()
                    owner_name, _, _ = win32security.LookupAccountSid(None, owner_sid)
                    group_name, _, _ = win32security.LookupAccountSid(None, group_sid)
                    file_info += f" {owner_name}"
                    file_info += f" {group_name}"
                if h:
                    file_info += f" {humanize.naturalsize(entry.stat().st_size)}"
                else:
                    file_info += f" {entry.stat().st_size} "
                file_info += f" {entry.name}"
                result_str += file_info + '\n'
            else:
                result_str += entry.name + '\n'
    return result_str[:-1]
