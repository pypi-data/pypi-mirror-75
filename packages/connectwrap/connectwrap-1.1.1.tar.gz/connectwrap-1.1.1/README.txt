connectwrap

A Python package built on top of the sqlite3 module made specifically for SQLite database management & object relational mapping.

Make sure to have the latest version of Python 3 installed although this should work with previous versions.  

To install the package with pip enter command in terminal:
    pip install connectwrap

To uninstall the package with pip enter command in terminal:
    pip uninstall connectwrap

---------
Module db
---------

db_filepath: 	                        Attribute of the string type representing the database file path.
                                        The file must have a .db, .sqlite, or .sqlite3 extension.
                                        This is the only attribute needed for the object's argument. The other attributes are generated from this.

connection: 	                        Attribute of the Connection type from the sqlite3 module representing the database connection. Used to commit changes to database.

connection_cursor: 	                    Attribute of the Cursor type from the sqlite3 module representing the database connection cursor. Used to execute queries.

connection_status: 	                    Attribute of the bool type representing whether the Database connection is opened or closed.
                                        Set to True upon the creation of a new Database object.
                                        Opened = True
                                        Closed = False

DatabaseOpenError: 	                    Custom exception to raise when the Database is open.

DatabaseNotOpenError: 	                Custom exception to raise when the Database is not open.

TableNotFoundError: 	                Custom exception to raise when an argument table doesn't exist in a database.

TableExistsError: 	                    Custom exception to raise when an argument table already exists in a database.

execute(query): 	                    Execute a custom query. The query argument must be a string.

commit(): 	                            Commit a query held in the connection cursor. 

close_db(): 	                        Close database connection.

open_db(): 	                            Open database connection. Reset the cursor.

set_db_filepath(db_filepath): 	        Change the db_filepath attribute value.
                                        The file must have a .db, .sqlite, or .sqlite3 extension.
                                        This allows you to switch between file databases while only creating one object.
                                        Works on open or closed databases. The result of this method will be an open Database using the db_filepath argument as the new Database file path.

get_connection_status(): 	            Return the connection_status attribute representing whether the Database connection is open or closed.
                                        Opened = True
                                        Closed = False

get_db_filepath(): 	                    Return the db_filepath attribute value representing the database file path.

get_tablenames(): 	                    Select and return the table names within a database as strings in a list.

get_keys(db_table): 	                Select and return the key names within a table as strings in a list.

get_column(db_table, key): 	            Select and return a list of the values in a column based on the key from that column.

get_row(db_table, key, value): 	                    Select and return a dictionary representing a row in the database table where the key and value arguments match a row column key and value pair.
                                                    Only returns the first row with the occurance of the key/value argument pair.
                                                    Returns None if there's no occurance of the key/value argument in any row in the table.
                                                    The key argument must be a string and a key within the table.
                                                    The value argument must be one of the following types - int, float, str, bytes, None.
                                                    Use a key with a unique value for best results.

get_table(db_table): 	                            Select and return a list of dictionaries with each dictionary representing a row in a table.

rename_table(old_table_name, new_table_name): 	    Rename a table.

drop_table(db_table): 	                            Drop/delete table in the file database.

drop_row(db_table, key, value): 	                Drop/delete rows within a table with matching key & value.
                                                    The key argument must be a string and a key within the table.
                                                    The value argument must be one of the following types - int, float, str, bytes, None.

create_table(db_table, **kwargs): 	                Create table within the file database.
                                                    The key in each kwargs entry denotes the key name of a column.
                                                    The value in each kwargs entry denotes the data type of a column.
                                                    The value in each kwargs entry must be one of the following strings - 'int', 'float', 'str', 'bytes', 'None'.

create_column(db_table, column, datatype): 	        Create a new column within a table.
                                                    The datatype argument must be one of the following strings - 'int', 'float', 'str', 'bytes', 'None'.

select_tablenames(): 	                            Select and output to terminal the table names within a database.

select_table(db_table): 	                        Select and output to terminal the rows as dictionaries from a table.

select_column(db_table, *args): 	                Select and output to terminal the values from keys within a table.
                                                    Each arg in *args arguments must be strings containing key names within the table.

select_keys(db_table): 	                        Select and output to terminal the key names within a table.

select_row(db_table, key, value): 	            Select and output to terminal a row of a table in a database.
                                                Only outputs the first row with the occurance of the key/value argument pair.
                                                Outputs None if there's no occurance of the key/value argument in any row in the table.
                                                The key argument must be a string and a key within the table.
                                                The value argument must be one of the following types - int, float, str, bytes, None.
                                                Use a key with a unique value for best results.

insert_row(db_table, *args): 	                Insert row of data into table.
                                                Each arg in *args must be one of the following types - int, float, str, bytes, None.

update_row(db_table, change_key, change_value, check_key, check_value): 	            Update/change row column values within a table.
                                                                                        The key arguments must be strings and keys within the table.
                                                                                        The value arguments must be one of the following types - int, float, str, bytes, None.

key_exists(db_table, key): 	                        Return True if the key argument exists in a table.

table_exists(db_table): 	                        Return True if the db_table argument is a table name within the database. 

------------
Module utils
------------

drop_database(db_filepath): 	    Drop/delete .db, .sqlite, or .sqlite3 file database.

create_database(db_filepath): 	    Create .db, .sqlite, or .sqlite3 file database.

ishex(arg): 	                    Return True if all characters in arg string are hexadecimal.

isfloat(arg): 	                    Return True if arg string characters constitute a float.

isdb(db_filepath): 	                Return True if db_filepath argument has one of the follow extensions: .db, .sqlite, or .sqlite3 