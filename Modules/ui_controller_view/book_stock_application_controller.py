
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
                         "4 - Search Book\n 5- View All Books\n 0 - Exit")
            # display menu to user
            self.view_renderer.display_sub_title("Main Menu")
            self.view_renderer.display_formatted_string(main_menu)

            break
