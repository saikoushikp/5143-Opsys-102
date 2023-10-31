# Filesystem Starter Class

from sqliteCRUD import SQLiteCrud
from prettytable import PrettyTable
import humanize
import datetime
import sqlite3 as Sqlite3

class FileSystem:
    def __init__(self,db_name=None):
        if not db_name:
            self.db_name = "filesystem.sqlite"
        else:
            self.db_name = db_name
        self.crud = SQLiteCrud(self.db_name)
        self.cwd = "/"
        self.cwdid = 0

        self.table_name = "files_data"
        # columns = ["id INTEGER PRIMARY KEY", "pid INTEGER NOT NULL", "name TEXT NOT NULL", "created_date TEXT NOT NULL", "modified_date TEXT NOT NULL", "size REAL NOT NULL","type TEXT NOT NULL","owner TEXT NOT NULL","groop TEXT NOT NULL","permissions TEXT NOT NULL", "content BLOB"]
        # test_data = [
        # (1, 0, 'Folder1', '2023-09-25 10:00:00', '2023-09-25 10:00:00', 0.0, 'folder', 'user1', 'group1', 'rwxr-xr-x', None),
        # (2, 1, '.File1.txt', '2023-09-25 10:15:00', '2023-09-25 10:15:00', 1024.5, 'file', 'user1', 'group1', 'rw-r--r--', b"This is a test file") ,
        # (3, 1, 'File2.txt', '2023-09-25 10:30:00', '2023-09-25 10:30:00', 512.0, 'file', 'user2', 'group2', 'rw-rw-r--', b"This is a test file"),
        # (4, 0, 'Folder2', '2023-09-25 11:00:00', '2023-09-25 11:00:00', 0.0, 'folder', 'user2', 'group2', 'rwxr-xr--', None),
        # (5, 4, 'File3.txt', '2023-09-25 11:15:00', '2023-09-25 11:15:00', 2048.75, 'file', 'user3', 'group3', 'rw-r--r--', b"This is a test file"),
        # (6, 4, 'File4.txt', '2023-09-25 11:30:00', '2023-09-25 11:30:00', 4096.0, 'file', 'user3', 'group3', 'rw-r--r--', b"This is a test file"),
        # (7, 0, 'Folder3', '2023-09-25 12:00:00', '2023-09-25 12:00:00', 0.0, 'folder', 'user4', 'group4', 'rwxr-x---', None),
        # (8, 7, 'File5.txt', '2023-09-25 12:15:00', '2023-09-25 12:15:00', 8192.0, 'file', 'user4', 'group4', 'rw-------', b"This is a test file"),
        # (9, 0, 'Folder4', '2023-09-25 13:00:00', '2023-09-25 13:00:00', 0.0, 'folder', 'user5', 'group5', 'rwxr-xr-x', None),
        # (10, 9, 'File6.txt', '2023-09-25 13:15:00', '2023-09-25 13:15:00', 3072.25, 'file', 'user5', 'group5', 'rwxr-xr--', b"This is a test file"),
        # ]

        self.command_history = []
        # self.crud.create_table(self.table_name, columns)
        # for row in test_data:
        #     self.crud.insert_data(self.table_name, row)


    def __getLocationId(self,**kwargs):
        """ Find a file id using location

        Args:
            location(str): location of file or folder
        Returns:
            int or None: id of file or folder
        """
        location = kwargs.get('location')
        if not location:
            return None

        if location == '/':
            return 0

        location = location.strip('/')
        search_absolute = False

        if self.cwdid != 0:
            part_id = self.cwdid
            for part in location.split('/'):
                if part == ".":
                    continue
                elif part == '..':
                    query = f"SELECT pid FROM {self.table_name} WHERE id = {part_id}"
                    self.crud.cursor.execute(query)
                    results = self.crud.cursor.fetchone()
                    if results is None:
                        search_absolute = True
                        break
                    else:
                        part_id = results[0]
                else:
                    query = f"SELECT id FROM {self.table_name} WHERE pid = {part_id} AND name = '{part}'"
                    self.crud.cursor.execute(query)
                    results = self.crud.cursor.fetchone()
                    if results is None:
                        search_absolute = True
                        break
                    else:
                        part_id = results[0]
        else:
            search_absolute = True

        if search_absolute:
            part_id = 0
            for part in location.split('/'):
                if part == ".":
                    continue
                elif part == '..':
                    results = self.crud.read_columns(self.table_name, ["pid"], id=part_id)
                    if results is None:
                        return None
                    part_id = results[0]
                else:
                    query = f"SELECT id FROM {self.table_name} WHERE pid = {part_id} AND name = '{part}'"
                    self.crud.cursor.execute(query)
                    results = self.crud.cursor.fetchone()
                    if results is None:
                        return None
                    else:
                        part_id = results[0]
        return part_id
    
    def list(self,**kwargs):
        """ List the files and folders in current directory
        """
        path = kwargs.get('path')
        if not path:
            path = '.'
        l = kwargs.get('l')
        a = kwargs.get('a')
        h = kwargs.get('h')
        
        path_id = self.__getLocationId(location=path)
        if path_id is None:
            print("Given path does not exist")
            return None
        if l:
            columns = ["name", "permissions", "type", "size", "created_date", "modified_date", "owner", "groop"]
        else:
            columns = ["name", "created_date", "type", "size"]
        
        results = self.crud.read_columns(self.table_name, columns, pid=path_id)
        if not results:
            return None
            return "No files found"
        data = [columns]
        for row in results:
            row = list(row)
            if row[2] == 'folder':
                row[3] = '[Dir]'
            data.append(row)
        if not a:
            data = [row for row in data if not row[0].startswith('.')]
        if h:
            for row in data:
                if row[2] == "file":
                    row[3] = humanize.naturalsize(row[3])
        else:
            for row in data:
                if row[2] == "file":
                    row[3] = f"{row[3]:.2f} Bytes"
        return data

    def __convert_permission(self, triple):
        """
        Convert a triple of numbers (e.g., 644) into the 'rwx' equivalent (e.g., 'rw-r--r--').
        
        Args:
            triple (int): A triple of numbers representing permissions (e.g., 644).

        Returns:
            str: The 'rwx' equivalent representation (e.g., 'rw-r--r--').
        """
        if triple < 0 or triple > 777:
            raise ValueError("Invalid permission triple. Must be between 0 and 777.")

        # Convert each digit of the triple to its 'rwx' equivalent
        owner = self.__convert_digit(triple // 100)
        group = self.__convert_digit((triple // 10) % 10)
        others = self.__convert_digit(triple % 10)

        return owner + group + others

    def __convert_digit(self, digit):
        """
        Convert a single digit (0-7) into its 'rwx' equivalent.

        Args:
            digit (int): A single digit (0-7).

        Returns:
            str: The 'rwx' equivalent representation.
        """
        if digit < 0 or digit > 7:
            raise ValueError("Invalid digit. Must be between 0 and 7.")

        permission_map = {
            0: '---',
            1: '--x',
            2: '-w-',
            3: '-wx',
            4: 'r--',
            5: 'r-x',
            6: 'rw-',
            7: 'rwx',
        }

        return permission_map[digit]

    def chmod(self,**kwargs):
        """ Change the permissions of a file
            1) will need the file / folder id
            2) select permissions from the table where that id exists
        Params:
            location (string) :  location of file or folder
            permission (string) : +x -x 777 644

            if its a triple just overwrite or update table 

        Example:
            +x 
            p = 'rw-r-----'
            p[2] = x
            p[5] = x
            p[8] = x
        """
        try:
            location = kwargs.get('location')
            permission = kwargs.get('permission')
            if not (location and permission):
                print("Location and permission are required")
                return None
            location_id = self.__getLocationId(location=location)
            if location_id is None:
                print("Given location does not exist")
                return None
            
            if permission.isdigit():
                new_permission = self.__convert_permission(int(permission))
            else:
                # get curret permission
                query = f"SELECT permissions FROM {self.table_name} WHERE id = {location_id}"
                self.crud.cursor.execute(query)
                results = self.crud.cursor.fetchone()
                if results is None:
                    print("Given location does not exist")
                    return None
                current_permissions = results[0]
                
                if permission == "+r":
                    new_permission = 'r' + current_permissions[1:3] + 'r' + current_permissions[4:6] + 'r' + current_permissions[7:]
                elif permission == "-r":
                    new_permission = '-' + current_permissions[1:3] + '-' + current_permissions[4:6] + '-' + current_permissions[7:]
                elif permission == "+w":
                    new_permission = current_permissions[:1] + 'w' + current_permissions[2:4] + 'w' + current_permissions[5:7] + 'w' + current_permissions[8:]
                elif permission == "-w":
                    new_permission = current_permissions[:1] + '-' + current_permissions[2:4] + '-' + current_permissions[5:7] + '-' + current_permissions[8:]
                elif permission == "+x":
                    new_permission = current_permissions[:2] + "x" + current_permissions[3:5] + "x" + current_permissions[6:8] + "x"
                elif permission == "-x":
                    new_permission = current_permissions[:2] + "-" + current_permissions[3:5] + "-" + current_permissions[6:8] + "-"
                else:
                    return None
            self.crud.update_data(self.table_name, 'permissions', new_permission, 'id', location_id)
            self.crud.conn.commit()
            return "permissions updated"
        except Exception as e:
            print(f"Error chmod: {e}")
            return None

    def cd(self,**kwargs):
        """
        cd .. = move to parent directory from cwd
        cd ../.. 
        cd /root  (need to find id of that folder, and set swd )
        cd homework/english (involves a check to make sure folder exist)
        """
        location = kwargs.get('location')
        if not location:
            print('Location is required')
            return None
        
        location_id = self.__getLocationId(location=location)
        if location_id is None:
            print("Given location does not exist")
            return None

        query = f"SELECT type FROM {self.table_name} WHERE id = {location_id}"
        self.crud.cursor.execute(query)
        result = self.crud.cursor.fetchone()
              
        if result is None:
            print("Given location does not exist")
            return None
        result = result[0]
        if result != 'folder':
            print("Given location is not a folder")
            return None

        if location_id is None:
            print("Given location does not exist")
            return None

        if location.startswith('/') or location.startswith('..') or location.startswith('.'):
            new_cwd = self.cwd
        else:
            new_cwd = ''
        for part in location.split('/'):
            if part:
                if part == ".":
                    continue
                elif part == "..":
                    new_cwd = "/".join(new_cwd.split('/')[:-1])
                else:
                    new_cwd += "/" + part
        
        self.cwdid = location_id
        self.cwd = new_cwd
        if self.cwdid == 0:
            self.cwd = "/"
        return self.cwd

    def mv(self,**kwargs):
        """ Move a file or folder to a new location
        Params:
            location (string) :  location of file or folder
            new_location (string) : location of file or folder
        """
        try:
            source = kwargs.get('source', None)
            destination = kwargs.get('destination', None)

            if source and destination:
                source_id = self.__getLocationId(location=source)
                if not source_id:
                    return f"mv: cannot reach '{source}': No such file or directory"
                destination_id = self.__getLocationId(location=destination)
                if not destination_id:
                    return f"mv: cannot reach '{destination}': No such file or directory"
                
                query = f"UPDATE files_data SET pid = {destination_id} WHERE id = {source_id};"
                self.crud.cursor.execute(query)
                self.crud.conn.commit()
                return f"Moved '{source}' to '{destination}'"
            else:
                return "mv: missing arguments"
            
        except Exception as e:
            print(f"Error mv: {e}")
            return None

    def cp(self, **kwargs):
        """ Copy a file or folder to a new location
        Params:
            location (string) :  location of file or folder
            new_location (string) : location of file or folder
        """
        try:
            source = kwargs.get('source', None)
            destination = kwargs.get('destination', None)
            if not (source and destination):
                return "cp: missing arguments"
            
            destination_id = None
            file_name = None
            destination_id = self.__getLocationId(location=destination)
            while not destination_id:
                file_name = destination.split('/')[-1]
                destination = "/".join(destination.split('/')[:-1])
                destination_id = self.__getLocationId(location=destination)
                if len(destination.split('/')) == 1:
                    break
            
            if not destination_id:
                return f"cp: cannot reach '{destination}': No such file or directory"

            query = f"SELECT type FROM files_data WHERE id = {destination_id};"
            self.crud.cursor.execute(query)
            result = self.crud.cursor.fetchone()
            if result[0] == "file":
                return "cp: cannot overwrite non-directory with directory"
            
            source_id = self.__getLocationId(location=source)
            if not source_id:
                return f"cp: cannot reach '{source}': No such file or directory"
            

            query = f"SELECT * FROM files_data WHERE id = {source_id};"
            self.crud.cursor.execute(query)
            result = self.crud.cursor.fetchone()

            result = list(result)
            result[0] = None
            result[1] = destination_id
            if file_name:
                result[2] = file_name
            result[4] = str(datetime.datetime.now())
            self.crud.insert_data(self.table_name, result)

            query = f"SELECT id, name FROM files_data WHERE pid = {destination_id} AND name = '{result[2]}';"
            self.crud.cursor.execute(query)
            res = self.crud.cursor.fetchone()
            if not res:
                return "cp: error copying file"

            copied_id, copied_name = res[0], res[1]

            if result[6] == 'folder':
                query = f"SELECT * FROM files_data WHERE pid = {source_id};"
                self.crud.cursor.execute(query)
                results = self.crud.cursor.fetchall()
                for row in results:
                    if row[6] == 'folder':
                        self.cp(source=f"{source}/{row[2]}", destination=f"{destination}/{copied_name}")
                    else:
                        row = list(row)
                        row[0] = None
                        row[1] = copied_id
                        if file_name:
                            row[2] = file_name
                        row[4] = str(datetime.datetime.now())
                        self.crud.insert_data(self.table_name, row)

            return "cp: file copied"
        except Exception as e:
            print(f"Error cp: {e}")
            return None


    def mkdir(self, **kwargs):
        """ Create a new folder
        
        Params:
            name (string) : name of new folder
        """
        try:
            name = kwargs.get('name')
            if not name:
                return "mkdir: missing arguments"
            
            data = [None, self.cwdid, name, str(datetime.datetime.now()), str(datetime.datetime.now()), 0.0, 'folder', 'user1', 'group1', 'rw-r--r--', None]
            self.crud.insert_data(self.table_name, data)
            return "mkdir: folder created"
        except Exception as e:
            print(f"Error mkdir: {e}")
            return None

    def pwd(self):
        return self.cwd

    def delete_file_folder(self, directory_id):
        # print(directory_id, type(directory_id))
        self.crud.cursor.execute(f"SELECT id, type FROM {self.table_name} WHERE id = {directory_id}")
        result = self.crud.cursor.fetchone()
        if result is None:
            return None
        
        location_type = result[1]

        if location_type == 'folder':
            self.crud.cursor.execute(f"SELECT id, type FROM {self.table_name} WHERE pid = {directory_id}")
            contents = self.crud.cursor.fetchall()

            for content_id, content_type in contents:
                if content_type == 'file':
                    self.crud.delete_data(self.table_name, 'id', content_id)
                elif content_type == 'folder':
                    self.delete_file_folder(content_id)

            self.crud.delete_data(self.table_name, 'id', directory_id)
        else:
            self.crud.delete_data(self.table_name, 'id', directory_id)
    
    def rm(self, **kwargs):
        """ Remove a file or folder
        
        Params:
            location (string) : location of file or folder
        """
        try:
            location = kwargs.get('location')
            if not location:
                return "rm: missing arguments"
            
            location_id = self.__getLocationId(location=location)
            if not location_id:
                return f"rm: cannot reach '{location}': No such file or directory"
            self.delete_file_folder(location_id)
            return "rm: file removed"
        except Exception as e:
            print(f"Error rm: {e}")
            return None
        
    def create_file(self, **kwargs):
        """ Create a new file

        Params:
            name (string) : name of new file
            content (string) : content of the file
        """
        try:
            name = kwargs.get('name')
            content = kwargs.get('content')
            if not (name and content):
                return "create_file: missing arguments"
            
            data = [None, self.cwdid, name, str(datetime.datetime.now()), str(datetime.datetime.now()), len(content.encode('utf-8')), 'file', 'user1', 'group1', 'rw-r--r--', Sqlite3.Binary(content.encode('utf-8'))]

            self.crud.insert_data(self.table_name, data)
            return "file created successfully"

        except Exception as e:
            print(f"Error touch: {e}")
            return None


    def cat(self, **kwargs):
        """ Display the contents of a file
        
        Params:
            location (string) : location of file
        """

        try:
            location = kwargs.get('location')
            if not location:
                return "cat: missing arguments"
            
            location_id = self.__getLocationId(location=location)
            if not location_id:
                return f"cat: cannot reach '{location}': No such file or directory"
            query = f"SELECT content, type FROM {self.table_name} WHERE id = {location_id}"
            self.crud.cursor.execute(query)
            result = self.crud.cursor.fetchone()
            if result is None:
                return f"cat: cannot reach '{location}': No such file or directory"
            if result[1] == 'folder':
                return f"cat: cannot reach '{location}': Is a directory"
            return result[0].decode('utf-8')
        except Exception as e:
            print(f"Error cat: {e}")
            return None
        
    def storefile(self, **kwargs):
        """ Store a file in the database
        Params:
            location (string) : location of file on the system
        """
        try:
            filepath = kwargs.get('location')
            if not filepath:
                return "storefile: missing arguments"
            content = None
            # open file in binary read mode
            with open(filepath, 'rb') as file:
                content = file.read()
                

            data = [None, self.cwdid, filepath.split('/')[-1], str(datetime.datetime.now()), str(datetime.datetime.now()), len(content), 'file', 'user1', 'group1', 'rw-r--r--', content]

            self.crud.insert_data(self.table_name, data)
            return "file created successfully"


        except Exception as e:
            print(f"Error storefile: {e}")
            return None
        
    def close(self):
        self.crud.commit()
