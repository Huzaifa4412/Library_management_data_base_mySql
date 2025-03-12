import mysql.connector as MyConn

my_db = MyConn.connect(host="localhost", user="root", password="H1u2z3@4i5", database="library_management")
db_cursor = my_db.cursor()
db_cursor.execute("create database library_management")