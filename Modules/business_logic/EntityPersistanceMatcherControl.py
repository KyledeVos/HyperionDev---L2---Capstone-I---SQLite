"""Module Holding Classes Matching an Entity to a Persistance Class
Entity - Module of classes for controlling user_input and business logic (eg Book, Employee).
        Classes should implement CRUD operations

Persistance Class - A class or module of classes using data from an 'Entity' to create and execute
                    Queries against a database

Classes in this module take validated data (in the form of an object instance) from a user and
use method calls for this module to determine the correct Persistance Classes to execute this data
to a database.

Data is returned from database queries in the form of None, row(s) as lists and booleans to confirm
database query execution statuses.
"""
from Modules.business_logic import book
from Modules.persistance_layer import persistence_classes_single_key


class EntityPersistanceSingleKeyControl:
    """"""

    def __init__(self, table_name, database_name, user_action):
        """"""

        self.table_name = table_name
        self.database_name = database_name
        self.user_action = user_action
        self.entity_object = EntityControl(
            table_name, user_action).initialise_entity()
        self.persistance_object = PersistanceSingleKeyControl(
            database_name, table_name, user_action, self.entity_object)

    def __str__(self):
        """Return Attributes of EntityPersistanceSingleKeyControl as string for testing"""
        return (f"table_name: {self.table_name}, database_name: {self.database_name} " +
                f"user_action: {self.user_action}, entity_object: {self.entity_object}, " +
                f"persistence_object: {self.persistance_object}")

    def create_and_execute_query(self):
        """call perform_data_base_query() method to construct and execute query and
            return data from database execution as list, boolean or None where applicable"""
        return self.persistance_object.perform_database_query()


# -------------------------------------------------------------------------------------------------
class EntityControl:
    """Class controlling match of table_name to Entity Controller (books, employee, customer, etc)
        using 'user_action' description to determine CRUD instance class to use for user_input
         retrieval and return populated CRUD Class instance.

         Attributes:
         -----------
         table_name: str
            name of table that would exist in database
        user_action: str
            description of CRUD action to perform matching actions specified by desired entity class

        Methods:
        --------
        __init__(self, table_name, user_action):


        __str()__:
            return string of attributes 'field_name' and 'user_action' for class testing

        initialise_entity(self):
            use 'table_name' and 'user_action' to call relevant CRUD class and request user
            data necessary for database query construction for 'EntityPersistanceSingleKeyControl'
            class attribute 'persistance_object'
         """

    def __init__(self, table_name, user_action):
        """Constructor to initialise 'table_name' and desired CRUD user_action'."""
        self.table_name = table_name
        self.user_action = user_action

    def __str__(self):
        """Return attributes 'field_name' and 'user_action' for testing"""
        return f"table_name: {self.table_name}, user_action: {self.user_action}"

    def initialise_entity(self):
        """Initialise entity used for user_input retrieval according to desired
            table_name and user_action. Call Entity Controller Class to perform
            user_input request and validation.

            Attributes:
            ------------------
            table_name: str
                name of table that would exist in a database
            user_action: str
                description of action to be performed to retrieve data from 
                 a user such as 'Create Table'

            Return:
            --------
            entity_object: object
                object populated with required atttibutes according to desired action
                against database
            None: 
                returned if invalid 'user_action' has been specified or 'table_name' given
                does not have a matching Entity Controller class added for this function
            """
        # check table name for 'books' to call matching Entity Controller 'BookController'
        if self.table_name == "books":
            # Create instance of BookController class initialising with desired 'user_action'
            book_controller = book.BookController(self.user_action)
            # call BookController method to request and validate user_input and return
            # specific sub-class object based on 'user_action' description
            book_entity = book_controller.create_crud_instance()

            # check that valid 'user_action' had been given to print a log message to developer
            if book_entity is None:
                print(
                    "Error Log - Invalid crud action has been supplied to 'book' class")
            return book_entity
        else:
            # table_name provided does not have a matching Entity Controller Class
            print("Error Log - Table name has not been matched to entity in Module " +
                  "'business logic'")
            return None

# -------------------------------------------------------------------------------------------------


class PersistanceSingleKeyControl:
    """Class using Entity Object dependancy to retrieve correct data needed for query generation
        and execution against a database using 'persistence_classes_single_key' class.
        'perform_database_query()' uses 'user_action' attribute to determine correct query method to
        use and can ONLY be one of:
        "Create Default Table', 'Create Entity', 'Read Entity', 'Delete Entity', 'Update Entity'

    Attributes:
    -----------
    database_name: str
        name of database
    table_name: str
        name of table that should be (or created) in above database
    user_action: str
        description of user action needed for Entity and Persistance Control objects
        "Create Default Table', 'Create Entity', 'Read Entity', 'Delete Entity', 'Update Entity'
    entity_object: component object
        instance of class used to retrieve and store required use_input based on user_action

    Methods:
    --------

    __init__(self, database_name, table_name, user_action, entity_object):
        constructor to initialise attributes of 'PersistanceSingleKeyControl' class

    __str__(self):
        "Return Attributes of PersistanceControl Class as string for testing

    
    """

    def __init__(self, database_name, table_name, user_action, entity_object):
        """constructor to initialise attributes of 'PersistanceSingleKeyControl' class."""
        self.database_name = database_name
        self.table_name = table_name
        self.user_action = user_action
        self.entity_object = entity_object


    def __str__(self):
        """Return Attributes of PersistanceControl Class as string for testing."""
        return (f"database_name: {self.database_name}, table_name: {self.table_name}, " +
                f"user_action: {self.user_action}, entity_object: {self.entity_object}")


    def perform_database_query(self):
        """Determine correct action based on 'user_action' to call Entity Object methods to 
            retrieve and validate user_input. Format and pass data to Persistance Control class
            according to requirements and execute against a database.
            
            Return:
            -------
            Function may return None, a boolean value or a list of values depending on desired
            user_action and Entity Object
            """

        # confirm that an Entity Object has been created to have access to correct and relevant
        # instance attributes needed for query construction and execution
        if self.entity_object is None:
            print("Error Log - Entity Object not created")
            return

        else:
            # check if table already exists in database
            table_exists = persistence_classes_single_key.VerifyTable(
                self.database_name, self.table_name)

            # if application needs to create a Default Table
            if self.user_action == "Create Default Table":

                if table_exists:
                    # if table in database with same name already exists, do not create new table
                    print(f"Table {self.table_name} is working in database")
                else:
                    # Table may be created
                    # retrieve the table's primary key, int_list fields, text_list fields
                    # and float_list fields names from Entity Object
                    primary_key = self.entity_object.primary_key
                    int_fields = self.entity_object.int_list
                    text_fields = self.entity_object.text_list
                    float_fields = self.entity_object.float_list

                    # Create instance of 'CreateTableSingleKey' class which initialises and
                    # manages database connection. Call its 'execute()' method to create and execute
                    # query to create a new table with name 'table_name'
                    persistence_classes_single_key.CreateTableSingleKey(
                        self.database_name, self.table_name, primary_key,
                        int_fields, text_fields, float_fields).execute()

            # if user wishes to perform an action requiring a table to already exist in the database
            elif self.user_action != "Create Default Table":
                # before allowing read, update or deletion of data from database table,
                # confirm that table does exist in database:
                if table_exists is False:
                    print(
                        f"Error Log - {self.table_name} does not exist, cannot perform " +
                        "action on database")
                    return None

                else:
                    # table does exist and program may proceed with desired user action

                    if self.user_action == "Create Entity":
                        # retrieve potential int_list, text_list and float_list
                        # values (in that order) from entity object
                        int_values = self.entity_object.int_list_values
                        text_values = self.entity_object.text_list_values
                        float_values = self.entity_object.float_list_values

                        # retrieve name and type of primary_key field
                        primary_key_data = self.entity_object.primary_key_data
                        # retrieve primary_key field name
                        primary_key_name = primary_key_data[0]
                        # determine primary key type
                        primary_key_type = primary_key_data[1]
                        # if type is integer, retrieve last row from table to increment primary
                        # key value for new (current) row by 1
                        if primary_key_type == "int":
                            
                            # increment primary_key int value for current row by 1 from last in
                            # database table
                            row_primary_value = persistence_classes_single_key.ReturnLastId(
                                self.database_name, self.table_name, primary_key_name).execute()
                            row_primary_value += 1
                        
                        # primary key is not an integer (not recommended)
                        else:
                            # loop until user enters a non-empty value for primary_key
                            while True:
                                row_primary_value = input("\nPlease enter a unique identifier for new entity")
                                if row_primary_value != "":
                                    print("\nA value was not entered.")
                                    continue
                                else:
                                    break

                        # 'InsertData' Class requiress values to be in one tuple, stored in a list
                        # create tuple with primary_key value and all values retrieved from user as
                        # ints, strings or floats
                        values_tup = (row_primary_value, )
                        values_tup += tuple(int_values + text_values + float_values)
                        # convert tuple with values to list for correct passing to InsertData constructor
                        values_list = []
                        values_list.append(values_tup)
                        
                        # Create instance of 'CreateTableSingleKey' class which initialises and
                        # manages database connection. Call its 'execute()' method to create and execute
                        # query to create and add new row to table
                        # Function call returns True for more than one row affected or False for none affected
                        return persistence_classes_single_key.InsertData(
                            self.database_name, self.table_name, values_list).execute()
                        

