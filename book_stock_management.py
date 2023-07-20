# Level 2 - Kyle de Vos (KD23040008523)
# L2T13 - Capstone Project I
# Date: 2 July 2023
# ____________________________________________________________
""" This is the main program file used for the Capstone Project I application
with the application modeling a book stock management system excluding
company and financial data and functionality. 

This program allows the application to create a sqlite3 database 'ebookstore'
in which a table 'books' is created. The application allows a user to:
Create a new Book, Return all book data, Search for a book, Update the data
for a book and Delete a book. 

A detailed breakdown of the programs functionality is available in the ReadMe
and Software Requirements Documents, but a summary of the various Modules is
as follows for quick reference

book_stock_management_system:
    houses only the database name, table name, desired Application Controller
     and View Renderer. Calls the Applicaton Controller application_run() method
     to start application
Modulues.ui_controller__view:
    Holds Main Controller and View modules
Modules.business_logic.book:
    Entity object controlling book attributes, above functionality and user_input
     for attributes. Field names and types have been given a centralised control
     by class 'FieldControl'
Modules.business_logic.entity_persistance_matcher_control:
    'linker class' using data from Entity Object to pass to persistance Controller
Modules.persistance_layer.persistance_classes_single_key: 
    Persistance Controller using data from Entity Object to create and execute queries

This application attempts to implement:
Single-Use Responsibility
Open-Closed Principle
Dependency Decoupling
A variant architecture composed of MVC, Layered and Repository Designs

NOTE: all classes and modules are designed to work with tables that do not
use a composite primary_key. It is recommended that the primary_key type 
be Integer (set in Modules.busines_logic.book.FieldControl class)
"""
from Modules.ui_controller_view import book_stock_application_controller
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

