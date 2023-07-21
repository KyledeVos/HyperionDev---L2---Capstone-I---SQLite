import sqlite3
from Modules.persistance_layer import persistence_classes_single_key
from Modules.business_logic import book
from Modules.business_logic import entity_persistance_matcher_control


###########################################################################
# QUICK TESTING

# connection = sqlite3.connect("test_db")
# cursor = connection.cursor()

# -- create new table
# cursor.execute("CREATE TABLE IF NOT EXISTS books(id INTEGER NOT NULL PRIMARY KEY, " +
#                "qty INTEGER NOT NULL, author TEXT NOT NULL, title TEXT NOT NULL)")

# -- check if table exists
# table_count = cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='books'").fetchone()
# print(table_count)

# -- various read from table
# print(cursor.execute("SELECT * FROM books").fetchall())
# # print(cursor.execute("SELECT * from books WHERE id = ?", (3,)).fetchall())
# print(cursor.execute("Select * FROM books ORDER BY id DESC LIMIT 1").fetchall())
# print(cursor.rowcount)

# -- delete table
# cursor.execute("DROP TABLE books")
# connection.commit()

# -- Insert data into table
# cursor.execute("Insert INTO books VALUES(3, 20, 'book3', 'auth3')")
# connection.commit()
# print(cursor.rowcount)

# -- delete table
# cursor.execute("DROP TABLE books")
# connection.commit()

# -- see table column names
# cursor.execute("SELECT * FROM books")
# names = [description[0] for description in cursor.description]
# print(names)

# connection.close()

############################################################################
# INDEPENDENT TESTING FOR book module

# # 1) Testing of Field Control
# field_control = book.FieldControl()
# print(field_control)

# 2) Create object holding fields for book table
# book_controller = book.BookController("Create Default Table")
# new_table = book_controller.create_crud_instance()
# print(new_table)

# 3) Create Book Object
# book_controller = book.BookController("Create Entity")
# book_object = book_controller.create_crud_instance()
# print(book_object)

# 4) Search for a book
# book_controller = book.BookController("Search Entity")
# read_object = book_controller.create_crud_instance()
# print(read_object)

# 5) Update a book
# book_controller = book.BookController("Update Entity")
# update_object = book_controller.create_crud_instance()
# print(update_object)

# 6) Delete a Book
# book_controller = book.BookController("Delete Entity")
# delete_book = book_controller.create_crud_instance()
# print(delete_book)


############################################################################
# INDEPENDENT TESTING FOR persistence_classes_single_key

# 1) Table Creation
# table_creator = persistence_classes_single_key.CreateTableSingleKey("db", "books", "id", ["qty"], ["title", "author"])
# table_creator.execute()

# 2) Determine if Table Exists
# table_verifier = persistence_classes_single_key.VerifyTable("db", "books")
# print(table_verifier.execute())

# 3) Insert Data
# table_insert = persistence_classes_single_key.InsertData("db", "books", [(1, 10,"book1", "auth1"),
#                                                                          (2, 20, "book2", "auth2"), (3, 10, "book3", "auth3")])
# table_insert.execute()

# 4) Update Data
# table_updater = persistence_classes_single_key.UpdateData("db", "books", ["qty", "id"], (100, 3))
# print(table_updater.execute())

# 5) Delete Data
# table_deletion = persistence_classes_single_key.DeleteData("db", "books", "id", 1)
# print(table_deletion.execute())

# 6) Read Data
# table_reader = persistence_classes_single_key.ReadData("db", "books", ["id", "qty", "title", "author"])
# print(table_reader.execute())

# 7) Return Last id value in row
# last_row = persistence_classes_single_key.ReturnLastId("db", "books", "id")
# print(last_row.execute())


###############################################################################
# INDEPENDANT TESTING FOR EntityPersistanceSingleKeyControl Class

# 1) Test for Table Creation
# entity_persistence_object = EntityPersistanceMatcherControl.EntityPersistanceSingleKeyControl(
#     "books", "db", "Create Default Table")
# print(entity_persistence_object)

# # 2) Test for Book Creation
# entity_persistence_object = EntityPersistanceMatcherControl.EntityPersistanceSingleKeyControl("books", "db", "Create Entity")
# print(entity_persistence_object)

# 3) Test for Book Search
# entity_persistence_object = EntityPersistanceMatcherControl.EntityPersistanceSingleKeyControl("books", "db", "Search Entity")
# print(entity_persistence_object)

# 4) Test for Book Update
# entity_persistence_object = EntityPersistanceMatcherControl.EntityPersistanceSingleKeyControl("books", "db", "Update Entity")
# print(entity_persistence_object)

# 5) Test for Book Deletion
# entity_persistence_object = EntityPersistanceMatcherControl.EntityPersistanceSingleKeyControl("books", "db", "Delete Entity")
# print(entity_persistence_object)

###############################################################################
# TESTING FOR PersistanceSingleKeyControl Class using EntityControl

# 1) Test for Table Creation
# # Create Entity Object - Book
# book_controller = book.BookController("Create Default Table")
# new_table = book_controller.create_crud_instance()
# # Create Table in Database
# persistance_control = entity_persistance_matcher_control.PersistanceSingleKeyControl(
#     "db", "books", "Create Default Table", new_table)
# persistance_control.perform_database_query()

# 2) Test Row Insertion
# # Create Entity Object - Book
# book_controller = book.BookController("Create Entity")
# new_book = book_controller.create_crud_instance()
# # Add book to database
# persistance_control = entity_persistance_matcher_control.PersistanceSingleKeyControl(
#     "db", "books", "Create Entity", new_book)
# insert_successful = persistance_control.perform_database_query()
# print(insert_successful)

# 3) Test for Table Read
# # Create Entity Object - Book
# book_controller = book.BookController("Read Entity")
# search_book = book_controller.create_crud_instance()
# # Read from database
# persistance_control = entity_persistance_matcher_control.PersistanceSingleKeyControl(
#     "db", "books", "Read Entity", search_book)
# matching_rows = persistance_control.perform_database_query()
# print(matching_rows)

# 4) Test for All Table Rows Read
# Create Entity Object - Book
book_controller = book.BookController("Read All")
read_all = book_controller.create_crud_instance()
# Read from database
persistance_control = entity_persistance_matcher_control.PersistanceSingleKeyControl(
    "db", "books", "Read Entity", read_all)
matching_rows = persistance_control.perform_database_query()
print(matching_rows)

# 5) Test for Table Update
# # Create Entity Object - Book
# book_controller = book.BookController("Update Entity")
# update_book = book_controller.create_crud_instance()
# # Make update to database
# persistance_control = entity_persistance_matcher_control.PersistanceSingleKeyControl(
#     "db", "books", "Update Entity", update_book )
# update_successful = persistance_control.perform_database_query()
# print(update_successful)

# # 6) Test for Table Row Deletion
# # Create Entity Object - Book
# book_controller = book.BookController("Delete Entity")
# delete_book = book_controller.create_crud_instance()
# # Make update to database
# persistance_control = entity_persistance_matcher_control.PersistanceSingleKeyControl(
#     "db", "books", "Delete Entity", delete_book )
# delete_successful = persistance_control.perform_database_query()
# print(delete_successful)

###############################################################################
