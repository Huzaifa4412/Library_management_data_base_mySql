import mysql.connector as MyConn

my_db = MyConn.connect(host="localhost", user="root", password="H1u2z3@4i5", database="library_management")
print(my_db)
db_cursor = my_db.cursor()

db_update_query = "update library_management.Book set author_name = %s where book_name=%s"
db_value = ("Huzaifa Bhai", "Total Gaming")
db_cursor.execute(db_update_query, db_value)
my_db.commit()

print(f"Number of rows updated: {db_cursor.rowcount}")