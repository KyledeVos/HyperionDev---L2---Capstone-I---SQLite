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
        self.entity_object = EntityControl(table_name, user_action).initialise_entity()
        self.persistance_object = None
        
    def __str__(self):
            """"""
            return (f"table_name: {self.table_name}, database_name: {self.database_name} " +
                    f"user_action = {self.user_action}, entity_object: {self.entity_object}, " +
                    f"persistence_object: {self.persistance_object}")


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
                print("Error Log - Invalid crud action has been supplied to 'book' class")
            return book_entity
        else:
            # table_name provided does not have a matching Entity Controller Class
            print("Error Log - Table name has not been matched to entity in Module " +
                  "'business logic'")
            return None

                



