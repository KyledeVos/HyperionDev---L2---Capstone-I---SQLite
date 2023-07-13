"""
Module holding classes for user_input retrieval and validation for 'book' table
with a single primary key. Imports and use of this module Must be done through
control class 'BookController' with 'action' attribute to determine correct instance
of other classes to create and return. Function 'create_crud_instance()' must then be
called for correct class instance return for CRUD Operation

NOTE: Database logic and queries are not handled by classes within this module. All
classes return a populated instance to calling method. Database and table names are
not handled in this module
"""

class BookController:
    """Main class of Module used to determine which lower class instance to return
    based on 'book-action'

    Attributes:
    ------------
    book_action: String
        used to determine lower class instance to return. Values can only be one of:
        'Create Default Table', 'Create Book', 'Search Book', 'Update Book' and 'Delete Book'

    Methods:
    -----------
    __init__(self, book_action):
        initialise instance of BookController

    create_crud_instance(self):
        Compulsory method that must be called after initialisation of 'BookController'
        determine instance of lower class to instantiate and return based on
        attribute 'book_action'
    """

    def __init__(self, book_action):
        "Create instance of book controller defining CRUD operation as book-action."
        self.book_action = book_action
        

    def create_crud_instance(self):
        """uses 'book_action" to determine object to instantiate of lower classes."""

        # Create Default book table with fields as: 'id', 'title' 'author'
        # NOTE: Constructors for each class will call respective method to create
        #       required object instance
        if self.book_action == "Create Default Table":
            return CreateDefaultBookTable()
        elif self.book_action == "Create Book":
            return CreateBook()
        elif self.book_action == "Search Book":
            BookSearch()


class CreateDefaultBookTable:
    """Define instance default field values for 'books' table using single Primary Key
        field.

    Attributes:
    ------------
    primary_key: string
        name of primary key for default table generation as "id
    int_list: string list
        name of field (price) that would hold integers
    text_list: string list
        name of fields(title and author) that would hold strings

    Methods:
    ---------
    __init__(self):
        define instance for single primary-key default book table

    __str__(self):
        return string of class attributes for testing
    """

    def __init__(self):
        """Create instance of books table with default field names"""
        self.primary_key = "id"
        self.int_list = ["quantity"]
        self.text_list = ["title", "author"]

    def __str__(self):
        "return attributes of 'CreateDefaultBookTable' instance as string for testing"
        return (f"PK: {self.primary_key}, int_list names: {self.int_list}," +
                        f"test_list names: {self.text_list}")


class CreateBook:
    """Request and Validate User Input to create a 'Book' Object. 'id'
    for primary key in books table is not handled or added here.

    Attributes:
    ------------
    title: string
        name of book
    Author: string
        name of book author(s)
    quantity: int
        number of book copies currently in stock

    Methods:
    __init__(self):
        call respective methods to request and retrieve user_input for class attributes

    __str__(self):
        return string of class attributes for testing

    retrieve_string_value(self, input_message):
        request and validate user_input for a string (text) based attribute

    def retrieve_numeric_value(self, data_type, input_message, error_message, value_range = []):
        use parameters to request and validate user input for a numeric based attribute

    """

    def __init__(self):
        """Use class method calls (and their parameters) to request, retrieve and validate user
            input used to instantiate a new 'book' object

        Arguments:
        -----------
        title: string
            name of book
        Author: string
            name of book author(s)
        quantity: int
            number of book copies currently in stock
            """
        self.title = self.retrieve_string_value("Enter the Book Title")
        self.author = self.retrieve_string_value(
            "Enter the Author(s) of the Book")
        # parameters set as 'datatype' - Integer, 'message to user', list of error messages for
        # missing input, incorrect value-type entered or value out of 'value-range',
        # value_range- list containing a minimum of zero with no max value
        self.quantity = self.retrieve_numeric_value("Integer",
                                                    "Enter the number of copies in stock",
                                                    ["Please enter a valid, non-decimal stock number.",
                                                     "Value entered is smaller than allowed minimum",
                                                     "Value entered exceeds allowed maximum"],
                                                    [0])


    def __str__(self):
        "return attributes of 'CreateBook' instance as string for testing"
        return f"title: {self.title}, author: {self.author}, quantity: {self.quantity}"


    def retrieve_string_value(self, input_message):
        """Request, retrieve and validate user input for a string (text) attribute and return value.

        Arguments:
        ----------
        input_message: string
            message to display to user for input request

        Return: 
        ----------
        user_input: string
            retrived user input that is non-empty
        """
        while True:
            user_input = input(f"\n{input_message}: ")
            # check input was not empty
            if user_input == "":
                print("\nAn input was not recieved.")
            else:
                return user_input

    def retrieve_numeric_value(self, data_type, input_message, error_message, value_range = None):
        """Rquest, retrieve, validate and return user_input for a numeric value.
        
        Arguments:
        -----------
        data_type: string
            desired input type currently allowing only "Integer" and "Float"
        input_message: string
            message to display to user to request numeric input
        error_message: string list
            strings to display to user for value_error (incorrect type given) or value out of
            range as defined by 'value_range' with current order as:
                [0] - message for value_error (incorrect type)
                [1] - message for value lower than minimum (optional if lower min not specified)
                [2] - message for exceeding max value (optional is max not specified)
        value_range: int or float list: default = None
            list to specify min [0] or max [1] allowed user_input. Values are inclusive for range.
            Values must be defined to correct datatype being requested.
            Argument is optional and can be one of three as:
            - None (ommited in function call) - no range is set
            - [min] - minimum allowed value
            - [min, max] - specify a min and max allowed values
        NOTE: 'value_range' must be checked against 'error_message' list

        Exceptions:
        -----------
        ValueError:
            caused by user entering a value not corresponding to 'data_type'

        Return: 
        ----------
        numeric_value: matching 'data_type' attribute (Currently only int or float)
            retrieved and validated user_input for numeric value
        """
        while True:
            # attempt to retrieve user_input corresponding to 'data_type' attribute
            try:
                # print message to user and cast to desired numeric data_type, throws
                # ValueError if incorrect type is not received.
                if data_type == "Integer":
                    numeric_value = int(input(f"\n{input_message}: "))
                elif data_type == "Float":
                    numeric_value = float(input(f"\n{input_message}: "))
                else:
                    # function has been called with a value not capable of handling
                    print(
                        "\nError Log - Function cannot handle number data type in call" +  
                        " for book creation")
                    # message intended for developer
                    return None

                # perform check for retrieved user_input against allowed value_range
                # check if range was specified
                if value_range is not None:
                    # perform minimum value check
                    if numeric_value < value_range[0]:
                        print(f"\n{error_message[1]}")
                        continue
                    # perform maximum value check (if supplied in function call)
                    if len(value_range) == 2:
                        if numeric_value > value_range[1]:
                            print(f"\n{error_message[2]}")
                            continue
                # return validated user_input
                return numeric_value

            except ValueError:
                print(f"\n{error_message[0]}")

class BookSearch:
    """
    """
    fields_list = None
    where_fields_list = None
    search_values = None

    def __init__(self):
        self.search_book( ["id", "quantity"], ["title", "author"],)


    def search_book(self, int_list = [], text_list = [], float_list = []):
        # add - int_list should have primary key field listed first for book_id
        
        while True:
            try:
                # function call has not provided at least one field_list for search
                if len(text_list) == 0 and len(int_list) == 0 and len(float_list) == 0:
                    print("\nError Log - At least one field has to be stated")
                    return

                else:
                    # store total number of options to perform search by
                    search_count = 0
                    # dictionary storing option number and field name
                    search_option_field = {}

                    # print field_names as options to user to perform search
                    print("\nEnter the number option below for how you want to perform search")
                    # move through each list to print options together
                    for count, field_name in enumerate(int_list + text_list + float_list):
                        print(f"{count} : {field_name}")
                        search_option_field[count] = field_name
                        search_count = count
                    # request input and attempt cast to int. Throws ValueError for character,
                    # empty input or invalid integer numer
                    user_input = int(input("\nOption: "))
                    
                    # check recieved int input is in range of options
                    if user_input < 0 or user_input > search_count:
                        print("\nInvalid. Please enter an option number within the range of options")
                    
                    # determine which list option corresponds to print correct input request message
                    else:
                        # # 1) check int_list
                        if len(int_list) > 0:
                            if user_input <= len(int_list):
                                search_field = int_list[user_input]
                        # 2) check text_list
                        if search_field == "":
                            if 
                        check 
                        print("seccuess")
                        break

            

            

                


            except ValueError:
                print("\nPlease enter a valid number for your choice.")

    

    

