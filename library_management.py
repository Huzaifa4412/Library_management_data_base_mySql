import streamlit as st
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

db_config = {
    "host": os.getenv("DATABASE_HOST_NAME"),
    "user": os.getenv("DATABASE_USERNAME"),
    "password": os.getenv("DATABASE_PASSWORD"),
    "database": os.getenv("DATABASE_NAME")
}

def db_connection():
    return mysql.connector.connect(**db_config)

def create_table():
    with db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                book_name VARCHAR(255),
                author_name VARCHAR(255),
                publication_year VARCHAR(20),
                book_price INT,
                book_quantity INT,
                book_genre VARCHAR(50),
                isRead BOOLEAN
            )
            ''')
            conn.commit()

def get_book_names():
    with db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT book_name FROM books")
            return [row[0] for row in cursor.fetchall()]

def add_book(book_name, author_name, publication_year, book_price, book_quantity, book_genre, is_read):
    with db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO books (book_name, author_name, publication_year, book_price, book_quantity, book_genre, isRead)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (book_name, author_name, publication_year, book_price, book_quantity, book_genre, is_read))
            conn.commit()

def view_books():
    with db_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM books")
            return cursor.fetchall()

def remove_book(book_name):
    with db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM books WHERE book_name = %s", (book_name,))
            conn.commit()

def update_book_status(book_name, is_read):
    with db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE books SET isRead = %s WHERE book_name = %s", (is_read, book_name))
            conn.commit()

def search_books(column, value):
    with db_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT * FROM books WHERE {column} = %s", (value,))
            return cursor.fetchall()

# Streamlit UI
st.set_page_config(page_title="Library Management", layout="wide")
st.title("📚 Library Management System")

menu = ["Add Book", "View Books", "Update Book", "Remove Book", "Search Book"]
choice = st.sidebar.selectbox("Menu", menu)

create_table()

if choice == "Add Book":
    with st.form("add_book_form"):
        book_name = st.text_input("Book Name")
        author_name = st.text_input("Author Name")
        publication_year = st.text_input("Publication Year")
        book_price = st.number_input("Book Price", min_value=0)
        book_quantity = st.number_input("Book Quantity", min_value=1)
        book_genre = st.text_input("Book Genre")
        is_read = st.checkbox("Have you read this book?")
        submit = st.form_submit_button("Add Book")
        
        if submit:
            add_book(book_name, author_name, publication_year, book_price, book_quantity, book_genre, is_read)
            st.success(f"Book '{book_name}' added successfully!")

elif choice == "View Books":
    books = view_books()
    st.write("### List of Books")
    st.dataframe(books)

elif choice == "Update Book":
    book_names = get_book_names()
    book_name = st.selectbox("Select Book to Update", book_names)
    is_read = st.checkbox("Mark as Read")
    if st.button("Update Status"):
        update_book_status(book_name, is_read)
        st.success("Book status updated successfully!")

elif choice == "Remove Book":
    book_names = get_book_names()
    book_name = st.selectbox("Select Book to Remove", book_names)
    if st.button("Remove Book"):
        remove_book(book_name)
        st.warning("Book removed successfully!")

elif choice == "Search Book":
    search_option = st.radio("Search by", ["Title", "Author"])
    search_value = st.text_input("Enter search value")
    if st.button("Search"):
        column = "book_name" if search_option == "Title" else "author_name"
        results = search_books(column, search_value)
        st.dataframe(results)
