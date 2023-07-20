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
    UI with user input request
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
A variant architecture composed of Layered and Repository Designs

NOTE: all classes and modules are designed to work with tables that do not
use a composite primary_key. It is recommended that the primary_key type 
be Integer (set in Modules.busines_logic.book.FieldControl class)
"""

from Modules.business_logic import entity_persistance_matcher_control

# set preferred database_name and table_name for application usage
DATABASE_NAME = "ebookstore"
TABLE_NAME = "books"

# table fields and types are set in Modules.busines_logic.book.FieldControl class
# Attempt to Create table (if not present) before menu print to user
# if table with matching table is found in database, new table creation is not attempted
entity_control = entity_persistance_matcher_control.EntityPersistanceSingleKeyControl(DATABASE_NAME, TABLE_NAME, "Create Default Table")
# required execution method to perform query against database
entity_control.create_and_execute_query()
