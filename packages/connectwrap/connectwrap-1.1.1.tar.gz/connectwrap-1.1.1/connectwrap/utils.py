#!/usr/bin/env python3

import os

# Drop/delete file database.
def drop_database(db_filepath):
    if (type(db_filepath) is not str):
        raise TypeError("The db_filepath argument isn't a string!")

    if (os.path.exists(db_filepath) == False):
        raise FileNotFoundError("The file that the db_filepath argument represents doesn't exist!")

    if (isdb(db_filepath) == False):
        raise ValueError("The db_filepath argument doesn't have the correct extension! Use .db, .sqlite, or .sqlite3!")
        
    print("Deleting Database:", db_filepath)
    os.remove(db_filepath)
    print("Deletion Success:", db_filepath, "Deleted!")

# Create file database. 
def create_database(db_filepath):
    if (type(db_filepath) is not str):
        raise TypeError("The db_filepath argument isn't a string!")

    if (os.path.exists(db_filepath) == True):
        raise FileExistsError("A file with that name already exists!")
        
    if (isdb(db_filepath) == False):
        raise ValueError("The db_filepath argument doesn't have the correct extension! Use .db, .sqlite, or .sqlite3!")
        
    print("Creating Database:", db_filepath)
    new_db = open(db_filepath, "xb"); new_db.close()
    print("Creation Success:", db_filepath, "Created!")

# Return True if all characters in arg string are hexadecimal.
def ishex(arg):
    if (type(arg) is not str):
        raise TypeError("The arg argument isn't a string!")
        
    hex_digits = str("0123456789abcdef")

    for digit in arg.replace(' ', '').lower():
        if not (digit in hex_digits):
            return False

    return True

# Return True if arg string characters constitute a float. 
def isfloat(arg):
    if (type(arg) is not str):
        raise TypeError("The arg argument isn't a string!")

    if (arg.replace('.', '', 1).isdigit() == True):
        return True
    else:
        return False

# Return True if db_filepath argument has one of the follow extensions: .db, .sqlite, or .sqlite3
def isdb(db_filepath):
    if (type(db_filepath) is not str):
        raise TypeError("The db_filepath argument isn't a string!")

    if (db_filepath.endswith(".db") == True or db_filepath.endswith(".sqlite") == True or db_filepath.endswith(".sqlite3") == True):
        return True
    else:
        return False