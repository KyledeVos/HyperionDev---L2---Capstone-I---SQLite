"""Module Holding Classes for Persistance Layer for tables with non-composite
    primary_key using sqlite3. Classes here are referenced in other modules
    as 'Persistance Controllers'

Superclass 'DataBaseQueryClass' utilises helper class 'DatabaseController' to
manage and abstract away database connections from creation of sqlite3 queries.

Module Usage:
-------------
Use of this module should only be through child classes of 'DataBaseQueryClass' as:
'CreateTableSingleKey', 'VerifyTable', 'InsertData', 'ReadData', ''UpdateData' and
'DeleteData'
NOTE: all child classes have method 'execute()' that must be called for class usage

Classes:
--------
DatabaseController:
    A Helper class controlling connection to a database with 'connection' and 'cursor' objects.

    Methods:
    --------
    __init__(self, database_name):
        Initialize DataBaseController Object with connection and cursor objects for sqlite3

    open_connection_and_create_cursor(self):
        attempts to create connection to specified database or create database
        if not present. Creates cursor object to database and returns cursor or
        'None' if successful connection is not made

    close_connection(self):
        attempts to close connection to current database. Any class using 'DataBaseController'
        instance MUST call this method.

DataBaseQueryClass:
    super class defining structure of methods to initialize database access object
     and execution of query to database.

    Methods:
    --------
    __init__(self, database_name, table_name):
        instantiate instance of class

    execute(self):
        method defining logic to execute query against database. Must be overridden by child class.

    create_database_connection(self):
        attempt to create database connection and initialize "connection"
        "cursor" objects

CreateTableSingleKey:
    Child class of DataBaseQueryClass allowing for creation of a new table in a Database using
    sqlite3 with a non-compound Primary-Key. Fields are all set as "NOT NULL".

    Methods:
    --------
    __init__(self, database_name, table_name, primary_key, int_list, text_list, float_list):
        Initialize CreateTableSingleKey and parent DataBaseQueryClass objects allowing
        for sqlite3 connection. Parent contructor attempts to create connection to database.

    execute(self): 'override'
        Use class attributes to create new table in database and then close database connection.

VerifyTable:
    child class of DataBaseQueryClass to verify if a table exists in specified database

    Methods:
    --------
    __init__(self, database_name, table_name):
        Constructor initialising VerifyTable and DataBaseQueryClass parent objects

    execute(self): 'override'
        Connect to database, create SQL query to return count of tables in database
         with name equal to 'table_name'. Close Database Connection.

InsertData:
    Allows for insertion of single or multiple rows to table in database

    Methods:
    ----------------
    __init__(self, database_name, table_name, row_data_list):
        Initialize InsertData and parent DataBaseQueryClass objects allowing
        for sqlite3 connection. Parent contructor attempts to create connection to database.

    execute(self): 'override'
        Use values in tuples of row_data_list to add row(s) to table and close database connection

ReadData:
    Allows reading of desired values from table and returns matching row(s)

    Methods:
    ----------------
    __init__(self, database_name, table_name, fields_list, where_field_list, search_vals):
        Initialize ReadData and parent DataBaseQueryClass objects allowing
        for sqlite3 connection. Parent contructor attempts to create connection to database.

    execute(self): 'override'
        Search for and return matching row from table and close database connection

UpdateData:
    Modify a single field value for row in database using primary_key value

    Methods:
    ----------------
    __init__(self, database_name, table_name, field_names, update_tuple):
        Initialize UpdateData and parent DataBaseQueryClass objects allowing
        for sqlite3 connection. Parent contructor attempts to create connection to database.

    execute(self): 'override'
        Attempt to update value in a row and close database connection

DeleteData:
    Delete a single row in database using only primary_key value

    Methods:
    ----------------
    __init__(self, database_name, table_name, primary_key, key_value):
        Initialize DeleteData and parent DataBaseQueryClass objects allowing
        for sqlite3 connection. Parent contructor attempts to create connection to database.

    execute(self): 'override'
        Attempt to delete matching row and close database connection. Returns True or False
        to confirm deletion of a row(s)

ReturnLastId:
    Retrieve primary_key value in last row of table in database.

    Methods:
    --------
    __init__(self, database_name, table_name, primary_key):
        Constructor initialising ReturnLastId and DataBaseQueryClass parent objects.

    execute(self): 'override'
        Connect to database, create SQL query to retrieve last row primary_key value.
         Close Database Connection
------------------------------------------------------------------------------------
"""
import sqlite3

class DatabaseController():
    """A Helper class controlling connection to a database with 'connection' and 'cursor' objects.

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
    __init__(self, database_name):
        Initialize DataBaseController Object with connection and cursor objects
        for sqlite3

    open_connection_and_create_cursor(self):
        attempts to create connection to specified database or create database
        if not present. Creates cursor object to database and returns cursor or
        'None' if successful connection is not made

    close_connection(self):
        attempts to close connection to current database. Any class using 'DataBaseController'
        instance MUST call this method.
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
            # retrieve cursor object from data_base connection
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
            Raised if connection to database cannot be closed
        """
        try:
            self.connection.close()
        except sqlite3.DatabaseError as data_error:
            print("Error closing database connection")
            print(data_error)


# -------------------------------------------------------------------------------------------------
class DataBaseQueryClass():
    """super class defining structure of methods to initialize database access object
        and execution of query to database.

    Attributes:
    -----------
    database_controller: DataBaseController
        object to connect to and query database
    connection: class:sqlite3.Connection:
        connection object to database
    cursor: class:sqlite3.Cursor
        cursor object to perform queries against database
    database_name: str
        name of the database to connect to, also serves as path to database
        file if not present in current directory
    table_name: str
        name of new table to create in database

    Methods:
    -----------
    __init__(self, database_name, table_name):
        instantiate instance of class

    execute(self):
        method defining logic to execute query against database. Must be overridden by child class.

    create_database_connection(self):
        attempt to create database connection and initialize "connection" and "cursor" objects
    """

    def __init__(self, database_name, table_name):
        """Constructor to initialise object.

        Arguments:
        -----------
        database_name: str
            name of the database to connect to, also serves as path to database
            file if not present in current directory
        table_name: str
            name of new table to create in database

        Attributes:
        -----------
        database_controller: DataBaseController
            object to connect to and query database
        connection: class:sqlite3.Connection:
            connection object to database
        cursor: class:sqlite3.Cursor
            cursor object to perform queries against database
        """
        self.database_name = database_name
        self.table_name = table_name
        self.database_controller = DatabaseController(self.database_name)
        self.connection = None
        self.cursor = None

    def execute(self):
        """Method to be overridden. Defines logic for creation of query
            and execution against a database"""

    def create_database_connection(self):
        """attempt to retrieve sqlite3.Cursor and sqlite3.Connection objects using 
            database controller objects"""
        self.cursor = self.database_controller.open_connection_and_create_cursor()

        if self.cursor is not None:
            # connection to database was successful, retrieve connection object
            self.connection = self.database_controller.connection


# -------------------------------------------------------------------------------------------------
class CreateTableSingleKey(DataBaseQueryClass):
    """Child class allowing for creation of a new table in a Database using SQLite3 with a
        non-compound Primary-Key. Fields are all set as "NOT NULL".

    Attributes:
    -----------------
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
    __init__(self, database_name, table_name, primary_key, int_list, text_list, float_list):
        Initialize CreateTableSingleKey and parent DataBaseQueryClass objects allowing
        for sqlite3 connection. Parent contructor attempts to create connection to database.

    execute(self):
        Use class attributes to create new table in database and then close database connection.
    """

    def __init__(self, database_name, table_name, primary_key, int_list=None,
                 text_list=None, float_list=None):
        """Constructor initialising CreateTableSingleKey and parent DataBaseQueryClass objects.

        Arguments:
        ---------------
        primary_key: inherited from function call
            primary key for table creation (non-compound)
        int-list: list (Optional - set to None as Default)
            list containing names of fields that would hold integers
        text-list: list (Optional - set to None as Default)
            list containing names of fields that would hold strings (TEXT)
        float-list: list (Optional - set to None as Default)
            list containing names of fields that would hold floats (REAL)  
        """
        super().__init__(database_name, table_name)
        self.primary_key = primary_key
        self.int_list = int_list
        self.text_list = text_list
        self.float_list = float_list

        # attempt to make connection to database (through super class)
        # successful connection will initialise 'cursor' and 'connection' objects
        #   in parent class
        self.create_database_connection()

    def execute(self):
        """Create SQL query comprised of desired table fields and execute
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
        # check if connection (in parent class) to database in __init__() was successful,
        # it not return None
        if self.connection is None:
            return None

        try:
            # create initial part of query string with table name and single primary_key field
            query = (f"CREATE TABLE IF NOT EXISTS {self.table_name}({self.primary_key} " +
                     "INTEGER NOT NULL PRIMARY KEY")

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
            # cursor in parent class
            self.cursor.execute(query)

        except sqlite3.OperationalError as operation_error:
            print(
                f"An error has occured trying to create table {self.table_name}")
            print(operation_error)
        except sqlite3.DatabaseError as database_error:
            print(database_error)
        finally:
            # close connection within method call to parent class
            self.database_controller.close_connection()

# -------------------------------------------------------------------------------------------------
class VerifyTable(DataBaseQueryClass):
    """Verify if a table exists in specified database.
    
    Attributes:
    -----------
    database_name: str
        name of database to connect to
    table_name: str
        name of table in above database

    Methods:
    --------
    __init__(self, database_name, table_name):
        Constructor initialising VerifyTable and DataBaseQueryClass parent objects

    execute(self):
        Connect to database, create SQL query to return count of tables in database
         with name equal to 'table_name'. Close Database Connection.
    """

    def __init__(self, database_name, table_name):
        """Constructor initialising VerifyTable and DataBaseQueryClass parent objects.

        Arguments:
        ---------------
        database_name: str
            name of the database to connect to, also serves as path to database
            file if not present in current directory
        table_name: str
            name of table to connect to in database
        """
        super().__init__(database_name, table_name)
        # attempt to make connection to database (through super class)
        # successful connection will initialise 'cursor' and 'connection' objects
        self.create_database_connection()

    def execute(self):
        """Connect to database, create SQL query to return count of tables in database
            with name equal to 'table_name'. Close Database Connection.

        Return:
        -----------
        Returns None if there was an error when attempting to connect to database
        Returns True if table count is 1 (table exists)
        Returns False if table count is 0 (table does not exist)

        Exceptions:
        -----------
        sqlite.OperationalError:
            raised if SQL query is not correctly constructed and executed
        sqlite.DatabaseError:
            raised for errors in closing connection or errors not caught by: sqlite.OperationalError
        """
        # check if connection (in parent class) to database was successful,
        if self.connection is None:
            return None
        try:
            # create and execute query to return number of tables with name equal to 'table_name'
            # Referenced from Python Examples on 18 July 2023
            # Available from: https://pythonexamples.org/python-sqlite3-check-if-table-exists/
            table_count = self.cursor.execute("SELECT count(name) FROM sqlite_master WHERE " +
                                              f"type='table' AND name=\'{self.table_name}\'").\
                fetchone()

            # if a table was found with matching name, return True. If not, return False
            return True if table_count[0] == 1 else False

        except sqlite3.OperationalError as operational_error:
            print(
                f"An error has occured trying to confirm existence of table {self.table_name}")
            print(operational_error)
            return None
        except sqlite3.DatabaseError as database_error:
            print(database_error)
            return None
        finally:
            # close connection to database with parent class
            self.database_controller.close_connection()


# -------------------------------------------------------------------------------------------------
class InsertData(DataBaseQueryClass):
    """Allows for insertion of single or multiple rows to table in database.

    Attributes:
    -----------------
    row_data_list: list of tuples
        list containing at least one tuple with values to be inserted into table.
         table must exist in database with values checked to match type and count 
         of table fields

    Methods:
    ----------------
    __init__(self, database_name, table_name, row_data_list):
        Initialize InsertData and parent DataBaseQueryClass objects allowing
        for sqlite3 connection. Parent contructor attempts to create connection to database.

    execute(self):
        Use values in tuples of row_data_list to add row(s) to table and close database connection
    """

    def __init__(self, database_name, table_name, row_data_list):
        """Constructor initialising InsertData and parent DataBaseQueryClass objects object.

        Arguments:
        ---------------
        database_name: str
            name of the database to connect to, also serves as path to database
            file if not present in current directory
        table_name: str
            name of table to connect to in database
        row_data_list: list of tuples (containing at least one)
            values to add in row(s) inserted into table
            NOTE: values MUST be added in same order as those used when table was created
        """
        super().__init__(database_name, table_name)
        self.row_data_list = row_data_list
        # attempt to make connection to database (through super class)
        # successful connection will initialise 'cursor' and 'connection' objects
        self.create_database_connection()

    def execute(self):
        """Connect to database, create SQL query to insert new row(s) into existing table and
            commit change. Close Database Connection.

        Return:
        ---------
        Returns None only if connection to database could not be made
        Return True for more than one row added, False for no rows added

        Exceptions:
        -----------
        sqlite.OperationalError:
            raised if SQL query is not correctly constructed and executed
        sqlite.DatabaseError:
            raised for errors in closing connection or errors not caught by: sqlite.OperationalError
        """
        # check if connection (in parent class) to database in __init__() was successful,
        # it not return None
        if self.connection is None:
            return None

        try:
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
            # close query string
            query += ")"

            if len(self.row_data_list) == 1:
                # execute for single row insertion (one tuple)
                self.cursor.execute(query, self.row_data_list[0])
            else:
                # execute for multiple row insertions with cursor in parent class
                self.cursor.executemany(query, self.row_data_list)
            self.connection.commit()

            # determine number of affected rows and return True if more than one row
            # was affected with database query
            affected_rows = self.cursor.rowcount
            return True if affected_rows > 0 else False

        except sqlite3.OperationalError as operational_error:
            print(
                f"An error has occured trying to insert data into {self.table_name}")
            print(operational_error)
        except sqlite3.DatabaseError as database_error:
            print(database_error)
        finally:
            # close connection within method call to parent class
            self.database_controller.close_connection()


# -------------------------------------------------------------------------------------------------
class ReadData(DataBaseQueryClass):
    """Allows for reading of desired values from table using multiple fields to
        perform check of matching attributes. Returns matching row(s).

    Attributes:
    -----------------
    fields_list: list of field names as strings
        desired fields to return values (provide '*' for all)
    where_fields_list: list of fields as strings
        field names used in WHERE part of query to perform checks on
    search_vals: tuple with entities matching type corresponding to entity in where_fields_list
        values to be checked for match

    Methods:
    ----------------
    __init__(self, database_name, table_name, fields_list, where_field_list, search_vals):
        Initialize ReadData and parent DataBaseQueryClass objects allowing
        for sqlite3 connection. Parent contructor attempts to create connection to database.

    execute(self):
        Search for and return matching row from table and close database connection
    """

    def __init__(self, database_name, table_name, fields_list, where_field_list=None,
                 search_vals=None):
        """Constructor initialising ReadData and parent DataBaseQueryClass objects.

        Arguments:
        ---------------
        database_name: str
            name of the database to connect to, also serves as path to database
            file if not present in current directory
        table_name: str
            name of table to connect to in database
        fields_list: list of field names as strings
            desired fields to return values from
        where_fields_list: list of fields as strings        
            field names used in WHERE part of query to perform checks on
        search_vals: tuple with entities matching type corresponding to entity in where_fields_list
            values to be checked for match 
        """
        super().__init__(database_name, table_name)
        self.fields_list = fields_list
        self.where_fields_list = where_field_list
        self.search_vals = search_vals
        # attempt to make connection to database (through super class)
        # successful connection will initialise 'cursor' and 'connection' objects
        self.create_database_connection()

    def execute(self):
        """Create SQL query to read row from table based on desired fields and values.
            Close Database Connection.

        Return:
        -----------
        Match Found - List with row as Tuple
        No Match - Empty List
        None - Field list does not have matching value count or connection could not be made

        Exceptions:
        -----------
        sqlite.OperationalError:
            raised if SQL query is not correctly constructed and executed
        sqlite.DatabaseError:
            raised for errors in closing connection or errors not caught by: sqlite.OperationalError
        """
        # check if connection (in parent class) to database in __init__() was successful,
        if self.connection is None:
            return None

        try:
            # start of query, add desired fields to be returned in row
            query = f"SELECT {', '.join(self.fields_list)} FROM {self.table_name}"

            # Conditions for row to match (may be none)
            # Add name of field and specified value to query
            if self.where_fields_list is not None:
                query += " WHERE "
                for count, where_field in enumerate(self.where_fields_list):
                    # add each required field name for checking
                    query += f"{where_field} = ? "
                    # append 'AND' for multiple queries if supplied
                    if count != len(self.where_fields_list) - 1:
                        query += " AND "

            # execute query and store returned row(s)
            # Case 1: Return all rows (no 'where' condition)
            if self.where_fields_list is None:
                rows_returned = self.cursor.execute(query).fetchall()
            # Case 2: Single 'where' condition - manually add comma for tuple
            elif len(self.where_fields_list) == 1:
                rows_returned = self.cursor.execute(
                    query, (self.search_vals), ).fetchall()
            # Case 3: Multiple 'where' conditions, use search_vals tuple as is
            else:
                rows_returned = self.cursor.execute(
                    query, self.search_vals).fetchall()

            # if at least one row was returned, retrieve field names
            # Referenced from AlixaProDev on 19 July 2023
            # Available from:
            # https://www.alixaprodev.com/how-to-get-column-names-from-sqlite-database-table-in-python/
            if len(rows_returned) > 0:
                self.cursor.execute(f"SELECT * FROM {self.table_name}")
                field_names = tuple([description[0]
                                    for description in self.cursor.description])

                # combine field_names tuple and returned database rows
                fields_and_values = []
                fields_and_values.append(field_names)
                fields_and_values.extend(rows_returned)
                # return field_names and row(s) returned from database
                return fields_and_values
            # no rows were returned, return empty list
            else:
                return rows_returned

        except sqlite3.OperationalError as read_error:
            print(
                f"An error has occured trying to retrieve data from {self.table_name}")
            print(read_error)
        except sqlite3.DatabaseError as database_error:
            print(database_error)
        finally:
            # close connection to database with parent class
            self.database_controller.close_connection()


# -------------------------------------------------------------------------------------------------
class UpdateData(DataBaseQueryClass):
    """Modify a single field value for row in database using only Primary Key value.

    Attributes:
    -----------------
    field_names: list of two strings
        string1 - field to change, string2 - primary_key field
    update_tuple: tuple
        contains new_value to assign, old value for row determination

    Methods:
    ----------------
    __init__(self, database_name, table_name, field_names, update_tuple):
        Initialize UpdateData and parent DataBaseQueryClass objects allowing
        for sqlite3 connection. Parent contructor attempts to create connection to database.

    execute(self):
        Attempt to update value in a row and close database connection
    """

    def __init__(self, database_name, table_name, field_names, update_tuple):
        """Constructor initialising UpdateData and parent DataBaseQueryClass objects.

        Arguments:
        ---------------
        database_name: str
            name of the database to connect to, also serves as path to database
            file if not present in current directory
        table_name: str
            name of table in above database
        field_names: list of two strings
            string1 - field to change, string2 - primary_key field
        update_tuple: tuple
            contains new_value to assign, old value for row determination
        """
        super().__init__(database_name, table_name)
        self.field_names = field_names
        self.update_tuple = update_tuple
        # attempt to make connection to database (through super class)
        # successful connection will initialise 'cursor' and 'connection' objects
        self.create_database_connection()

    def execute(self):
        """Create and execute SQL query to update one value in row. Close Database Connection.

        Return:
        -----------
         None if there was an error when attempting to connect to database
         True if one row was affected by update to database, False if no rows were affected

        Exceptions:
        -----------
        sqlite.OperationalError:
            raised if SQL query is not correctly constructed and executed
        sqlite.DatabaseError:
            raised for errors in closing connection or errors not caught by: sqlite.OperationalError
        """
        # check if connection (in parent class) to database was successful,
        if self.connection is None:
            return None

        try:
            # create and execute query using field names and desired values
            query = (f"UPDATE {self.table_name} SET {self.field_names[0]} = ? " +
                     f"WHERE {self.field_names[1]}  = ?")
            self.cursor.execute(query, self.update_tuple)
            self.connection.commit()

            # retrieve number of affected rows after update query has been executed
            affected_rows = self.cursor.rowcount
            # if at least one row was updated, return True to confirm deletion
            return True if affected_rows > 0 else False

        except sqlite3.OperationalError as update_error:
            print(
                f"An error has occured trying to update data in {self.table_name}")
            print(update_error)
        except sqlite3.DatabaseError as database_error:
            print(database_error)
        finally:
            # close connection to database with parent class
            self.database_controller.close_connection()


# -------------------------------------------------------------------------------------------------
class DeleteData(DataBaseQueryClass):
    """Delete a single row in database using only Primary_key value.

    Attributes:
    -----------------
    primary_key: str
        name of primary_key field
    key_value: type specific to table (cannot be composite) 
        unique value determining row to delete

    Methods:
    ----------------
    __init__(self, database_name, table_name, primary_key, key_value):
        Initialize DeleteData and parent DataBaseQueryClass objects allowing
        for sqlite3 connection. Parent contructor attempts to create connection to database.

    execute(self):
        Attempt to delete matching row and close database connection. Returns True or False
        to confirm deletion of a row(s)
    """

    def __init__(self, database_name, table_name, primary_key, key_value):
        """Constructor initialising DeleteData and DataBaseQueryClass parent objects.

        Arguments:
        ---------------
        database_name: str
            name of the database to connect to, also serves as path to database
            file if not present in current directory
        table_name: str
            name of table to connect to in database
        primary_key: str
            name of primary_key field
        key_value: type specific to table (cannot be composite) 
            unique value determining row to delete
        """
        super().__init__(database_name, table_name)
        self.primary_key = primary_key
        self.key_value = key_value
        # attempt to make connection to database (through super class)
        # successful connection will initialise 'cursor' and 'connection' objects
        self.create_database_connection()

    def execute(self):
        """Connect to database, create SQL query to delete one row. Close Database Connection.

        Return:
        -----------
        Returns None if there was an error when attempting to connect to database
        Return True if the number of affected rows after deletion is greater than 0
        Return False if number of affected rows is 0

        Exceptions:
        -----------
        sqlite.OperationalError:
            raised if SQL query is not correctly constructed and executed
        sqlite.DatabaseError:
            raised for errors in closing connection or errors not caught by: sqlite.OperationalError
        """
        # check if connection (in parent class) to database was successful,
        if self.connection is None:
            return None
        try:
            # create and execute query using primary_key field and value to delete desired row
            query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} = ?"
            # convert received value for primary_key into tuple for query execution
            self.cursor.execute(query, (self.key_value,))
            self.connection.commit()

            # retrieve number of affected rows after deletion query has been executed
            affected_rows = self.cursor.rowcount
            # if at least one row was deleted, return True to confirm deletion
            return True if affected_rows > 0 else False

        except sqlite3.OperationalError as operational_error:
            print(
                f"An error has occured trying to delete data from {self.table_name}")
            print(operational_error)
        except sqlite3.DatabaseError as database_error:
            print(database_error)
        finally:
            # close connection to database with parent class
            self.database_controller.close_connection()


# -------------------------------------------------------------------------------------------------
class ReturnLastId(DataBaseQueryClass):
    """Retrieve primary_key value in last row of table in database.
    
    Atrributes:
    -----------
    database_name: str
        name of database to connect to
    table_name: str
        name of table in above database
    primary_key: str
        name of primary_key field

    Methods:
    --------
    __init__(self, database_name, table_name, primary_key):
        Constructor initialising ReturnLastId and DataBaseQueryClass parent objects.

    execute(self):
        Connect to database, create SQL query to retrieve last row primary_key value.
         Close Database Connection
    """

    def __init__(self, database_name, table_name, primary_key):
        """Constructor initialising ReturnLastId and DataBaseQueryClass parent objects.

        Arguments:
        ---------------
        database_name: str
            name of the database to connect to, also serves as path to database
            file if not present in current directory
        table_name: str
            name of table to connect to in database
        primary_key: str
            name of primary_key field
        """
        super().__init__(database_name, table_name)
        self.primary_key = primary_key
        # attempt to make connection to database (through super class)
        # successful connection will initialise 'cursor' and 'connection' objects
        self.create_database_connection()

    def execute(self):
        """Connect to database, create SQL query to retrieve last row primary_key value.
            Close Database Connection.

        Return:
        -----------
        Returns None if there was an error when attempting to connect to database
        Returns 0 if table in database is empty (default primary_key value for Integer type)
        Returns primary_key value for last row in non-empty table

        Exceptions:
        -----------
        sqlite.OperationalError:
            raised if SQL query is not correctly constructed and executed
        sqlite.DatabaseError:
            raised for errors in closing connection or errors not caught by: sqlite.OperationalError
        """
        # check if connection (in parent class) to database was successful,
        if self.connection is None:
            return None
        try:
            # create and execute query using primary_key field_name to return last row in database
            row = self.cursor.execute(f"SELECT * FROM {self.table_name} ORDER BY " +
                                      f"{self.primary_key} DESC LIMIT 1").fetchall()

            # if table is empty, return 0
            if len(row) == 0:
                return 0
            # return primary key value of last row in table
            else:
                return row[0][0]

        except sqlite3.OperationalError as operational_error:
            print(
                f"An error has occured trying to retrieve last row id from {self.table_name}")
            print(operational_error)
            return None
        except sqlite3.DatabaseError as database_error:
            print(database_error)
            return None
        finally:
            # close connection to database with parent class
            self.database_controller.close_connection()
