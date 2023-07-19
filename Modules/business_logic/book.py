"""
Module holding classes for user_input retrieval and validation for 'book' table
with a single primary key. Module has individual classes to handle CRUD operation data
retrieval. Imports and use of this module MUST be done as:

1) Use of Component class 'FieldControl' to set primary_field name and other
    field names and types. This component Class and all other Composite classes
    only allow for types as 'Integer', 'String' and 'Float'. Fields are set within 
    constructor and class instance should not be created seperate from this module.

2) Control class 'BookController' with 'action' attribute to determine correct instance
    of other classes to create and return. 
    Valid BookController Arguments are:
    "Create Default Table", "Create Entity", "Search Entity" or 'Read Entity' or "Read All",
        "Update Entity" and "Delete Entity"

3) Function 'create_crud_instance()' in BookController MUST then be called for correct class
    instance return for CRUD Operation

NOTE: Database logic and queries are not handled by classes within this module. All
classes return a populated instance to calling method or None. 

The order of Fields (which should be extended to the Database by any class utilising this module) is:
Primary_Key
Integer_Values
Text_Values
Float_Values

Values within each category would be ordered sequentially

Classes designed with high consideration of Single Responsibility and Open-Closed Principles.
"""

class FieldControl():
    """A component used to set and control the names and types of fields that would be present in
        a database. Additional value_range attributes are added for Integer and Float fields.

    Attributes:
    -----------
    primary_key: tuple
        contains a single-field primary key name and its associated type
    int_list: list of tuple(s)
        list containing tuples ordered as:
        field_name, data_type as int, lower_range(inclusive), upper_range(inclusive)
        lower_range and upper_range may be set as None (not empty)
    text_list: list of tuple(s)
        list containing tuples of field names and their type as text (String)
    float_list: list of tuple(s)
        list containing tuples ordered as:
        field_name, data_type as float, lower_range(inclusive), upper_range(inclusive)
        lower_range and upper_range may be set as None (not empty)
    int_field_names: string list
        list containing field_names populated from 'int_list'
    text_field_names: string list
        list containing field_names populated from 'text_list'
    float_field_names: string list
        list containing field_names populated from 'float_list'

    Methods:
    -------
    __init__(self):
        used to initialise component and set primary_key, field names and their associated types

    __str__(self):
        print all declared field_names and types for testing

    primary_key_field_getter(self):
        Getter to return primary_key field_name

    __return_field_names(self, field_list):
        'private', helper method to return the names of fields from a list of tuples with first value
        in tuple equal to field name

    __check_no_list_duplicates(self, check_list):
        'private', helper method to check for any duplicates in check_list
    """

    def __init__(self):
        """Constructor to set primary_key, field names, associated types and possible value range.
            Tuples MUST have first two values as 'field_name' and 'data_type'. Integer and Float Lists
            must have third and fourth values as min and max for range checks (use None if not applicable).
        """
        self.primary_key = ("id", "int")
        # set int value of 'quantity' to have a lower, inclusive limit of zero and no preset upper limit.
        self.int_list = [("qty", "int", 0, None)]
        self.text_list = [("author", "text"), ("title", "text")]
        self.float_list = []

        # attributes storing only the names of the fields (no other data as in tuples above)
        self.int_field_names = self.__return_field_names(self.int_list)
        self.text_field_names = self.__return_field_names(self.text_list)
        self.float_field_names = self.__return_field_names(self.float_list)

        # perform check that primary_key tuple has been populated
        if not self.primary_key:
            print("Error Log - A Primary Key has not been stated for 'Book' Entity")

        # perform check that at least one field list has been populated
        if not self.int_list and not self.text_list and not self.float_list:
            print(
                "Error Log - At least one additional field has not been stated for 'Book' Entity")

        # perform check that field names in and between each list is unique
        if not self.__no_duplicates_tuple_lists(self.int_list, self.text_list, self.float_list):
            print("Error Log - A duplicated field name has been stated.")

    def __str__(self):
        """return attributes of 'FieldControl' instance as string for testing"""
        return (f"PK: {self.primary_key}, Integer_List: {self.int_list}, " +
                f"Text_List: {self.text_list}, Float_List: {self.float_list}, " +
                f"int_fields: {self.int_field_names}, text_fields: {self.text_field_names}, " +
                f"float_fields: {self.float_field_names}")

    def __return_field_names(self, field_list):
        """Internal, Helper Function that may be called by another class to retrieve the names of
            fields contained with class atrribute lists of tuples

        Keyword Arguments:
        -----------
        field_list: list of tuples
            list containing tuples that MUST conform to tuple[0] = field_name as string

        Return:
        ---------
        list containing the names of fields from 'field_list' (may return empty list)
        """
        return [tup[0] for tup in field_list]

    def __no_duplicates_tuple_lists(self, *tuple_lists):
        """Internal, Helper Function validating there are no duplicated values in a list.

        Keyword Arguments:
        ------------------
        tuple_lists: varying number of lists containing tuples
            list(s) containing values to be checked for any duplicates
            Tuples must correspond to at least one value with first value to be checked

        Return:
        -------
        True for no duplicates, False if duplicate value (field_name) is found
        """
        # list to contain combined, first_values in tuple
        combined_list = []
        # combine tuple_lists into list containing only first value in each tuple
        # data_list = each list of tuples in method arguments, tup = tuples contained in each list
        for data_list in tuple_lists:
            for tup in data_list:
                combined_list.append(tup[0])

        # Perform check within combined list to check for any duplicates. As implementation
        # is anticipated to be used for field lists with an assumed small count, complexity
        # has been left as 0(n^2)
        for i in range(0, len(combined_list) - 1):
            for j in range(i + 1, len(combined_list)):
                # compare current (i) in list to next (j) to check for match
                if combined_list[i] == combined_list[j]:
                    # duplicate found
                    return False

        # no duplicates were found
        return True


# -------------------------------------------------------------------------------------------------
class BookController:
    """Main class of Module used to determine which lower class instance to return
    based on 'book-action'

    Attributes:
    ------------
    book_action: String
        used to determine lower class instance to return. Values can only be one of:
        'Create Default Table', 'Create Entity', 'Search Entity' or 'Read Entity' or 
        'Read All', 'Update Entity' and 'Delete Entity'

    Methods:
    -----------
    __init__(self, book_action):
        initialise instance of BookController

    create_crud_instance(self):
        Compulsory method that must be called after initialisation of 'BookController'
        determine instance of lower class to instantiate and return based on
        attribute 'book_action' Returns none for 'book_action' not matching:
        'Create Default Table', 'Create Entity', 'Search Entity' or 'Read Entity' or 'Read All',
        'Update Entity' and 'Delete Entity'
    """

    def __init__(self, book_action):
        "Create instance of BookController with book action attribute."
        self.book_action = book_action

    def create_crud_instance(self):
        """uses 'book_action" to determine object to instantiate of lower classes.
        NOTE: Constructors for each class will call respective method to create
              required object instance
        """
        if self.book_action == "Create Default Table":
            return CreateDefaultBookTable()
        elif self.book_action == "Create Entity":
            return CreateBook()
        elif self.book_action == "Search Entity" or self.book_action == "Read Entity" or self.book_action == "Read All":
            return BookSearch(self.book_action)
        elif self.book_action == "Update Entity":
            return BookUpdate()
        elif self.book_action == "Delete Entity":
            return BookDelete()
        else:
            print("Error Log - Invalid Book Action has been entered for BookController")
            return None


# -------------------------------------------------------------------------------------------------
class CreateDefaultBookTable:
    """Define instance default field values for 'books' table using single Primary Key
        field.

    Attributes:
    ------------
    field_control: FieldControl
        component holding primary_key field, other field names and associated types
    primary_key: string
        name of primary key for default table generation
    int_list: string list
        name of field(s) that would hold integer(s)
    text_list: string list
        name of field(s) that would hold string(s)
    float_list: string list
        name of field(s) that would hold float(s)

    Methods:
    ---------
    __init__(self):
        define instance for single primary-key default book table using component
        FieldControl instance for field_names and types

    __str__(self):
        return string of class attributes for testing
    """

    def __init__(self):
        """Create instance of books table with default field names"""
        self.field_control = FieldControl()
        # set name of primary key
        self.primary_key = self.field_control.primary_key[0]
        # use field_control to retrieve and set lists containing int, text and float field names
        self.int_list = self.field_control.int_field_names
        self.text_list = self.field_control.text_field_names
        self.float_list = self.field_control.float_field_names

    def __str__(self):
        "return attributes of 'CreateDefaultBookTable' instance as string for testing"
        return (f"PK: {self.primary_key}, int_list names: {self.int_list}," +
                f"test_list names: {self.text_list}, float_list names: {self.float_list}")


# -------------------------------------------------------------------------------------------------
class CreateBook:
    """Request and Validate User Input to create a 'Book' Object. 'id'
    for primary key in books table is not handled or added here or in this module.

    Attributes:
    ------------
    field_control: FieldControl
        component holding primary_key field, other field names and associated types
    int_list_values: list of Integer Values
        values corresponding to each field in field_control int_list
    text_list_values: list of String Values
        values corresponding to each field in field_control text_list
    float_list_values: list of Float Values
        values corresponding to each field in field_control float_list

    Methods:
    --------
    __init__(self):
        call respective methods to request and retrieve user_input for class attributes

    __str__(self):
        return string of class attributes for testing

    retrieve_string_value(self, input_field):
        request and validate user_input for a string (text) based attribute

    def retrieve_numeric_value(self, data_type, input_field, error_message, value_range=None):
        use parameters to request and validate user input for a numeric based attribute
    """

    def __init__(self):
        """Use class method calls (and their parameters) to request, retrieve and validate user
            input used to instantiate a new 'CreateBook' object

        Attributes:
        -----------
        field_control: FieldControl
            component holding primary_key field, other field names and associated types
        primary_key_field: str
            holds name of primary key (for use in persistance class)
        int_list_values: list of Integer Values
            values corresponding to each field in field_control int_list
        text_list_values: list of String Values
            values corresponding to each field in field_control text_list
        float_list_values: list of Float Values
            values corresponding to each field in field_control float_list
        """
        self.field_control = FieldControl()
        self.primary_key_data = self.field_control.primary_key
        self.int_list_values = []
        self.text_list_values = []
        self.float_list_values = []

        # retrieve and validate string (text) values from user according to field
        # names in field_control for text_list:
        for text_field in self.field_control.text_list:
            # call retrieve_string_value() method to request user input and validate non-empty
            self.text_list_values.append(
                self.retrieve_string_value(text_field[0]))

        # retrieve and validate int values from user according to field_names
        # in field_control for int_list.
        for int_field in self.field_control.int_list:
            # call retrieve_numeric_value() to request user input and validate input
            # is of correct type and within possible numeric range
            self.int_list_values.append(
                self.retrieve_numeric_value("int", int_field[0],
                                            ["Please enter a valid, non-decimal number.",
                                            "Value entered is smaller than allowed minimum",
                                             "Value entered exceeds allowed maximum"],
                                            [int_field[2], int_field[3]]
                                            ))

        # retrieve and validate float values from user according to field_names
        # in field_control for float_list.
        for float_field in self.field_control.float_list:
            # call retrieve_numeric_value() to request user input and validate input
            # is of correct type and within possible numeric range
            self.float_list_values.append(
                self.retrieve_numeric_value("float", float_field[0],
                                            ["Please enter a valid number.",
                                            "Value entered is smaller than allowed minimum",
                                             "Value entered exceeds allowed maximum"],
                                            [float_field[2], float_field[3]]
                                            ))

    def __str__(self):
        "return list attributes of 'CreateBook' instance as string for testing"
        return (f"int_fields: {self.int_list_values}, text_values: {self.text_list_values}, " +
                f"float_values: {self.float_list_values}")

    def retrieve_string_value(self, input_field):
        """Request, retrieve and validate user input for a string (text) attribute and return value.

        Arguments:
        ----------
        input_field: string
            name of field for which a value is being requested

        Return: 
        ----------
        user_input: string
            retrieved user input that is non-empty
        """
        while True:
            user_input = input(f"\nEnter the book's {input_field}: ")
            # check input was not empty
            if user_input == "":
                print("\nAn input was not recieved.")
            else:
                return user_input

    def retrieve_numeric_value(self, data_type, input_field, error_message, value_range=None):
        """Rquest, retrieve, validate and return user_input for a numeric value.

        Arguments:
        -----------
        data_type: string
            desired input type currently allowing only "int" and "float"
        input_field: string
            name of field that would hold a numeric value currently being requested
        error_message: string list
            strings to display to user for value_error (incorrect type given) or value out of
            range as defined by 'value_range' with current order as:
                [0] - message for value_error (incorrect type)
                [1] - message for value lower than minimum (optional if lower min not specified)
                [2] - message for exceeding max value (optional if max not specified)
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
            caused by user entering a value not corresponding to 'data_type' for
            int of float

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
                if data_type == "int":
                    numeric_value = int(
                        input(f"\nPlease enter the book's {input_field}: "))
                elif data_type == "float":
                    numeric_value = float(
                        input(f"\nPlease enter the book's {input_field}: "))
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
                    if value_range[0] is not None:
                        if numeric_value < value_range[0]:
                            print(f"\n{error_message[1]}")
                            continue
                    # perform maximum value check (if supplied in function call)
                    if value_range[1] is not None:
                        if numeric_value > value_range[1]:
                            print(f"\n{error_message[2]}")
                            continue
                # return validated user_input
                return numeric_value

            except ValueError:
                print(f"\n{error_message[0]}")


# -------------------------------------------------------------------------------------------------
class BookSearch:
    """Request and validate user_input to initialise class instance with field_names and search
        values corresponding to a book search.
        NOTE: whilst the database query executions may still execute even with invalid data_types
              or values out of a given range, validation was added (here and in field_control) to
              allow for potential restriction of search values adding to possible scalability of
              project in addition to maintaining control of data_types in application.

    "Attributes:
    ------------
    field_control: FieldControl
        component holding primary_key field, other field names and associated types
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
        class method 'search_book_single_field' to retrieve and set class instance attributes

    __str__(self):
        return string containing values for class attributes for testing

    search_book_single_field(self, int_list, text_list, float_list):
        retrieve and validate user inputs to determine desired fields and values used
        when performing book search. Method will instantiate class attributes. Returns
        None for invalid argmuments in method call.

    check_no_list_duplicates(self, int_list, text_list, float_list):
        Helper Function to check if list arguments contain any duplicated values between them
    """
    # name(s) of field values to return in database book search.
    fields_list = None
    # field_names used to perform database book search
    where_fields_list = None
    # values corresponding to where_fields_list above
    search_values = None

    def __init__(self, user_action):
        """call 'search_book_single_field' method to request and validated user_input to populate
            class arguments 'where_fields_list' and 'search_values'. Return of None to constructor
            indicates incorrect arguments where given to 'search_book_single_field' method.

        Attribute
        ---------
        user_action: str
            Description of user action to either allow user to enter book search parameters or 
            create required parameters to read all books
            Can only be "Read Book" or "Search Book" to perform book search
            or "Read All" to create required parameters to search for all books
        """
        self.field_control = FieldControl()
        if user_action == "Read Entity" or user_action == "Search Entity":
            # call 'search_book' with int, text and float field_names list from field_control
            self.search_book_single_field(self.field_control.int_list, self.field_control.text_list,
                                          self.field_control.float_list)
        elif user_action == "Read All":
            self.read_all_books()

    def __str__(self):
        """return class instance variables values for testing."""
        return (f"fields_list: {self.fields_list}, where_fields_list: {self.where_fields_list} " +
                f"search_vals = {self.search_values}")


    def read_all_books(self):
        """Populate fields list with '*' to return data from all fields in table."""
        self.fields_list = ["*"]
        self.where_fields_list = None
        self.search_values = None


    def search_book_single_field(self, int_list, text_list, float_list):
        """determine search criteria from user to perform a book(s) search. Method requests and
            validates one field_name and one corresponding search_value used for search in database.

        Keyword Arguments:
        ------------------
        int_list: list (can be empty)
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
                # set to return all fields as default
                self.fields_list = ["*"]

                # store total number of options to perform search by
                search_count = 0
                # dictionary to store option number (key) and list (value) of field
                # name and origin list
                search_option_field = {}

                # print field_names as options to user to perform search
                print(
                    "\nEnter the number option below for how you want to perform search")
                # move through each list to print options together
                for count, field_name in enumerate(self.field_control.int_field_names +
                                                   self.field_control.text_field_names +
                                                   self.field_control.float_field_names):
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

                        # Determine data_type by matching user option selection to tuple lists
                        # in field control
                        # second value in list for dict 'search_option_value' holds data_type
                        if search_option_field[option_input][1] == "int_list":
                            # variable to store matching int tuple containing possible allowed
                            # value rangeS
                            int_tup = ()
                            # Retrieve possible allowed value range from field_control,
                            # by iterating through all tuples trying to match field names
                            for tup in self.field_control.int_list:
                                # tup[0] = field_name
                                if search_option_field[option_input][0] == tup[0]:
                                    int_tup = tup

                            # check value is integer and within allowed value range
                            try:
                                # check if user_value is less than allowed minimum value
                                # tup[2] holds minimum value (or None)
                                if int_tup[2] is not None:
                                    if int(user_value) < int_tup[2]:
                                        print(
                                            "\nValue entered is below allowed minimum of: " +
                                            f"{int_tup[2]}")
                                        continue
                                # check if user_value is above allowed maximim value
                                # tup[3] holds maximum value (or None)
                                if int_tup[3] is not None:
                                    if int(user_value) > int_tup[3]:
                                        print(
                                            "\nValue entered is above allowed maximum of: " +
                                            f"{int_tup[3]}")
                                        continue

                                # if value_range was not set, attempt conversion to int to check
                                # if valid data_type was entered
                                if int_tup[2] is None and int_tup[3] is None:
                                    int(user_value)

                            except ValueError:
                                print(
                                    "\nInvalid. Please enter a valid, non-decimal number")
                                continue

                        # perform check for correct type if field corresponds to a float
                        # (second value in list for dict 'search_option_value')
                        elif search_option_field[option_input][1] == "float_list":
                            # store matching float tuple containing possible allowed value ranges
                            float_tup = ()
                            # Retrieve possible allowed value range from field_control,
                            # by iterating through all tuples trying to match field names
                            for tup in self.field_control.float_list:
                                # tup[0] = field_name
                                if search_option_field[option_input][0] == tup[0]:
                                    float_tup = tup

                            # check value is valid float and within allowed value range
                            try:
                                # check if user_value is less than allowed minimum value
                                if float_tup[2] is not None:
                                    if float(user_value) < float_tup[2]:
                                        print(
                                            "\nValue entered is below allowed minimum of: " +
                                            f"{float_tup[2]}")
                                        continue
                                # check if user_value is above allowed maximim value
                                if float_tup[3] is not None:
                                    if float(user_value) > float_tup[3]:
                                        print(
                                            "\nValue entered is above allowed maximum of: " +
                                            f"{float_tup[3]}")
                                        continue

                                # if value_range was not set, attempt conversion to float to check
                                # valid data type was entered
                                if float_tup[2] is None and float_tup[3] is None:
                                    float(user_value)

                            except ValueError:
                                print(
                                    "\nInvalid. Please enter a valid number")
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

            # Exception caused by user entering option number that is not an integer
            except ValueError:
                print("\nPlease enter a valid number for your choice.")


# -------------------------------------------------------------------------------------------------
class BookUpdate:
    """Retrieve desired user field and associated value to perform update to field. Update is only
        performed using primary key for 'book' entity.

        Attributes:
        -----------
        field_control: FieldControl
            component holding primary_key field, other field names and associated types
        field_names: string_list
            holds (in order) name of field to be updated and name of primary_key field
        update_tuple: tuple
            holds (in order) new value for field to be updated and primary key value
            where update should be performed

        Methods:
        --------
        __init__(self):
            initialise attributes of BookUpdate instance and call 'update_book_single_field()'
            to retrieve and validate user_inputs for update

        __str__(self):
            testing method to print values in 'field_names' and 'update_tuple' attributes

        update_book_single_field(self):
            request, retrieve and validate user_input for desired field and value for update
            of book entity

        Exceptions:
        -----------
        Value_Error:
            raised if user enters a value not correspoding to required 'int' or 'float' types
        """

    def __init__(self):
        """Constructor to initialise field_control component controlling field names, types and 
        ranges (for numeric fields). Calls 'update_book_single_field()' method to retrieve and validate 
        user inputs used to set class attributes.

        Attributes:
        -----------
        field_control: FieldControl
            component holding primary_key field, other field names and associated types
        field_names: string_list
            holds (in order) name of field to be updated and name of primary_key field
        update_tuple: tuple
            holds (in order) new value for field to be updated and primary key value
            where update should be performed
        """
        self.field_control = FieldControl()
        self.field_names = []
        self.update_tuple = []
        # call 'update_book_single_field()' to initialise attributes with user inputs
        self.update_book_single_field()

    def __str__(self):
        """Return attributes 'field_name' and 'update_tuple' values for testing."""
        return f"field_names_list: {self.field_names}, update_tuple: {self.update_tuple}"

    def update_book_single_field(self):
        """Method to request, retrieve and validate user_input for data to be used for a 'book'
        entity update.
        """

        # retrieve data_type of primary key used for book update
        primary_key_type = self.field_control.primary_key[1]

        # Request and validate user_input for primary_key value used for book update
        while True:
            # request user_input for primary key
            # field_control.primary_key[0] = field_name of primary key
            primary_search_value = input("\nPlease enter the book " +
                                         f"{self.field_control.primary_key[0]} for update: ")

            # check for empty input
            if primary_search_value == "":
                print(
                    f"\nA {self.field_control.primary_key[0]} was not entered.")
                continue

            # perform check for primary key input value as 'int' type
            if primary_key_type == "int":
                # attempt cast of user input for primary key to int:
                try:
                    int(primary_search_value)
                except ValueError:
                    print("\nPlease enter a valid, non-decimal number")
                    continue

            elif primary_key_type == "float":
                # attempt cast of user input for primary_key to float:
                try:
                    float(primary_search_value)
                except ValueError:
                    print("\nPlease enter a valid number")
                    continue

            # at this point primary key is of valid type, end loop
            break

        # combine tuple lists in field_control into single list containing all tuples
        # all tuples hold: 'field_name', 'data_type'
        # tuples for numeric lists also hold: 'min_value' and 'max-value' - both may be None
        fields_combined = []
        fields_combined.extend(self.field_control.int_list)
        fields_combined.extend(self.field_control.text_list)
        fields_combined.extend(self.field_control.float_list)

        # dictonary to hold all field_tuples with an index number acting as the key
        field_tuple_dict = {}

        # add combined_list tuples into dictionary with an index number
        for count, tuple_val in enumerate(fields_combined):
            field_tuple_dict[count] = tuple_val

        # Request and Validate user input for desired field whose value should be updated
        while True:
            try:
                # hold total number of field options for range validation
                total_options = 0

                print(
                    "\nPlease select an option for the book category you would like to update:")
                # print field options to user to select from - for field to update
                # for each tuple contained in the combined field_lists
                for field_tuple in fields_combined:
                    # print option number and field_name
                    print(f"{total_options}: {field_tuple[0]}")
                    total_options += 1
                # request user_input option and validate as integer
                user_option = int(input("Selected Option: "))

                # check that user input is within range of total fields available
                if user_option < 0 or user_option > total_options - 1:
                    print(
                        f"\nThere is no matching option for number: {user_option}")
                    continue

                # user has entered valid integer within range of options, end loop
                break

            except ValueError:
                print("\nInvalid Option. Please enter a valid option number.")

        # add selected field_from user_option selection to 'field_names' attribute
        self.field_names.append(field_tuple_dict[user_option][0])

        # set data type for user chosen field to update
        update_value_field = field_tuple_dict[user_option][1]

        # request and retrieve user input for new value to be used for 'book' update
        while True:
            new_value = input(
                f"\nEnter a new value for {self.field_names[0]}: ")

            if new_value == "":
                print("\nA new value was not entered")
                continue

            # perform check for 'int' data_type (if field is an Integer)
            if update_value_field == "int":
                try:
                    # check value not below possible minimum allowed value
                    if field_tuple_dict[user_option][2] is not None:
                        if int(new_value) < field_tuple_dict[user_option][2]:
                            print("\nValue entered is below allowed minimum of " +
                                  f"{field_tuple_dict[user_option][2]}")
                            continue

                    # check value is not above possible allowed maximum
                    if field_tuple_dict[user_option][3] is not None:
                        if int(new_value) > field_tuple_dict[user_option][3]:
                            print("\nValue entered is above allowed maximum of " +
                                  f"{field_tuple_dict[user_option][3]}")
                            continue

                    # check value is an Integer if no value range was specified
                    if field_tuple_dict[user_option][2] is None and \
                            field_tuple_dict[user_option][3] is None:
                        # cast input to int to confirm valid data_type
                        int(new_value)

                # error caused by user entering character or non-decimal number
                except ValueError:
                    print("\nPlease enter a valid, non-decimal number")
                    continue

            # perform check for 'float' data_type (if field is a Float)
            if update_value_field == "float":
                try:
                    # check value not below possible minimum allowed value
                    if field_tuple_dict[user_option][2] is not None:
                        if float(new_value) < field_tuple_dict[user_option][2]:
                            print("\nValue entered is below allowed minimum of " +
                                  f"{field_tuple_dict[user_option][2]}")
                            continue

                    # check value is not above possible allowed maximum
                    if field_tuple_dict[user_option][3] is not None:
                        if float(new_value) > field_tuple_dict[user_option][3]:
                            print("\nValue entered is above allowed maximum of " +
                                  f"{field_tuple_dict[user_option][3]}")
                            continue

                    # check value is a Float if no value range was specified
                    if field_tuple_dict[user_option][2] is None and \
                            field_tuple_dict[user_option][3] is None:
                        # cast input to int to confirm valid data_type
                        float(new_value)

                # error caused by user entering character
                except ValueError:
                    print("\nPlease enter a valid number")
                    continue

            # at this point, user has entered a valid value for update field, end loop
            break

        # add new value for update to attribute 'update_tuple'
        self.update_tuple.append(new_value)
        # add id number of book to be updated to attribute 'update_tuple'
        self.update_tuple.append(primary_search_value)
        # compulsory means of seach is by primary key only.
        # add primary key field_name to attribute 'field_names'
        self.field_names.append(self.field_control.primary_key[0])


# -------------------------------------------------------------------------------------------------
class BookDelete:
    """Retrieve primary_key field name from field_controller, request and retrieve associated value
        for primary_key matching data_type.

        Attributes:
        -----------
        field_control: FieldControl
            component holding primary_key field, other field names and associated types
        primary_key_field: str
            name of primary_key_field
        primary_value: type controlled by FieldControl (int, string or float)
            value for primary_key corresponding to desired row to be deleted

        Methods:
        --------
        __init__(self):
            initialise attributes of BookDelete instance

        __str__(self):
            testing method to print values in 'primary_key_field' and 'primary_value' attributes

        retrieve_deletion_value(self):
            request, retrieve and validate user_input for primary_key to perform row deletion
            in a database

        Exceptions:
        -----------
        Value_Error:
            raised if user enters a primary_key value not correspoding to required
            'int' or 'float' types
        """

    def __init__(self):
        """Constructor to initialise BookDelete instance.

        Attributes:
        -----------
        field_control: FieldControl
            component holding primary_key field, other field names and associated types
        primary_key_field: str
            name of primary_key_field
        primary_value: type controlled by FieldControl (int, string or float)
            value for primary_key corresponding to desired row to be deleted
        """
        self.field_control = FieldControl()
        # set primary_key field name defined by primary_key in FieldControl Class
        self.primary_key_field = self.field_control.primary_key[0]
        # retrieve user input value for primary key
        self.primary_value = self.retrieve_deletion_value()

    def __str__(self):
        """Return values for primary key field and associated values for testing"""
        return (f"primary_key field: {self.primary_key_field}, " +
                f"primary_key_value: {self.primary_value}")

    def retrieve_deletion_value(self):
        """Request, retrieve and validate user_input for primary key for desired row (book)
            to delete.

        Return:
        -------
        primary_key value for row deletion (could be string, int or float)
        """
        # determine data_type for primary_key
        primary_key_type = self.field_control.primary_key[1]

        while True:
            # request user_input value for primary key
            user_input = input(
                f"\nPlease enter the row {self.primary_key_field} for deletion: ")

            # check for empty input
            if user_input == "":
                print("\nA value was not entered.")
                continue

            # check if primary_key type is Integer to validate
            if primary_key_type == "int":
                try:
                    # return value to be used for deletion of row
                    return int(user_input)
                except ValueError:
                    print("\nPlease Enter a valid, non-decimal number")
                    continue

            # check if primary_key type is Float to validate
            if primary_key_type == "float":
                try:
                    # return value to be used for deletion of row
                    return float(user_input)
                except ValueError:
                    print("\nPlease Enter a valid number")
                    continue
