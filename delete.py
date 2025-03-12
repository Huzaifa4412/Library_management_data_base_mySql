import mysql.connector as MyConn

my_db = MyConn.connect(host="localhost", user="root", password="H1u2z3@4i5", database="library_management")
print(my_db)
db_cursor = my_db.cursor()

# Delete Single Data
db_delete_query = "delete from library_management.Book where book_name = %s"
db_value = ("Total Gaming",)
db_cursor.execute(db_delete_query, db_value)
my_db.commit()

# Delete all Data
db_delete_query = "truncate table library_management.Book"
db_cursor.execute(db_delete_query)
print(f"Number of rows deleted: {db_cursor.rowcount}")