import time
from rich import print
from rich.table import Table
from rich.box import SIMPLE
from fileSystem import FileSystem
from sqliteCRUD import SQLiteCrud


def display_ls(files):
    if not files:
        return
    table = Table(show_header=True, header_style="bold blue", box=SIMPLE)
    for head in files[0]:
        table.add_column(head)
    data = [[str(item) for item in row] for row in files[1:]]
    for row in data:
        table.add_row(*row)
    print(table)


def display_pwd(directory):
    if directory is None:
        print("[bold red]Invalid Directory[/bold red]")
        return
    print(f"[bold cyan]Current Directory:[/bold cyan] [green]{directory}[/green]")
    print()

def main():
    file_system = FileSystem()
    crud = SQLiteCrud("filesystem.sqlite")
    table_name = "files_data"
    columns = ["id INTEGER PRIMARY KEY", "pid INTEGER NOT NULL", "name TEXT NOT NULL", "created_date TEXT NOT NULL", "modified_date TEXT NOT NULL", "size REAL NOT NULL","type TEXT NOT NULL","owner TEXT NOT NULL","groop TEXT NOT NULL","permissions TEXT NOT NULL", "content BLOB"]
    test_data = [
    (1, 0, 'Folder1', '2023-09-25 10:00:00', '2023-09-25 10:00:00', 0.0, 'folder', 'user1', 'group1', 'rwxr-xr-x', None),
    (2, 1, '.File1.txt', '2023-09-25 10:15:00', '2023-09-25 10:15:00', 1024.5, 'file', 'user1', 'group1', 'rw-r--r--', b"This is a test file") ,
    (3, 1, 'File2.txt', '2023-09-25 10:30:00', '2023-09-25 10:30:00', 512.0, 'file', 'user2', 'group2', 'rw-rw-r--', b"This is a test file"),
    (4, 0, 'Folder2', '2023-09-25 11:00:00', '2023-09-25 11:00:00', 0.0, 'folder', 'user2', 'group2', 'rwxr-xr--', None),
    (5, 4, 'File3.txt', '2023-09-25 11:15:00', '2023-09-25 11:15:00', 2048.75, 'file', 'user3', 'group3', 'rw-r--r--', b"This is a test file"),
    (6, 4, 'File4.txt', '2023-09-25 11:30:00', '2023-09-25 11:30:00', 4096.0, 'file', 'user3', 'group3', 'rw-r--r--', b"This is a test file"),
    (7, 0, 'Folder3', '2023-09-25 12:00:00', '2023-09-25 12:00:00', 0.0, 'folder', 'user4', 'group4', 'rwxr-x---', None),
    (8, 7, 'File5.txt', '2023-09-25 12:15:00', '2023-09-25 12:15:00', 8192.0, 'file', 'user4', 'group4', 'rw-------', b"This is a test file"),
    (9, 0, 'Folder4', '2023-09-25 13:00:00', '2023-09-25 13:00:00', 0.0, 'folder', 'user5', 'group5', 'rwxr-xr-x', None),
    (10, 9, 'File6.txt', '2023-09-25 13:15:00', '2023-09-25 13:15:00', 3072.25, 'file', 'user5', 'group5', 'rwxr-xr--', b"This is a test file"),
    (11, 1, 'Folder6', '2023-09-25 13:15:00', '2023-09-25 13:15:00', 3072.25, 'folder', 'user5', 'group5', 'rwxr-xr--', b"This is a test file"),
    (12, 11, 'file11.txt', '2023-09-25 13:15:00', '2023-09-25 13:15:00', 3072.25, 'file', 'user5', 'group5', 'rwxr-xr--', b"This is a test file"),


    ]
    
    crud.drop_table(table_name)
    crud.create_table(table_name, columns)
    for row in test_data:
     crud.insert_data(table_name, row)
    crud.close_connection()

    print("[bold blue]Command:[/bold blue] [green]ls[/green]")
    data = file_system.list()
    display_ls(data)
    file_system.command_history.append("ls")
    #time.sleep(2)
    promot=input("")
   
    print("[bold blue]Command:[/bold blue] [green]cd Folder1[/green]")
    res = file_system.cd(location="Folder1")
    display_pwd(res)
    file_system.command_history.append("cd Folder1/")
    #time.sleep(2)
    promot=input("")


    print("[bold blue]Command:[/bold blue] [green]ls Folder1 -alh[/green]")
    data = file_system.list(path = "Folder1",a=True,l=True, h=True)
    display_ls(data)
    file_system.command_history.append("ls Folder1 -alh")
    #time.sleep(2)
    promot=input("")



    print("[bold blue]Command:[/bold blue] [green]chmod +w File2.txt[/green]")
    res =  file_system.chmod(location="File2.txt", permission="+w")
    print(res, end="\n\n")
    file_system.command_history.append("chmod +w File2.txt")
   # time.sleep(2)
    promot=input("")
    
    
    
    print("[bold blue]Command:[/bold blue] [green]chmod 000 Folder6[/green]")
    res =  file_system.chmod(location="Folder6", permission="000")
    print(res, end="\n\n")
    file_system.command_history.append("chmod 000 Folder6")
   # time.sleep(2)
    promot=input("")


    print("[bold blue]Command:[/bold blue] [green]ls Folder1 -lh[/green]")
    data = file_system.list(path = "Folder1",l=True, h=True)
    display_ls(data)
    file_system.command_history.append("ls Folder1 -lh")
    #time.sleep(2)
    promot=input("")


    print("[bold blue]Command:[/bold blue] [green]mv Folder2 Folder1[/green]")
    res = file_system.mv(source="Folder2", destination="Folder1")
    print(res, end="\n\n")
    file_system.command_history.append("mv Folder2 Folder1")
    #time.sleep(2)
    promot=input("")


    print("[bold blue]Command:[/bold blue] [green]cp Folder2/File4.txt Folder1/copiedFile.txt[/green]")
    res = file_system.cp(source="Folder2/File4.txt", destination="Folder1/copiedFile.txt")
    print(res, end="\n\n")
    file_system.command_history.append("cp Folder2/File4.txt Folder1/copiedFile.txt")
    promot=input("")
    
    print("[bold blue]Command:[/bold blue] [green]ls[/green]")
    data = file_system.list()
    display_ls(data)
    file_system.command_history.append("ls")
    promot=input("")


    print("[bold blue]Command:[/bold blue] [green]pwd[/green]")
    res = file_system.pwd()
    display_pwd(res)
    file_system.command_history.append("pwd")
    #time.sleep(2)
    promot=input("")


    print("[bold blue]Command:[/bold blue] [green]ls[/green]")
    data = file_system.list()
    display_ls(data)
    file_system.command_history.append("ls")
    #time.sleep(2)
    promot=input("")

    print("[bold blue]Command:[/bold blue] [green]cp Folder4 Folder1[/green]")
    res = file_system.cp(source="Folder4", destination="Folder1")
    print(res, end="\n\n")
    file_system.command_history.append("cp folder4 folder1")
   # time.sleep(2)
    promot=input("")



    print("[bold blue]Command:[/bold blue] [green]ls Folder1 -lh[/green]")
    data = file_system.list(path = "Folder1",l=True, h=True)
    display_ls(data)
    file_system.command_history.append("ls Folder1 -lh")
    #time.sleep(2)
    promot=input("")



    print("[bold blue]Command:[/bold blue] [green]mkdir newFolder[/green]")
    res = file_system.mkdir(name="newFolder")
    print(res, end="\n\n")
    file_system.command_history.append("mkdir newFolder")
    #time.sleep(2)
    promot=input("")
    
    print("[bold blue]Command:[/bold blue] [green]mkdir cass[/green]")
    res = file_system.mkdir(name="cass")
    print(res, end="\n\n")
    file_system.command_history.append("mkdir cass")
    #time.sleep(2)
    promot=input("")
    
    print("[bold blue]Command:[/bold blue] [green]cd cass[/green]")
    res = file_system.cd(location="cass")
    display_pwd(res)
    file_system.command_history.append("cd cass/")
    #time.sleep(2)
    promot=input("")
    
    print("[bold blue]Command:[/bold blue] [green]mkdir folder3[/green]")
    res = file_system.mkdir(name="folder3")
    print(res, end="\n\n")
    file_system.command_history.append("mkdir folder2")
    #time.sleep(2)
    
    promot=input("")
   
    print("[bold blue]Command:[/bold blue] [green]ls[/green]")
    data = file_system.list()
    display_ls(data)
    file_system.command_history.append("ls")
    #time.sleep(2)
    promot=input("")

    print("[bold blue]Command:[/bold blue] [green]cd ..[/green]")
    res = file_system.cd(location="..")
    print(f"[bold cyan]Current Directory:[/bold cyan] [green] /Folder1 \n [/green]")

    #display_pwd(res)
    file_system.command_history.append("cd ..")
    #time.sleep(2)
    promot=input("")
           


    print("[bold blue]Command:[/bold blue] [green]ls[/green]")
    data = file_system.list()
    display_ls(data)
    file_system.command_history.append("ls")
    #time.sleep(2)
    promot=input("")



    print("[bold blue]Command:[/bold blue] [green]rm  newFolder[/green]")
    res = file_system.rm(location="newFolder")
    print(res, end="\n\n")
    
    file_system.command_history.append("rm newFolder")
    #time.sleep(2)
    promot=input("")


    print("[bold blue]Command:[/bold blue] [green]rm  cass[/green]")
    res = file_system.rm(location="cass")
    print(res, end="\n\n")
   
    file_system.command_history.append("rm cass")
    #time.sleep(2)
    promot=input("")


    print("[bold blue]Command:[/bold blue] [green]ls[/green]")
    data = file_system.list()
    display_ls(data)
    file_system.command_history.append("ls")
    #time.sleep(2)
    promot=input("")
  

    print('[bold blue]Command:[/bold blue] [green]"This is test file content" > newFile.txt[/green]')
    res = file_system.create_file(name="newFile.txt", content="This is test file content")
    print(res, end="\n\n")
    file_system.command_history.append('"This is test file content" > newFile.txt')
    #time.sleep(2)
    promot=input("")
    
   

    print("[bold blue]Command:[/bold blue] [green]ls[/green]")
    data = file_system.list()
    display_ls(data)
    file_system.command_history.append("ls")
    #time.sleep(2)
    promot=input("")

    # show file content
    print("[bold blue]Command:[/bold blue] [green]cat newFile.txt[/green]")
    res = file_system.cat(location="newFile.txt")
    print(res, end="\n\n")
    file_system.command_history.append("cat newFile.txt")
    #time.sleep(2)

    promot=input("")
    # store a file data in DB from computer file
    print("[bold blue]Command:[/bold blue] [green]storefile requirements.txt[/green]")
    res = file_system.storefile(location="requirements.txt")
    print(res, end="\n\n")
    file_system.command_history.append("storefile requirements.txt")
    #time.sleep(2)
   
    promot=input("")
    
    

    print("[bold blue]Command:[/bold blue] [green]ls[/green]")
    data = file_system.list()
    display_ls(data)
    file_system.command_history.append("ls")
    #time.sleep(2)
    promot=input("")
    
    
    
    promot=input("")
    
    print("[bold blue]Command:[/bold blue] [green]cat requirements.txt[/green]")
    res = file_system.cat(location="requirements.txt")
    print(res, end="\n\n")
    file_system.command_history.append("cat requirements.txt")
    #time.sleep(2)
    promot=input("")
    
    # history command
    print("[bold blue]Command:[/bold blue] [green]history[/green]")
    print("\n".join(file_system.command_history))
    time.sleep(2)
    
   
     
    file_system.close()
    
main()
