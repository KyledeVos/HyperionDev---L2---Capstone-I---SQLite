"""Application Controller Module used by application launcher 'book_stock_management'.
    Determine correct action from user and call 'entity_persistance_matcher_control'
    module classes to match Entity with Database Controller.

Classes:
--------
BookStoreController
    Match user action to Book Entity and Persistance Control Module calling
     viewrenderer only for Main Menu displays

    Exported Functions:
    -------------------
    __init__(database_name, table_name, view_renderer) -> None
        initialise BookController object

    application_run() -> None
        start application run

Components:
-----------
view_renderer: object
    instance controlling display of data, menus or information to user

entity_persistance_matcher_control: module
    contains classes to create a desired Entity matching user menu selection then
     matched to a Persistance Controller for database execution and data return

    Requirements:
    -------------
    Desired user_action must be passed as string, being only one of:
    'Create Default Table', 'Create Entity', 'Read Entity' or 'Search Entity' or
     'Read All', 'Update Entity', 'Delete Entity'
"""
from Modules.business_logic import entity_persistance_matcher_control

class BookStoreController:
    """Application Main controller determining desired user_action that is then
        passed to 'entity_persistance_matcher_control'. Data returned is formatted
        using view_renderer.

    Attributes:
    -----------
    - database_name: str
        name of database
    - table_name: str
        name of table in above database
    - view_renderer: object
        instance controlling display of data, menus or information to user
    - entity_persistance_matcher_control: module
        classes using user menu selection (formatted to action string) for
         entity creation and database execution

    Methods:
    --------
    __init__(self, database_name, table_name, view_renderer):
        create BookStoreController Instance

    create_default_table(self):
        use 'entity_persistance_matcher_control' instance to check for existing
         table and create new table if not present

    application_run(self):
        start application run, printing main menu and passing matching user selection
         to 'entity_persistance_matcher_control' component

    Exceptions:
    -----------
    ValueError:
        User main menu input does not of valid Integer type
    """

    def __init__(self, database_name, table_name, view_renderer):
        """Initialise class with database and table names and view_render class
            Check if desired table_name has been created.

        Arguments:
        ----------
        - database_name: str
            name of database
        - table_name: str
            name of table in above database
        - view_renderer: object
            instance controlling display of data, menus or information to user
        """
        self.database_name = database_name
        self.table_name = table_name
        self.view_renderer = view_renderer

        # ensure table for book_clerk has been created and populated with fields
        self.create_default_table()


    def create_default_table(self):
        """use 'entity_persistance_matcher_control' instance to check for existing
            table and create new table if not present.

        Call Restrictions:
        ------------------
        Function is called by BookStoreController, additional call should not be needed
        """

        # Check for table existance in database before main menu print to user,
        #  create table if not present
        entity_control = entity_persistance_matcher_control.EntityPersistanceSingleKeyControl(
            self.database_name, self.table_name, "Create Default Table")
        # required execution method to perform query against database
        entity_control.create_and_execute_query()


    def application_run(self):
        """Method used to run book application. Call is compulsory to start application."""

        # create and display application Main Title String
        self.view_renderer.display_title("BOOK STOCK MANAGER")

        while True:
            # construct main menu string
            main_menu = ("\nPlease Select an option number below:\n" +
                         "1 - Enter Book\n2 - Update Book\n3 - Delete Book" +
                         "\n4 - Search Book\n5 - View All Books\n0 - Exit")
            # display menu to user
            self.view_renderer.display_sub_title("Main Menu")
            self.view_renderer.display_formatted_string(main_menu)

            try:
                # use viewrender to display input request and retrieve input as string
                user_input = int(
                    self.view_renderer.input_request("\nSelected Option: "))

                # check user_input is within option range
                if user_input < 0 or user_input > 5:
                    self.view_renderer.display_formatted_string(
                        "\nPlease enter an option number between 0 and 5")
                    continue

                # determine if user wishes to end application
                if user_input == 0:
                    self.view_renderer.display_title("Application Closed")
                    break

                # create new book
                elif user_input == 1:
                    self.view_renderer.display_title("Create New Book")
                    # create Entity request for Book Creation and perform execution against
                    #  database. Returns boolean for affected rows greater than 0
                    successful_creation = entity_persistance_matcher_control.\
                        EntityPersistanceSingleKeyControl(
                            self.database_name, self.table_name, "Create Entity").\
                        create_and_execute_query()

                    # confirm to user if new book was added to database
                    if successful_creation:
                        self.view_renderer.display_sub_title(
                            "New Book Added Successfully")
                    else:
                        self.view_renderer.display_sub_title(
                            "New Book was not created")

                # update book
                elif user_input == 2:
                    self.view_renderer.display_title("Book Update Menu")
                    # create Entity request for Book Update and perform execution against
                    #  database. Returns boolean for affected rows greater than 0
                    successful_update = entity_persistance_matcher_control.\
                        EntityPersistanceSingleKeyControl(
                            self.database_name, self.table_name, "Update Entity").\
                        create_and_execute_query()

                    # confirm to user if update was successful
                    if successful_update:
                        self.view_renderer.display_sub_title(
                            "Book Update was Successful")
                    else:
                        self.view_renderer.display_sub_title(
                            "Book could not be updated")

                # delete book
                elif user_input == 3:
                    self.view_renderer.display_title("Book Deletion Menu")
                    # create Entity request for Book Deletion and perform execution against
                    #  database. Returns boolean for affected rows greater than 0
                    successful_deletion = entity_persistance_matcher_control.\
                        EntityPersistanceSingleKeyControl(
                            self.database_name, self.table_name, "Delete Entity").\
                        create_and_execute_query()

                    # confirm to user if deletion was successful
                    if successful_deletion:
                        self.view_renderer.display_sub_title(
                            "Book has been deleted")
                    else:
                        self.view_renderer.display_sub_title(
                            "Book could not be deleted")

                # search book
                elif user_input == 4:
                    self.view_renderer.display_title("Book Search Menu")
                    # create Entity request for individual Book Search and perform execution against
                    #  database.
                    #  Returns: Empty list for no match or list with field names and matching row(s)
                    search_books = entity_persistance_matcher_control.\
                        EntityPersistanceSingleKeyControl(
                            self.database_name, self.table_name, "Search Entity").\
                        create_and_execute_query()

                    # display matching book row(s) data or message for no match found
                    if len(search_books) == 0:
                        self.view_renderer.display_formatted_string(
                            "No Matching Books found")
                    else:
                        self.view_renderer.display_sub_title("Search Results")
                        self.view_renderer.display_table_with_header(
                            search_books)

                # retrieve and display all books in database
                elif user_input == 5:
                    self.view_renderer.display_title("All Books")
                    # create Entity request for All Books retrieval and perform execution against
                    #  database.
                    #  Returns: Empty list for no books or list with field names and all rows
                    all_books = entity_persistance_matcher_control.\
                        EntityPersistanceSingleKeyControl(
                            self.database_name, self.table_name, "Read All").\
                        create_and_execute_query()

                    # display data in all rows with field names or message for empty table
                    if len(all_books) == 0:
                        self.view_renderer.display_formatted_string(
                            "No Books in Stock")
                    else:
                        self.view_renderer.display_table_with_header(all_books)

            # user has given empty input, character or decimal number
            except ValueError:
                self.view_renderer.display_formatted_string(
                    "\nPlease enter a valid, non-decimal number")
                continue
