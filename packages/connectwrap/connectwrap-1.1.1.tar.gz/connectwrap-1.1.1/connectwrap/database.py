#!/usr/bin/env python3

import sqlite3, os
from connectwrap import utils

class db:

    # Constructor
    def __init__(self, db_filepath):
        if (type(db_filepath) is not str):
            raise TypeError("The path to the db_filepath isn't a string!")

        if (os.path.exists(db_filepath) == False):
            raise FileNotFoundError("The file that the db_filepath argument represents doesn't exist!")

        if (os.path.isfile(db_filepath) == False):
            raise ValueError("The db_filepath argument isn't a file!")

        if (utils.isdb(db_filepath) == False):
            raise ValueError("The db_filepath argument doesn't have the correct extension! Use .db, .sqlite, or .sqlite3!")

        self.db_filepath = str(db_filepath)
        self.connection = sqlite3.connect(self.db_filepath)
        self.connection_cursor = self.connection.cursor()
        self.connection_status = bool(True)

    # Custom exception to raise when the Database is open.
    class DatabaseOpenError(Exception):
        pass

    # Custom exception to raise when the Database is not open.
    class DatabaseNotOpenError(Exception):
        pass

    # Custom exception to raise when an argument table doesn't exist in a database. 
    class TableNotFoundError(Exception):
        pass

    # Custom exception to raise when an argument table already exists in a database. 
    class TableExistsError(Exception):
        pass

    # Execute a custom query.
    def execute(self, query):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(query) is not str):
            raise TypeError("The query argument isn't a string!")

        return self.connection_cursor.execute(query)

    # Commit a query held in the connection cursor. 
    def commit(self):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        self.connection.commit()

    # Close database connection.
    def close_db(self):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        self.connection.close()
        self.connection_status = bool(False)

    # Open database connection. Reset the cursor. 
    def open_db(self):
        if (self.connection_status != False):
            raise db.DatabaseOpenError("Database is not closed! The connection status attribute is not set to False!")

        self.connection = sqlite3.connect(self.db_filepath)
        self.connection_cursor = self.connection.cursor()
        self.connection_status = bool(True)

    # Change the db_filepath attribute value. 
    def set_db_filepath(self, db_filepath):
        if (type(db_filepath) is not str):
            raise TypeError("The path to the db_filepath isn't a string!")

        if (os.path.exists(db_filepath) == False):
            raise FileNotFoundError("The file that the db_filepath argument represents doesn't exist!")

        if (os.path.isfile(db_filepath) == False):
            raise ValueError("The db_filepath argument isn't a file!")

        if (utils.isdb(db_filepath) == False):
            raise ValueError("The db_filepath argument doesn't have the correct extension! Use .db, .sqlite, or .sqlite3!")
        
        if (self.connection_status == True): 
            db.close_db(self)
            self.db_filepath = str(db_filepath)
            db.open_db(self)
        else: 
            self.db_filepath = str(db_filepath)
            db.open_db(self)

    # Return the connection_status attribute representing whether the Database connection is open or closed. 
    # Opened = True; Closed = False
    def get_connection_status(self):
        return self.connection_status

    # Return the db_filepath attribute value representing the database file path.
    def get_db_filepath(self):
        return self.db_filepath

    # Select and return the table names within a database as strings in a list. 
    def get_tablenames(self):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        table_names = list([])
        query = "SELECT name FROM sqlite_master WHERE type='table'"

        for name in db.execute(self, query):
            name = str(name).strip("(,')")
            table_names.append(name)

        return table_names

    # Select and return the key names within a table as strings in a list. 
    def get_keys(self, db_table):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(db_table) is not str):
            raise TypeError("The db_table argument isn't a string!")

        if (db.table_exists(self, db_table) == False):
            raise db.TableNotFoundError("The table doesn't exist!") 
        
        connection = sqlite3.connect(self.db_filepath)
        connection.row_factory = sqlite3.Row
        connection_cursor = connection.cursor()
        query = str("SELECT * FROM {0}").format(db_table)
        connection_cursor.execute(query)
        row = connection_cursor.fetchone()
        connection.close()
        return list(row.keys())

    # Select and return a list of the values in a column of a table based on the key from that column.
    def get_column(self, db_table, key):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(db_table) is not str):
            raise TypeError("The db_table argument isn't a string!")

        if (type(key) is not str):
            raise TypeError("The key argument isn't a string!")

        if (db.table_exists(self, db_table) == False):
            raise db.TableNotFoundError("The table doesn't exist!")

        if (db.key_exists(self, db_table, key) == False):
            raise KeyError("The key argument doesn't exist within the table!")

        column_values = list([])
        query = str("SELECT {0} FROM {1}").format(key, db_table)

        for column in db.execute(self, query):
            column = str(column).strip("(,')")

            if (column.isdigit() == True):
                column = int(column)
            elif (utils.isfloat(column) == True):
                column = float(column)
            elif (utils.ishex(column) == True):
                column = bytes.fromhex(column)
            elif (column == "None"):
                column = None
            else:
                column = str(column)
                
            column_values.append(column)
            
        return column_values

    # Select and return a dictionary representing a row in the database table where the key and value arguments match a row column key and value pair. 
    # Only returns the first row with the occurance of the key/value argument pair.
    # Returns None if there's no occurance of the key/value argument in any row in the table.
    # The key argument must be a string and a key within the table. 
    # The value argument must be one of the following types - int, float, str, bytes, None.
    # Use a key with a unique value for best results.   
    def get_row(self, db_table, key, value):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(db_table) is not str):
            raise TypeError("The db_table argument isn't a string!")

        if (type(key) is not str):
            raise TypeError("The key argument isn't a string!")

        if (type(value) is not int and type(value) is not float and type(value) is not str and type(value) is not bytes and value != None):
            raise TypeError("The value argument must be one of the following types - int, float, str, bytes, None")

        if (db.table_exists(self, db_table) == False):
            raise db.TableNotFoundError("The table doesn't exist!")

        if (db.key_exists(self, db_table, key) == False):
            raise KeyError("The key argument doesn't exist within the table!")

        table = list(db.get_table(self, db_table))
        i = int(0)

        while(i <  len(table)):
            row = dict(table[i])
                
            for row_key in row:
                if (key == row_key and value == row[row_key]):
                    return row
                
            i += 1
            
        return None

    # Select and return a list of dictionaries with each dictionary representing a row in a table.
    def get_table(self, db_table):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(db_table) is not str):
            raise TypeError("The db_table argument isn't a string!")

        if (db.table_exists(self, db_table) == False):
            raise db.TableNotFoundError("The table doesn't exist!")

        table = list([])
        keys = list(db.get_keys(self, db_table))
        query = str("SELECT * FROM {0}").format(db_table)

        for row in db.execute(self, query):
            row_dict = dict.fromkeys(keys)
            row_factor = list([])
            i = int(0)

            for column in row:
                column = str(column).strip("(,')") 
                            
                if (column.isdigit() == True):
                    column = int(column)
                elif (utils.isfloat(column) == True):
                    column = float(column)   
                elif (utils.ishex(column) == True):
                    column = bytes.fromhex(column)    
                elif (column == "None"):
                    column = None
                else:
                    column = str(column)
                
                row_factor.append(column)

            for key in row_dict:
                row_dict[key] = row_factor[i]
                i += 1
                
            table.append(row_dict)

        return table 

    # Rename a table. 
    def rename_table(self, old_table_name, new_table_name):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(old_table_name) is not str):
            raise TypeError("The old_table_name argument isn't a string!")

        if (type(new_table_name) is not str):
            raise TypeError("The new_table_name argument isn't a string!")

        if (db.table_exists(self, old_table_name) == False):
            raise db.TableNotFoundError("The old_table_name argument table doesn't exist!")

        if (db.table_exists(self, new_table_name) == True):
            raise db.TableExistsError("The new_table_name argument table already exists!")

        query = str("ALTER TABLE {0} RENAME TO {1}").format(old_table_name, new_table_name)
        db.execute(self, query)
        db.commit(self)
    
    # Drop/delete table in the file database. 
    def drop_table(self, db_table):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(db_table) is not str):
            raise TypeError("The db_table argument isn't a string!")

        if (db.table_exists(self, db_table) == False):
            raise db.TableNotFoundError("The table doesn't exist!")
        
        query = str("DROP TABLE {0}").format(db_table)
        db.execute(self, query)
        db.commit(self)

    # Drop/delete rows within a table with matching key & value. 
    # The key argument must be a string and a key within the table. 
    # The value argument must be one of the following types - int, float, str, bytes, None.
    def drop_row(self, db_table, key, value):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(db_table) is not str):
            raise TypeError("The db_table argument isn't a string!")

        if (type(key) is not str):
            raise TypeError("The key argument isn't a string!")

        if (type(value) is not int and type(value) is not float and type(value) is not str and type(value) is not bytes and value != None):
            raise TypeError("The value argument must be one of the following types - int, float, str, bytes, None")

        if (db.table_exists(self, db_table) == False):
            raise db.TableNotFoundError("The table doesn't exist!")

        if (db.key_exists(self, db_table, key) == False):
            raise KeyError("The key argument doesn't exist within the table!")

        if (type(value) is str):
            query = str("DELETE FROM {0} WHERE {1}='{2}'")
        elif (type(value) is bytes):
            value = str(value.hex())
            query = str("DELETE FROM {0} WHERE {1}='{2}'")
        elif (value == None):
            value = str("None")
            query = str("DELETE FROM {0} WHERE {1}='{2}'")
        else: 
            query = str("DELETE FROM {0} WHERE {1}={2}")

        query = query.format(db_table, key, value)
        db.execute(self, query)
        db.commit(self)

    # Create table within the file database.
    # The key in each kwargs entry denotes the key name of a column. 
    # The value in each kwargs entry denotes the data type of a column. 
    # The value in each kwargs entry must be one of the following strings - 'int', 'float', 'str', 'bytes', 'None'.     
    def create_table(self, db_table, **kwargs):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(db_table) is not str):
            raise TypeError("The db_table argument isn't a string!")

        if (db.table_exists(self, db_table) == True):
            raise db.TableExistsError("The table already exists!")

        query = str("CREATE TABLE {0} ({1})")
        record = str("")
        count = int(0)
    
        for kwarg in kwargs:
            if (type(kwargs[kwarg]) is not str):
                raise TypeError("The value in kwargs must be a string!")

            if (kwargs[kwarg] != "int" and kwargs[kwarg] != "float" and kwargs[kwarg] != "str" and kwargs[kwarg] != "bytes" and kwargs[kwarg] != "None"):
                raise ValueError("The value in kwargs must be one of the following strings - 'int', 'float', 'str', 'bytes', 'None'")

            if (count < len(kwargs) - 1):
                record += (kwarg + " " + kwargs[kwarg] + ",")
            else:
                record += (kwarg + " " + kwargs[kwarg])

            count += 1
        
        query = query.format(db_table, record)  
        db.execute(self, query)
        db.commit(self)

    # Create a new column within a table.
    # The datatype argument must be one of the following strings - 'int', 'float', 'str', 'bytes', 'None'.
    def create_column(self, db_table, column, datatype):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(db_table) is not str):
            raise TypeError("The db_table argument isn't a string!")

        if (type(column) is not str):
            raise TypeError("The column argument isn't a string!")

        if (type(datatype) is not str):
            raise TypeError("The datatype argument isn't a string!")

        if (db.table_exists(self, db_table) == False):
            raise db.TableNotFoundError("The table doesn't exist!")

        if (db.key_exists(self, db_table, column) == True):
            raise KeyError("The column already exists within the table!")

        if (datatype != "int" and datatype != "float" and datatype != "str" and datatype != "bytes" and datatype != "None"):
            raise ValueError("The datatype argument must be one of the following strings - 'int', 'float', 'str', 'bytes', 'None'")

        query = str("ALTER TABLE {0} ADD {1} {2}").format(db_table, column, datatype)
        db.execute(self, query)
        db.commit(self)

    # Select and output to terminal the table names within a database. 
    def select_tablenames(self):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        for name in db.get_tablenames(self):
            print("Table Name:", name)

    # Select and output to terminal the rows from a table.
    def select_table(self, db_table):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(db_table) is not str):
            raise TypeError("The db_table argument isn't a string!")

        if (db.table_exists(self, db_table) == False):
            raise db.TableNotFoundError("The table doesn't exist!")

        for row in db.get_table(self, db_table):
            print(db_table, "Row:", row)
       
    # Select and output to terminal the values from keys within a table. 
    # Each arg in *args arguments must be strings containing key names within the table.
    def select_column(self, db_table, *args):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(db_table) is not str):
            raise TypeError("The db_table argument isn't a string!")

        if (db.table_exists(self, db_table) == False):
            raise db.TableNotFoundError("The table doesn't exist!")

        for arg in args:
            if (type(arg) is not str):
                raise TypeError("An argument in args isn't a string!")

            print(db_table, "Column", arg + ":", db.get_column(self, db_table, arg), sep=" ")
            
    # Select and output to terminal the key names within a table. 
    def select_keys(self, db_table):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(db_table) is not str):
            raise TypeError("The db_table argument isn't a string!")

        if (db.table_exists(self, db_table) == False):
            raise db.TableNotFoundError("The table doesn't exist!")

        print(db_table, "Keys:", db.get_keys(self, db_table))
    
    # Select and output to terminal a row of a table in a database.  
    # Only outputs the first row with the occurance of the key/value argument pair.
    # Outputs None if there's no occurance of the key/value argument in any row in the table.
    # The key argument must be a string and a key within the table. 
    # The value argument must be one of the following types - int, float, str, bytes, None.
    # Use a key with a unique value for best results.   
    def select_row(self, db_table, key, value):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(db_table) is not str):
            raise TypeError("The db_table argument isn't a string!")

        if (type(key) is not str):
            raise TypeError("The key argument isn't a string!")

        if (type(value) is not int and type(value) is not float and type(value) is not str and type(value) is not bytes and value != None):
            raise TypeError("The value argument must be one of the following types - int, float, str, bytes, None")

        if (db.table_exists(self, db_table) == False):
            raise db.TableNotFoundError("The table doesn't exist!")

        if (db.key_exists(self, db_table, key) == False):
            raise KeyError("The key argument doesn't exist within the table!")

        print(db_table, "Row:", db.get_row(self, db_table, key, value))

    # Insert row of data into table.
    # Each arg in *args must be one of the following types - int, float, str, bytes, None.
    def insert_row(self, db_table, *args):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(db_table) is not str):
            raise TypeError("The table name argument isn't a string!")

        if (db.table_exists(self, db_table) == False):
            raise db.TableNotFoundError("The table doesn't exist!")

        query = str("INSERT INTO {0} VALUES ({1})")
        record = str("")
        count = int(0)

        for arg in args:
            if (type(arg) is not int and type(arg) is not float and type(arg) is not str and type(arg) is not bytes and arg != None):
                raise TypeError("The argument must be one of the following types - int, float, str, bytes, None")

            if (count < len(args) - 1):
                if (type(arg) is str):
                    record += "'" + arg + "'" + ","
                elif (type(arg) is bytes):
                    arg = arg.hex()
                    record += "'" + str(arg) + "'" + ","
                elif (arg == None):
                    record += "'None'" + "," 
                else:
                    record += str(arg) + ","
            else: 
                if (type(arg) is str):
                    record += "'" + arg + "'"
                elif (type(arg) is bytes):
                    arg = arg.hex()
                    record += "'" + str(arg) + "'"
                elif (arg == None):
                    record += "'None'"
                else:
                    record += str(arg)

            count += 1

        query = query.format(db_table, record)
        db.execute(self, query)
        db.commit(self)

    # Update/change row column values within a table.
    # The key arguments must be strings and keys within the table. 
    # The value arguments must be one of the following types - int, float, str, bytes, None.
    def update_row(self, db_table, change_key, change_value, check_key, check_value):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(db_table) is not str):
            raise TypeError("The table name argument isn't a string!")
        
        if (type(change_key) is not str):
            raise TypeError("The key argument isn't a string!")

        if (type(check_key) is not str):
            raise TypeError("The key argument isn't a string!")

        if (type(change_value) is not int and type(change_value) is not float and type(change_value) is not str and type(change_value) is not bytes and change_value != None):
            raise TypeError("The change_value argument must be one of the following types - int, float, str, bytes, None")

        if (type(check_value) is not int and type(check_value) is not float and type(check_value) is not str and type(check_value) is not bytes and check_value != None):
            raise TypeError("The check_value argument must be one of the following types - int, float, str, bytes, None")

        if (db.table_exists(self, db_table) == False):
            raise db.TableNotFoundError("The table doesn't exist!")

        if (db.key_exists(self, db_table, change_key) == False):
            raise KeyError("The change_key argument doesn't exist within the table!")

        if (db.key_exists(self, db_table, check_key) == False):
            raise KeyError("The check_key argument doesn't exist within the table!")

        query = str("UPDATE {0} SET {1}={2} WHERE {3}={4}")

        if (change_value == None):
            change_value = str("'None'")
            
        if (check_value == None):
            check_value = str("'None'")

        if (type(change_value) is bytes):
             change_value = str("'" + change_value.hex() + "'").lower()
            
        if (type(check_value) is bytes):
            check_value == str("'" + check_value.hex() + "'").lower()

        if (type(change_value) is str):
            change_value = str("'" + change_value + "'")

        if (type(check_value) is str):
            check_value = str("'" + check_value + "'")

        query = query.format(db_table, change_key, change_value, check_key, check_value)
        db.execute(self, query)
        db.commit(self)

    # Return True if the key argument exists in a table. 
    def key_exists(self, db_table, key):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(db_table) is not str):
            raise TypeError("The db_table argument isn't a string!")

        if (type(key) is not str):
            raise TypeError("The key argument isn't a string!")

        for element in db.get_keys(self, db_table):
            if (key == element):
                return True
        
        return False

    # Return True if the db_table argument is a table name within the database. 
    def table_exists(self, db_table):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")
        
        if (type(db_table) is not str):
            raise TypeError("The db_table argument isn't a string!")

        for name in db.get_tablenames(self):
            if (name == db_table):
                return True
        
        return False