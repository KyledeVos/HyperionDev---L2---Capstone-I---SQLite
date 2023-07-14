"""
Module holding classes for user_input retrieval and validation for 'book' table
with a single primary key. Imports and use of this module Must be done through
control class 'BookController' with 'action' attribute to determine correct instance
of other classes to create and return. 

Valid BookController Arguments are:
"Create Default Table", "Create Book", "Search Book", "Update Book" and "Delete Book"

Function 'create_crud_instance()' must then be
called for correct class instance return for CRUD Operation

NOTE: Database logic and queries are not handled by classes within this module. All
classes return a populated instance to calling method or None. Database and table names are
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
            return BookSearch()


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
    --------
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


    def retrieve_numeric_value(self, data_type, input_message, error_message, value_range=None):
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
    """Request and validate user_input to initialise class instance with field_names and search
        values corresponding to a book search.

    "Attributes:
    ------------
    fields_list: string list (default = "*" for all fields)
        list containing field name values to return for search
    where_fields_list: string list
        list containing name of fields to perform search against
    search_values: list of type corresponding to desired search field
        list containing search values used when performing a book search in a database

    Methods:
    --------
    __init__(self):
        Constructor used to create class instance with attributes retrieved from user, using
        class method 'search_book' to  retrieve and set class instance attributes

    __str__(self):
        return string containing values for class attributes for testing

    search_book_single_field(self, int_list, text_list, float_list):
        retrieve and validate user inputs to determine desired fields and values used
        when performing book search. Method will instantiate class attributes. Returns
        None for invalid argmuments in method call.

    check_no_list_duplicates(self, int_list, text_list, float_list):
        Helper Function to check if list arguments contain any duplicated values between them
    """
    # name(s) of field values to return in database book search. Default has been set to "*"
    # to return all fields
    fields_list = "*"
    # field_names used to perform database book search
    where_fields_list = None
    # values corresponding to where_fields_list above
    search_values = None


    def __init__(self):
        """call 'search_book_single_field' method to request and validated user_input to populate
            class arguments 'where_fields_list' and 'search_values'. Return of None to constructor
            indicates incorrect arguments where given to 'search_book_single_field' method.
        """
        self.search_book_single_field(["id", "quantity"], ["author"], [])


    def __str__(self):
        """return class instance variables values for testing."""
        return (f"fields_list: {self.fields_list}, where_fields_list: {self.where_fields_list} " +
                f"search_vals = {self.search_values}")


    def search_book_single_field(self, int_list, text_list, float_list):
        """determine search criteria from user to perform a book(s) search. Method requests and
            validates one field_name and one corresponding search_value used for search in database.

        Keyword Arguments:
        ------------------
        int_list: string list (can be empty)
            names of fields corresponding to Integer values in a database
        text_list: string list (can be empty)
            names of fields corresponding to string (Text) values in a database
        float_list: string list (can be empty)
            names of fields corresponding to float (Real) values in a database
        NOTE: at least one list must be populated. For book implementation the 'id'
                primary key should be included in the 'int_list'

        Exceptions:
        -----------
        ValueError:
            occurs when user choice for option as integer is of incorrect type or
            user input for 'integer' or 'float' search value type is incorrect

        Return:
        -------
        None :
            occurs if function is called with no population of at least one list or
            there are duplicated values (field_names) in any of the lists
        """

        # boolean to terminate main loop once values for 'where_fields_list' and
        # 'search_vals' have been recieved and validated from user
        values_recieved = False
        while True:
            try:
                # Perform Initial Validation of arguments lists:
                # 1) Check function call has been made with at least one populated list
                if len(text_list) == 0 and len(int_list) == 0 and len(float_list) == 0:
                    print("\nError Log - At least one field has to be populated")
                    return None

                # 2) Confirm there are no duplicated values (field names) in any of the lists
                elif self.check_no_list_duplicates(int_list, text_list, float_list) is False:
                    print(
                        "/Error Log - There is a duplicated field name in one the lists")
                    return None

                # Lists are valid
                else:
                    # store total number of options to perform search by
                    search_count = 0
                    # dictionary to store option number (key) and list (value) of field
                    # name and origin list
                    search_option_field = {}

                    # print field_names as options to user to perform search
                    print(
                        "\nEnter the number option below for how you want to perform search")
                    # move through each list to print options together
                    for count, field_name in enumerate(int_list + text_list + float_list):
                        # print option number and field_name to user
                        print(f"{count} : {field_name}")

                        # determine list current field belongs to
                        if len(int_list) != 0 and count <= len(int_list) - 1:
                            search_option_field[count] = [
                                field_name, "int_list"]
                        # add length of previous int_list to account for total options summed
                        # together for all three lists
                        elif len(text_list) != 0 and count <= ((len(text_list) + len(int_list))-1):
                            search_option_field[count] = [
                                field_name, "text_list"]
                        # field not in int-list or text_list so must be in float_list
                        else:
                            search_option_field[count] = [
                                field_name, "float_list"]

                        # track total number of options given to user for validation below
                        search_count = count

                    # request input and attempt cast to int. Throws ValueError for character,
                    # empty input or invalid integer number
                    option_input = int(input("\nOption: "))

                    # check recieved int input is in range of options
                    if option_input < 0 or option_input > search_count:
                        print(
                            "\nInvalid. Please enter an option number within range of options")
                    else:
                        # set name of field in a database to be used for search
                        self.where_fields_list = [
                            search_option_field[option_input][0]]

                        # Request and validate user_input value for selected field above
                        # first list value in dict 'seach_option_value' holds field name
                        while True:
                            user_value = input("\nEnter a value for the book(s) " +
                                               f"{search_option_field[option_input][0]}: ")
                            # check for empty input
                            if user_value == "":
                                print("\nA value was not recieved")
                                continue

                            # perform check for correct type if field corresponds to an
                            # Integer or float (second value in list for dict 'search_option_value')
                            if search_option_field[option_input][1] == "int_list":
                                # check for an Integer Value
                                try:
                                    int(user_value)
                                except ValueError:
                                    print(
                                        "\nInvalid. Please enter a valid, non-decimal number")
                                    continue
                            elif search_option_field[option_input][1] == "float_list":
                                try:
                                    float(user_value)
                                except ValueError:
                                    print(
                                        "\nInvalid. Please enter a valid, numeric value")
                                    continue

                            # at this point, value has been recieved and validated from user
                            self.search_values = [user_value]
                            # terminate main_loop
                            values_recieved = True
                            break

                # check if 'where_fields_list' and 'search_vals' have been populated
                # to end main loop
                if values_recieved is True:
                    break

            except ValueError:
                print("\nPlease enter a valid number for your choice.")

    def check_no_list_duplicates(self, int_list, text_list, float_list):
        """Helper Function validating there are no duplicated values between or in
            the three lists. Lists may be empty.

        Keyword Arguments:
        ------------------
        int_list: list of strings
            names of fields that would hold integer values
        text_list: list of strings
            names of fields that would hold text (string) values
        float_list: list of strings
            names of fields that would hold real (float) values

        Return:
        -------
        True for no duplicates, False if duplicate value (field_name) is found
        """
        # combine all lists into single list
        combined_list = int_list + text_list + float_list
        # Perform check within combined list to check for any duplicates. As lists are
        # anticipated to be small, checking complexity for all three lists has been left as 0(n^2)
        for i in range(0, len(combined_list) - 1):
            for j in range(i + 1, len(combined_list)):
                if combined_list[i] == combined_list[j]:
                    return False

        # no duplicates were found
        return True
