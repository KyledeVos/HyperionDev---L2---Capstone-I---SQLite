# Level 2 - Kyle de Vos (KD23040008523)
# L2T13 - Capstone Project I
# Date: 21 July 2023
# ____________________________________________________________
""" Project Description:
    --------------------
    Main program file used for the Capstone Project I application modeling a book stock
    management system excluding company and financial data and functionality. Program
    incorporates the use of sqlite3 allowing for CRUD operations

    Full Breakdown is available in the Software Requirements Document and ReadMe file

Module Summary:
---------------

- book_stock_management_system:
    houses database name, table name, desired Application Controller and View Renderer instances.
     Calls the Applicaton Controller application_run() method to start application
- Modulues.ui_controller__view:
    Main Application Controller and View Renderer modules
- Modules.business_logic.book:
    Book Entity object controlling attributes, above functionality and user_input
     for attributes. Field names and types have central control in class 'FieldControl'
- Modules.business_logic.entity_persistance_matcher_control:
    'linker class' using data from Entity Object to pass to Persistance Controller
- Modules.persistance_layer.persistance_classes_single_key: 
    Persistance Controller using data from Entity Object to create and execute queries

Architecture:
--------------
Variant architecture composed of MVC, Layered and Central Repository Designs

Other:
------
Project was designed with strong considerations of:
- Single-Use Responsibility
- Open-Closed Principle
- Dependency Decoupling

Restrictions:
-------------
Classes and modules are designed to work with tables that do not
use a composite primary_key. It is recommended that the primary_key type 
be Integer (set in Modules.busines_logic.book.FieldControl class)
"""

# Application Controller (MVC - Controller)
from Modules.ui_controller_view import book_stock_application_controller
# View Renderer (MVC - View)
from Modules.ui_controller_view import view_render

# set preferred database_name, table_name
DATABASE_NAME = "ebookstore"
TABLE_NAME = "books"
# Set Preferred Application controller and View Renderer for application usage
VIEW_RENDERER = view_render.ConsoleViewRender()
APPLICATION_CONTROLLER = book_stock_application_controller.BookStoreController(
    DATABASE_NAME, TABLE_NAME, VIEW_RENDERER)

# use application controller to begin run of application
APPLICATION_CONTROLLER.application_run()
