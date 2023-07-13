"""Module Holding Classes for Persistance Layer using SQLite3 module

Each class allows for individual operations as:
Create Table, Insert into Table, Read from Table,
  Update Row in Table, Delete Row in Table

Validation of inputs is not completed in this module - values must be validated
according to data types and requirements of each class before use of this module

Each class creates and closes its own connection to the database with each call of
     its respective 'execute()' method

Class Separations follow the Single Responsibility Principle. Design is generic
to maximise reusability
------------------------------------------------------------------------------------
"""
import sqlite3

class DatabaseController():
    """A class controlling connection to a database with 'connection' and 'cursor' objects.

    Attributes:
    -----------------
    database_name: str
        name of the database to connect to, also serves as path to database
        file if not present in current directory
    connection: class:sq3lite: Connection
        object to connect to database
    cursor: class:sqlite3.Cursor
        object to execute SQL statements against database

    Methods:
    ----------------
    init(self, database_name):
        Initialize Data_Controller Object with connection and cursor objects
        for SQLite3

    open_connection_and_create_cursor(self):
        attempts to create connection to specified database or create database
        if not present. Creates cursor object to database and returns cursor or
        'None' if successful connection is not made

    close_connection(self):
        attempts to close connection to current database
    """
    def __init__(self, database_name):
        """Constructor initialising database name and creation of 
           connection and cursor fields.

        Arguments:
        ---------------
        database_name: str
            name of database connection will be made to or create
        """
        self.database_name = database_name
        self.connection = None
        self.cursor = None

    def open_connection_and_create_cursor(self):
        """Attempt to create connection to specified database and return a cursor object.

        Return:
        ----------
        cursor: class:sqlite3.Cursor
            Returns None if connection to database should fail

        Exceptions:
        -------------
        sqlite3.OperationalError:
            Raised if connection to database cannot be made
        """
        try:
            # attempt to make connection to database. Creates database if not present.
            self.connection = sqlite3.connect(self.database_name)
            self.cursor = self.connection.cursor()
            return self.cursor

        except sqlite3.OperationalError as operation_error:
            # connection to database failed
            print(f"Error connecting to Database {self.database_name}")
            print(operation_error)
            return None

    def close_connection(self):
        """Complusory Function used to close connection to database. All classes utilising this
           class must ensure this function is called.

        Exceptions:
        -------------
        sqlite3.DatabaseError
            Raised is connection to database cannot be closed
        """
        try:
            self.connection.close()
        except sqlite3.DatabaseError as data_error:
            print("Error closing database connection")
            print(data_error)


class CreateTableSingleKey():
    """Allows for creation of a new table in a Database using SQLite3 with a
        non-compound Primary-Key. Fields are all set as "NOT NULL".

    Attributes:
    -----------------
    database_controller: DataBaseController
        object to connect to and query database
    database_name: str
        name of the database to connect to, also serves as path to database
        file if not present in current directory
    table_name: str
        name of new table to create in database
    primary_key: inherited from function call
        primary key for table creation(non-compound)
    int-list: list
        list containing names of fields that would hold integers
    text-list: list
        list containing names of fields that would hold strings (TEXT)
    float-list: list
        list containing names of fields that would hold floats (REAL)
    
    Methods:
    ----------------
    init(self, database_name, table_name, primary_key, int_list, text_list, float_list):
        Initialize CreateTableSingleKey Object and creating composed database_controller 
        object to connect to and create table in database

    execute(self):
        open connection to database, use class attributes to create new table in database and
        close connection to database.
    """

    # object to connect to and query database
    database_controller = None

    def __init__(self, database_name, table_name, primary_key, int_list=None,
                 text_list=None, float_list=None):
        """Constructor initialising CreateTableSingleKey object.

        Arguments:
        ---------------
        database_name: str
            name of the database to connect to, also serves as path to database
            file if not present in current directory
        table_name: str
            name of new table to create in database
        primary_key: inherited from function call
            primary key for table creation(non-compound)
        int-list: list (Optional - set to None as Default)
            list containing names of fields that would hold integers
        text-list: list (Optional - set to None as Default)
            list containing names of fields that would hold strings (TEXT)
        float-list: list (Optional - set to None as Default)
            list containing names of fields that would hold floats (REAL)  
        """
        self.table_name = table_name
        self.primary_key = primary_key
        self.int_list = int_list
        self.text_list = text_list
        self.float_list = float_list
        # object allowing for connection and creation of table in database
        self.database_controller = DatabaseController(database_name)

    def execute(self):
        """Connect to database, create SQL query comprised of desired table fields and execute
            to create new table. Close Database Connection.

        Return:
        ---------
        Returns None only if connection to database could not be made

        Exceptions:
        -----------
        sqlite.OperationalError:
            raised if SQL query is not correctly constructed and executed
        sqlite.DatabaseError:
            raised for errors in closing connection or errors not caught by: sqlite.OperationalError
        """
        try:
            # connection to database here to prevent multiple connections open at once
            self.cursor = self.database_controller.open_connection_and_create_cursor()

            if self.cursor is None:
                # failure to connect to Database and return a sqlite3.Cursor object
                print(f"Cannot Create New Table {self.table_name}")
                return None
            # retrieve already created sqlite3.Connection object
            self.connection = self.database_controller.connection

            # create initial part of query string with table name and single primary-key field
            query = f"""CREATE TABLE IF NOT EXISTS {self.table_name}({self.primary_key}
                INTEGER NOT NULL PRIMARY KEY"""

            # Iterate through each list below (if provided in class initialization) and add query
            # to create a field for each item
            if self.int_list is not None:
                for field in self.int_list:
                    query += f", {field} INTEGER NOT NULL"

            if self.text_list is not None:
                for field in self.text_list:
                    query += f", {field} TEXT NOT NULL"

            if self.float_list is not None:
                for field in self.float_list:
                    query += f", {field} REAL NOT NULL"

            # conclude query and execute against database to create table
            query += ")"
            self.cursor.execute(query)

        except sqlite3.OperationalError as operation_error:
            print(
                f"An error has occured trying to create table {self.table_name}")
            print(operation_error)
        except sqlite3.DatabaseError as database_error:
            print(database_error)
        finally:
            # close connection within method call
            self.database_controller.close_connection()


class InsertData:
    """Allows for insertion of single or multiple rows to table in database".

    Attributes:
    -----------------
    database_controller: DataBaseController
        object to connect to and query database
    database_name: str
        name of the database to connect to, also serves as path to database
        file if not present in current directory
    table_name: str
        name of new table to create in database
    row_data_list: list of tuples
        list containing at least one tuple with values to be inserted into table
        table must exist in database with values checked to match type and count 
        of table fields
    
    Methods:
    ----------------
    init(self, database_name, table_name, row_data_list):
        Initialize InsertData Object and creating composed database_controller 
        object to connect to and insert new row(s) to table

    execute(self):
        open connection to database, use values in tuples of row_data_list to add row(s) to table
    """

    # object to connect to and query database
    database_controller = None

    def __init__(self, database_name, table_name, row_data_list):
        """Constructor initialising InsertData object.

        Arguments:
        ---------------
        database_name: str
            name of the database to connect to, also serves as path to database
            file if not present in current directory
        table_name: str
            name of new table to create in database
        row_data_list: list of tuples (containing at least one)
            values to add in row(s) inserted into table
        """
        self.table_name = table_name
        self.row_data_list = row_data_list
        # object allowing for connection and creation of table in database
        self.database_controller = DatabaseController(database_name)


    def execute(self):
        """Connect to database, create SQL query to insert new row(s) into existing table and
            commit change. Close Database Connection.

        Return:
        ---------
        Returns None only if connection to database could not be made

        Exceptions:
        -----------
        sqlite.OperationalError:
            raised if SQL query is not correctly constructed and executed
        sqlite.DatabaseError:
            raised for errors in closing connection or errors not caught by: sqlite.OperationalError
        """
        try:
            # ensure connection is made and closed within function call only
            self.cursor = self.database_controller.open_connection_and_create_cursor()

            if self.cursor is None:
                # failure to connect to Database and return a sqlite3.Cursor object
                print(f"Cannot Insert Data to table {self.table_name}")
                return None
            # return the sqlite3.Connection object
            self.connection = self.database_controller.connection

            # begin query construction for row(s) insertion
            query = f"INSERT INTO {self.table_name} VALUES( "
            # retrieve first tuple to determine number of fields in table
            tup = self.row_data_list[0]
            for i in range(len(tup)):
                # create corresponding number of '?' according to number of fields in table
                query += "?"
                # stop adding commas for '?' separation
                if i != (len(tup) - 1):
                    query += ", "
            query += ")"

            if len(self.row_data_list) == 1:
                # execute for single row insertion (one tuple)
                self.cursor.execute(query, self.row_data_list[0])
            else:
                # execute for multiple row insertions
                self.cursor.executemany(query, self.row_data_list)
            self.connection.commit()

        except sqlite3.OperationalError as operational_error:
            print(
                f"An error has occured trying insert data into {self.table_name}")
            print(operational_error)
        except sqlite3.DatabaseError as database_error:
            print(database_error)
        finally:
            # close connection within method call
            self.database_controller.close_connection()


class ReadData:
    """Allows for reading of desired values from one row from table using multiple fields to
        perform check of matching attributes, returns matching row".

    Attributes:
    -----------------
    database_controller: DataBaseController
        object to connect to and query database
    database_name: str
        name of the database to connect to, also serves as path to database
        file if not present in current directory
    table_name: str
        name of new table to create in database
    fields_list: list of field names as strings
        desired fields to return values (enter * for all)
    where_fields_list: list of fields  as strings
        field names used in WHERE part of query to perform checks on
    search_vals: list with entities matching type corresponding to entity in where_fields_list
        values to be checked for match

    Methods:
    ----------------
    init(self, database_name, table_name, fields_list, where_field_list, search_vals):
        Initialize ReadData Object and create composed database_controller 
        object to connect to database

    execute(self):
        open connection to database, search for and return matching row from table,
        close database connection
    """
    # object to connect to and query database
    database_controller = None

    def __init__(self, database_name, table_name, fields_list, where_field_list, search_vals):
        """Constructor initialising InsertData object.

        Arguments:
        ---------------
        database_name: str
            name of the database to connect to, also serves as path to database
            file if not present in current directory
        table_name: str
            name of new table to create in database
        fields_list: list of field names as strings
            desired fields to return values
        where_fields_list: list of fields  as strings
            field names used in WHERE part of query to perform checks on
        search_vals: list with entities matching type corresponding to entity in where_fields_list
            values to be checked for match 
        """
        self.database_name = database_name
        self.table_name = table_name
        self.fields_list = fields_list
        self.where_fields_list = where_field_list
        self.search_vals = search_vals
        # object allowing for connection and creation of table in database
        self.database_controller = DatabaseController(database_name)

    def execute(self):
        """Connect to database, create SQL query to read row from table based on desired fields
        and values. Close Database Connection.

        Return:
        -----------
        Match Found - List with row as Tupple
        No Match - Empty List
        None - Field list does not have matching value count or connection could not be made

        Exceptions:
        -----------
        sqlite.OperationalError:
            raised if SQL query is not correctly constructed and executed
        sqlite.DatabaseError:
            raised for errors in closing connection or errors not caught by: sqlite.OperationalError
        """
        # confirm fields to check have corresponding values (by count)
        if len(self.where_fields_list) != len(self.search_vals):
            return None

        try:
            # ensure connection to database is made and closed within function call only
            self.cursor = self.database_controller.open_connection_and_create_cursor()

            if self.cursor is None:
                # connection could not be made and cursor object not created
                print(f"Cannot Insert data to table: {self.table_name}" +
                      " due to connection error.")
                return None
            # get connection object
            self.connection = self.database_controller.connection

            # start of query, add desired fields to be returned in row
            query = f"SELECT {', '.join(self.fields_list)} FROM {self.table_name}"


            if len(self.where_fields_list) != 0:
                query += " WHERE "
                for i in range(len(self.where_fields_list)):
                    query += f"{self.where_fields_list[i]} = {self.search_vals[i]}"

                    if i != len(self.where_fields_list) - 1:
                        query += " AND "

            # execute query and return row as tuple in list (empty list for no match)
            return self.cursor.execute(query).fetchall()

        except sqlite3.OperationalError as read_error:
            print(
                f"An error has occured trying to retrieve data from {self.table_name}")
            print(read_error)
        except sqlite3.DatabaseError as database_error:
            print(database_error)
        finally:
            # close connection to database
            self.database_controller.close_connection()

class UpdateData:
    """Modify a single field value for row in database".

    Attributes:
    -----------------
    database_controller: DataBaseController
        object to connect to and query database
    database_name: str
        name of the database to connect to, also serves as path to database
        file if not present in current directory
    table_name: str
        name of new table to create in database
    field_names: list of two strings
        string1 - field to change, string2 - primary_key field
    update_tuple: tuple
        contains new_value to assign, old value for row determination

    Methods:
    ----------------
    init(self, database_name, table_name, field_names, update_tuple):
        Initialize Update Object and create composed database_controller 
        object to connect to database

    execute(self):
        open connection to database, attempt to update value in a row, close database connection
    """
    # object to connect to and query database
    database_controller = None

    def __init__(self, database_name, table_name, field_names, update_tuple):
        """Constructor initialising UpdateData object.

        Arguments:
        ---------------
        database_name: str
            name of the database to connect to, also serves as path to database
            file if not present in current directory
        table_name: str
            name of new table to create in database
        field_names: list of two strings
            string1 - field to change, string2 - primary_key field
        update_tuple: tuple
            contains new_value to assign, old value for row determination
        """
        self.database_name = database_name
        self.table_name = table_name
        self.field_names = field_names
        self.update_tuple = update_tuple
        # object allowing for connection and creation of table in database
        self.database_controller = DatabaseController(database_name)

    def execute(self):
        """Connect to database, create SQL query to update one value in row. Close Database Connection.

        Return:
        -----------
        Only returns None if there was an error when attemting to connect to database

        Exceptions:
        -----------
        sqlite.OperationalError:
            raised if SQL query is not correctly constructed and executed
        sqlite.DatabaseError:
            raised for errors in closing connection or errors not caught by: sqlite.OperationalError
        """

        try:
            # attempt to connect to database and retrieve cursor object
            self.cursor = self.database_controller.open_connection_and_create_cursor()

            if self.cursor is None:
                print(
                    f"Cannot make update to table {self.table_name} due to connection error")
                return None
            # retrieve sq3lite.Connection object
            self.connection = self.database_controller.connection

            # create and execute query using field names and desired values
            query = (f"UPDATE {self.table_name} SET {self.field_names[0]} = ? " +
                     f"WHERE {self.field_names[1]}  = ?")
            self.cursor.execute(query, self.update_tuple)
            self.connection.commit()

        except sqlite3.OperationalError as update_error:
            print(
                f"An error has occured trying update data in {self.table_name}")
            print(update_error)
        except sqlite3.DatabaseError as database_error:
            print(database_error)
        finally:
            # close connection to database
            self.database_controller.close_connection()


class DeleteData:
    """Delete a single value row in database".

    Attributes:
    -----------------
    database_controller: DataBaseController
        object to connect to and query database
    database_name: str
        name of the database to connect to, also serves as path to database
        file if not present in current directory
    table_name: str
        name of new table to create in database
    primary_key: str
        name of primary_key field
    key_value: type specific to table (cannot be composite) 
        unique value determining row to delete

    Methods:
    ----------------
    init(self, database_name, table_name, primary_key, key_value):
        Initialize DeleteData object and create composed database_controller object to connect to
        database

    execute(self):
        open connection to database, attempt to delete matching row, close database connection
    """
    # object to connect to and query database
    database_controller = None

    def __init__(self, database_name, table_name, primary_key, key_value):
        """Constructor initialising DeleteData object.

        Arguments:
        ---------------
        database_name: str
            name of the database to connect to, also serves as path to database
            file if not present in current directory
        table_name: str
            name of new table to create in database
        primary_key: str
            name of primary_key field
        key_value: type specific to table (cannot be composite) 
            unique value determining row to delete
        """
        self.database_name = database_name
        self.table_name = table_name
        self.primary_key = primary_key
        self.key_value = key_value
        # object allowing for connection and creation of table in database
        self.database_controller = DatabaseController(database_name)

    def execute(self):
        """Connect to database, create SQL query to delete one row. Close Database Connection.

        Return:
        -----------
        Only returns None if there was an error when attemting to connect to database

        Exceptions:
        -----------
        sqlite.OperationalError:
            raised if SQL query is not correctly constructed and executed
        sqlite.DatabaseError:
            raised for errors in closing connection or errors not caught by: sqlite.OperationalError
        """
        try:
            # open connection to database and return sqlite3.Cursor Object
            self.cursor = self.database_controller.open_connection_and_create_cursor()

            if self.cursor is None:
                # error with connection
                print(
                    f"Cannot Delete row from {self.table_name} due to connection error")
                return None
            # connection to database was successful, retrieve sqlite3.Connection object
            self.connection = self.database_controller.connection

            # create and execute query using primary_key field and value to delete desired row
            query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} = ?"
            self.cursor.execute(query, self.key_value)
            self.connection.commit()

        except sqlite3.OperationalError as operational_error:
            print(
                f"An error has occured trying to delete data from {self.table_name}")
            print(operational_error)
        except sqlite3.DatabaseError as database_error:
            print(database_error)
        finally:
            # close connection to database
            self.database_controller.close_connection()
