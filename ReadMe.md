# Python Capstone Project I - Book Stock Management <br> Kyle de Vos - HyperionDev Student

# Description
The aim of this project was to model a Book Store Stock Management System for a book clerk including
the use of a sqlite3 database - allowing a user to perform CRUD operations against the database.

# Features
- Abstracted Database Connection and Query Execution
- Independant Modules allowing for application evolution
- Main Menu print to user for CRUD operations
- User input validation and error handling
- Allows user to create, modify, read and delete 'books' stored in database

# Software and Hardware

### Hardware
This project was developed on a Lenovo Ideapad 3 i5 Laptop running Windows 11<br>
11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz   2.42 GHz<br>
Display Resolution 1920 x 1080

### Software
This project was developed, tested and tracked using:
- Microsoft Visual Studio Code with sqlite3
- Microsoft Word (Software Documentation)
- https://app.diagrams.net/ for UML Diagram creations
- Git and GitHub

# Opening and Running of Project

Entire Project is located in current directory with "book_stock_management.py" file
acting as appplication launcher. Database 'ebookstore' has been created and populated
with 6 book entities for sample data. All other modules are contained in sub-directory
'Modules' and are further elaborated in "Project Classes and Behaivour Breakdown" section

1. Ensure 'tabulate' module has been installed and is on class path before run of
    application. Module needed for print of book data to console and application will
    crash if not present
2. Open project in VS code (or another preferred IDE)
3. Run application 'book_stock_management.py' to begin application
4. Application data and input requests are printed to console window
5. Main Menu will print, enter integer values for desired actions with 0 to end
    application run.

# Visuals

<h4>Fig 1. Main Menu Screenshot</h4>
<p><img src="./Software Documentation/Document_Images/Main_Menu_Screenshot.jpg" style="width: 60%">

<h4>Fig 2. Sample Books in Database Output (Tabular)</h4>
<p><img src="./Software Documentation/Document_Images/Read_All_Books_Screenshot.jpg" style="width: 60%">

# Program Architecture Summary

<h4>Fig 3. High Level System Architecture Overview</h4>
<p><img src="./Software Documentation/Document_Images/Architecture_Overview.jpg" style="width: 60%">

<h4>Fig 4. Main Classes with System Architecture</h4>
<p><img src="./Software Documentation/Document_Images/System_Architecture_Main_Classes.jpg" style="width: 60%">

# Project Classes and Behaivour Breakdown

<h4>Fig 5. Presentation Layer Class UML Diagram</h4>
<p><img src="./Software Documentation/Document_Images/Persistence_Layer_Class_UML_Diagram.jpg" style="width: 60%">

<h4>Fig 6. Business Logic - Entity-Persistence Match Control (Central Repository) Class UML Diagram</h4>
<p><img src="./Software Documentation/Document_Images/Central_Repository_Entity_Persistence_Match.jpg" style="width: 50%">

<h4>Fig 7. Business Logic - Book Controller with Entity Classes and Field Control Class UML Diagram</h4>
<p><img src="./Software Documentation/Document_Images/BookController_Class_UML_Diagram.jpg" style="width: 60%">

<h4>Fig 8. Persistence Layer - Persistence Classes Breakdown</h4>
<p><img src="./Software Documentation/Document_Images/Persistence_classes_UML_diagram.jpg" style="width: 60%">

## Classes Module References: 

### ui_controller_view.book_stock_application_controller:
- BookStockController

### ui_controller_view.view_render
- ConsoleViewRender

### business_logic.entity_persistance_matcher_control:
- EntityPersistanceSingleKeyControl
- EntityControl
- PersistanceSingleKeyControl

### business_logic.book
- FieldControl
- BookController
- CreateDefaultBookTable
- CreateBook
- BookSearch
- BookUpdate
- BookDelete

### persistance_layer.persistance_classes_single_key
- DatabaseController
- DatabaseQueryClass
- CreateTableSingleKey
- VerifyTable
- InsertData
- ReadData
- UpdateData
- DeleteData
- ReturnLastId

## Program Execution

1. 'book_stock_management.py' is run, initialising 'BookStoreController' class passing database name, table_name<br>
and desired View Renderer as 'ConsoleViewRenderer' (Fig 5.) <br>

2. Before print of Main Menu to user, 'BookStoreController' 'create_default_table()' method is called to check for<br>
existing table according to table name (Fig 5), and creates if not present.

    2.1 'EntityPersistanceSingleKeyControl' instance is initialised (Fig 6) passing instruction "Create Default Table".<br>
    During initialisation of 'EntityPersistanceControl' - 'EntityControl' instance is then initialised with immediate call<br>
    to 'initialise_entity()' method of 'EntityControl' class (Fig 6)

    2.2 With table_name = "books", EntityControl will set its 'book_controller' attribute in 'initialise_entity()' to 'BookController'<br>
        calling the 'BookController' constructor and executing its 'create_crud_instance()' method. (Fig 7)
        
    2.3 This method uses the instruction 'Create Default Table' to initialise and create the correct 'Entity' class which here would be<br>
    class 'CreateDefaultBookTable' (Fig 7). The constructor of 'CreateDefaultBookTable' will initialise an instance of class 'FieldControl<br>
    which houses the correct table primary_key and field names and types. 'CreateDefaultBookTable' will store all these attributes <br>
    from field control as its own

    2.4 Entity Control is now initialised with a populated book_entity class and is returned to 'EntityPersistanceSingleKeyControl'<br>

    2.5 'EntityPersistanceSingleKeyControl' will then initalise an instance of 'PersistanceSingleKeyControl' passing to it<br>
    the database and table name, instruction of "Create Default Table" and the initialised entity_object from 2.4 (Fig 6)<br>
    At this point initialisation of 'EntityPersistanceSingleKeyControl' instance is completed

    2.6. 'BookStoreController' will then call the 'create_and_execute_query()' method of 'EntityPersistanceSingleKeyControl'<br>
    (Fig 6). This method will call 'perform_database_query()' in 'PersistanceSingleKeyControl' class which will verify if the table<br>
    exists first, and then generate and create a query executed against the database based on the instuction received<br>
    (Create Default Table) (Fig 8).

        2.6.1 All classes used for query creation and execution are child classes of 'DataBaseQueryClass' which use helper class<br>
        'DatabaseController' to make a connection to a database and atempt to initialise 'connection' and 'cursor' objects. (Fig 8)<br>
        These objects are then used by the child classes of 'DatabaseController' for query execution.

        2.6.2 Values needed for query generation are retrieved from the instantiated entity-object (2.4)

        2.6.3 'DatabaseController' requests (and has been implemented) that all child classes use the method 'close_connection()' to<br>
            to close their connections to the database. 

    2.7 At this point a new table would have been created in the database. Program execution returns to 'book_stock_management.py'
    which calls 'BookStoreController' 'aaplication.run()' method which will print the Main Menu to user (using 'ConsoleViewRenderer')

    2.8 The Main Menu options (Fig 1) selected by a user will be executed in the same logical steps as those used above to create a<br>
    books table in the database. The different user_actions will change the entity_class (where user input is retrieved) that is initialised<br> and the child class of 'DatabaseController' that is instantiated and used to generate a query against the database.

# Future Development and Improvement

### Interface and View Rendering to User
The current View Renderer is set to only display content to the user through the terminal window. For this application's<br>
use in a book store it would be more user_friendly and enhance the UX to replace this with an HTML output or stand alone<br>
application display window with better features for input retrieval such as boxes, buttons, drop_down menus etc.

There are currently two groups of classes that perform printing to the console - "ConsoleViewRender" and the entity classes<br>
in the 'book' module. This is not ideal as all view rendering should be contained to one class or module for easy change or<br>
modification. Future Development would look to pass the 'view_renderer' to these entity_classes to allow them to display<br>
user input retrieval requests with the same view_renderer used to display the Main Menu

This standard of passing down the view_renderer through the applications execution should be implemented for any new entities added<br>
to this project and the view_renders themselves should follow strict and standard practices (function names, required data) to<br>
ensure they can be integrated easily into the growing application.

### Field Types and Quantity Evolution
The current FieldControl class does allow for additional fields to be added in this current application as long as they<br>
are of type Integer, String or Float and can be set to 'Non Null". Doing so should be done with a new table as this change<br>
will affect existing database table rows.

Whilst this does allow for easy growth of the application to hold more attributes of each 'book', it is limited in the sense
that other field data types have been excluded (such as dates). In addition, the current Entity classes and Persistance Control<br>
can only function with tables that use a non-compound primary key which would be problematic for larger tables.

This restricts the current application of the system to very small, non-complex entities. However, the modular design of the system<br>
does allow for each component in its Architecture to be re-used and can serve as a baseline for a new project to implement these<br>
more complex tables.

### New Entities and Persistance Controllers

The current application is shipped with a 'book' entity only and a non-compound primary-key persistance controller.<br>
Evolution of this application will likely include new entities such as Pricing, Profit or Finance capabilites, Customer<br>
and transactions tracking and Employee Data - all of which would be modeled as new Entities. Increasing the entities<br>
resulting in an increased table count and the use of foreign keys to link them together would likely require new <br>
Persistance Controllers to be created to handle them

The current Architecture can work for these new features and Entities, provided new Main Menu options are added and the<br>
Application Controllers are extended to handle these new capabilities.
