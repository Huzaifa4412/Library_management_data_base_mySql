import mysql.connector as MyConn

my_db = MyConn.connect(host="localhost", user="root", password="H1u2z3@4i5", database="library_management")
print(my_db)
db_cursor = my_db.cursor()
#! When to add a single Value to the database
# db_cursor.execute("insert into Book(book_name, author_name,publication_year,book_price, book_quantity, book_genre,isRead) values(%s,%s,%s,%s,%s,%s,%s)", ("Harry Potter", "Huzaifa", 1980, 8000, 80, "Magical", True))

#! When to add multiple values to the database
db_insert_query = "insert into Book(book_name, author_name,publication_year,book_price, book_quantity, book_genre,isRead) values(%s,%s,%s,%s,%s,%s,%s)" 

db_list = [("Total Gaming", "Aju Bhai", 1980, 8000, 80, "Gaming", True), ("Captain America", "Ayan", 2020, 10000, 100, "Fighting", False)]

db_cursor.executemany(db_insert_query, db_list)

my_db.commit()
print(db_cursor.rowcount, "Record Inserted successfully")