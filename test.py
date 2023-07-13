import sqlite3
from Modules.persistance_layer import persistence_classes_single_key
from Modules.business_logic import book

###########################################################################
# QUICK TESTING

# connection = sqlite3.connect("db")
# cursor = connection.cursor()

# print(cursor.execute("SELECT * from books WHERE id = ?", (3,)).fetchall())
# cursor.execute("DROP TABLE books")

# cursor.execute("DROP TABLE books")
# connection.commit()

# cursor.execute("SELECT * FROM books")
# names = [description[0] for description in cursor.description]
# print(names)

# connection.close()

############################################################################
# TESTING FOR book module

# 1) Create object holding fields for book table
# book_controller = book.BookController("Create Default Table")
# new_book = book_controller.create_crud_instance()
# print(new_book)

# 2) Create Book Object
# book_controller = book.BookController("Create Book")
# book_object = book_controller.create_crud_instance()
# print(book_object)

# 3) Search for a book
book_controller = book.BookController("Search Book")
book_object = book_controller.create_crud_instance()

############################################################################
# TESTING FOR persistence_classes_single_key
# table_creator = persistence_classes_single_key.CreateTableSingleKey("db", "books", "id", ["qty"], ["title", "author"])
# table_creator.execute()

# table_insert = persistence_classes_single_key.InsertData("db", "books", [(1,10,"book1", "auth1"), (2, 20, "book2", "auth2")])
# table_insert.execute()

# table_updater = persistence_classes_single_key.UpdateData("db", "books", ["price", "id"], (100, 2))
# table_updater.execute()

# table_deletion = persistence_classes_single_key.DeleteData("db", "books", "id", 3)
# table_deletion.execute()

# table_reader = persistence_classes_single_key.ReadData("db", "books", ["id", "qty", "title", "author"])
# print(table_reader.execute())
###############################################################################





# LATER TESTING


