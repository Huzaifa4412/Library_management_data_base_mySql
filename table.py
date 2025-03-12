import mysql.connector as MyConn

my_db = MyConn.connect(host="localhost", user="root", password="H1u2z3@4i5", database="library_management")
print(my_db)
db_cursor = my_db.cursor()

# To Create Table
db_cursor.execute("create table Book(book_name varchar(30), author_name varchar(30),publication_year varchar(20),book_price int, book_quantity int, book_genre varchar(10),isRead bool)")

# To Show Table
db_cursor.execute("show tables")
for table in db_cursor:
    print(table)

print("Table Created Successfully !!")