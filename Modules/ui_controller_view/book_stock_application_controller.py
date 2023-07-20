
from Modules.business_logic import entity_persistance_matcher_control


class BookStoreController:
    """"""

    def __init__(self, database_name, table_name, view_renderer):
        """Constructor to initialise Book Controller class with desired database and table names
            and view_render class
        """
        self.database_name = database_name
        self.table_name = table_name
        self.view_renderer = view_renderer

        # ensure table for book_clerk has been created and populated with fields
        self.create_default_table()

    def create_default_table(self):
        """use 'entity_persistance_matcher_control' instance to check for existing
            table and create new table if not present."""

        # table fields and types are set in Modules.busines_logic.book.FieldControl class
        # Attempt to Create table (if not present) before menu print to user
        # if table with matching table is found in database, new table creation is not attempted
        entity_control = entity_persistance_matcher_control.EntityPersistanceSingleKeyControl(
            self.database_name, self.table_name, "Create Default Table")
        # required execution method to perform query against database
        entity_control.create_and_execute_query()

    def application_run(self):
        """Method used to run book application."""

        # create and display application Main Title String
        title_string = "BOOK STOCK MANAGER"
        self.view_renderer.display_title(title_string)

        while True:
            # construct main menu string
            main_menu = ("\nPlease Select an option number below:\n" +
                         "1 - Enter Book\n2 - Update Book\n3 - Delete Book" +
                         "\n4 - Search Book\n5 - View All Books\n0 - Exit")
            # display menu to user
            self.view_renderer.display_sub_title("Main Menu")
            self.view_renderer.display_formatted_string(main_menu)

            # use viewrender to display input request and retrieve input as string
            try:
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
                    successful_creation = entity_persistance_matcher_control.\
                        EntityPersistanceSingleKeyControl(
                            self.database_name, self.table_name, "Create Entity").\
                        create_and_execute_query()

                    if successful_creation:
                        self.view_renderer.display_sub_title(
                            "New Book Added Successfully")
                    else:
                        self.view_renderer.display_sub_title(
                            "New Book was not created")

                # update book
                elif user_input == 2:
                    self.view_renderer.display_title("Book Update Menu")
                    successful_update = entity_persistance_matcher_control.\
                        EntityPersistanceSingleKeyControl(
                            self.database_name, self.table_name, "Update Entity").\
                        create_and_execute_query()

                    if successful_update:
                        self.view_renderer.display_sub_title(
                            "Book Update was Successful")
                    else:
                        self.view_renderer.display_sub_title(
                            "Book could not be updated")

                # delete book
                elif user_input == 3:
                    self.view_renderer.display_title("Book Deletion Menu")
                    successful_deletion = entity_persistance_matcher_control.\
                        EntityPersistanceSingleKeyControl(
                            self.database_name, self.table_name, "Delete Entity").\
                        create_and_execute_query()

                    if successful_deletion:
                        self.view_renderer.display_sub_title(
                            "Book has been deleted")
                    else:
                        self.view_renderer.display_sub_title(
                            "Book could not be deleted")

                # search book
                elif user_input == 4:
                    self.view_renderer.display_title("Book Search Menu")
                    search_books = entity_persistance_matcher_control.\
                        EntityPersistanceSingleKeyControl(
                            self.database_name, self.table_name, "Search Entity").\
                        create_and_execute_query()

                    if len(search_books) == 0:
                        self.view_renderer.display_formatted_string(
                            "No Books in Stock")
                    else:
                        self.view_renderer.display_sub_title("Search Results")
                        self.view_renderer.display_table_with_header(
                            search_books)

                # retrieve and display all books in database
                elif user_input == 5:
                    self.view_renderer.display_title("All Books")
                    all_books = entity_persistance_matcher_control.\
                        EntityPersistanceSingleKeyControl(
                            self.database_name, self.table_name, "Read All").\
                        create_and_execute_query()

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
