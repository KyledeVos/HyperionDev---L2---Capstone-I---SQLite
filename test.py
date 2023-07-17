import sqlite3
from Modules.persistance_layer import persistence_classes_single_key
from Modules.business_logic import book
from Modules.business_logic import EntityPersistanceMatcherControl


###########################################################################
# QUICK TESTING

# connection = sqlite3.connect("db")
# cursor = connection.cursor()

# print(cursor.execute("SELECT * from books WHERE id = ?", (3,)).fetchall())
# print(cursor.execute("Select * FROM books ORDER BY id DESC LIMIT 1").fetchall())
# print(cursor.rowcount)


# cursor.execute("DROP TABLE books")

# cursor.execute("Insert INTO books VALUES(3, 20, 'book3', 'auth3')")
# print(cursor.rowcount)

# cursor.execute("DROP TABLE books")
# connection.commit()

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
# new_book = book_controller.create_crud_instance()
# print(new_book)

# 3) Create Book Object
# book_controller = book.BookController("Create Book")
# book_object = book_controller.create_crud_instance()
# print(book_object)

# 4) Search for a book
# book_controller = book.BookController("Search Book")
# read_object = book_controller.create_crud_instance()
# print(read_object)

# 5) Update a book
# book_controller = book.BookController("Update Book")
# update_object = book_controller.create_crud_instance()
# print(update_object)

# 6) Delete a Book
# book_controller = book.BookController("Delete Book")
# delete_book = book_controller.create_crud_instance()
# print(delete_book)


############################################################################
# INDEPENDENT TESTING FOR persistence_classes_single_key
# table_creator = persistence_classes_single_key.CreateTableSingleKey("db", "books", "id", ["qty"], ["title", "author"])
# table_creator.execute()

# table_insert = persistence_classes_single_key.InsertData("db", "books", [(1,10,"book1", "auth1"), (2, 20, "book2", "auth2")])
# table_insert.execute()

# table_updater = persistence_classes_single_key.UpdateData("db", "books", ["qty", "id"], (100, 3))
# print(table_updater.execute())

# table_deletion = persistence_classes_single_key.DeleteData("db", "books", "id", 1)
# print(table_deletion.execute())

# table_reader = persistence_classes_single_key.ReadData("db", "books", ["id", "qty", "title", "author"])
# print(table_reader.execute())


###############################################################################
# INDEPENDANT TESTING FOR EntityPersistanceSingleKeyControl Class

# 1) Test for Table Creation
# entity_persistence_object = EntityPersistanceMatcherControl.EntityPersistanceSingleKeyControl("books", "db", "Create Default Table")
# print(entity_persistence_object)

# 2) Test for Book Creation
# entity_persistence_object = EntityPersistanceMatcherControl.EntityPersistanceSingleKeyControl("books", "db", "Create Book")
# print(entity_persistence_object)

# 3) Test for Book Search
# entity_persistence_object = EntityPersistanceMatcherControl.EntityPersistanceSingleKeyControl("books", "db", "Search Book")
# print(entity_persistence_object)

# 4) Test for Book Update
# entity_persistence_object = EntityPersistanceMatcherControl.EntityPersistanceSingleKeyControl("books", "db", "Update Book")
# print(entity_persistence_object)

# 5) Test for Book Deletion
# entity_persistence_object = EntityPersistanceMatcherControl.EntityPersistanceSingleKeyControl("books", "db", "Delete Book")
# print(entity_persistence_object)




