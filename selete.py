import mysql.connector as MyConn

my_db = MyConn.connect(host="localhost", user="root", password="H1u2z3@4i5", database="library_management")
print(my_db)
db_cursor = my_db.cursor()

db_cursor.execute("select * from library_management.Book")

for db_data in db_cursor.fetchall():
    print(db_data)
