import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Getting the variables from .env files
database_host_name = os.environ.get("DATABASE_HOST_NAME")
database_username = os.environ.get("DATABASE_USERNAME")
database_name= os.environ.get("DATABASE_NAME")
database_password = os.environ.get("DATABASE_PASSWORD")

RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"

# 📂 Helper function to manage DB connection
def db_connection():
    return mysql.connector.connect(
        host=database_host_name,
        user=database_username,
        password=database_password,
        database=database_name
    )

# 🟩 Create the 'books' table 
def create_table():
    with db_connection() as connection:
        with connection.cursor() as cursor:
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
            connection.commit()
            print(f"{GREEN}Table created successfully!{RESET}")

def add_book():
    print(f"{BLUE}Adding a new book...{RESET}")
    book_name = input("Enter book name: ")
    author_name = input("Enter author name: ")
    publication_year = input("Enter publication year: ")
    book_price = int(input("Enter book price: "))
    book_quantity = int(input("Enter book quantity: "))
    book_genre = input("Enter book genre: ")
    isRead = input("Have you read this book? (yes/no): ").lower() in ['yes', 'y']

    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
            INSERT INTO books (book_name, author_name, publication_year, book_price, book_quantity, book_genre, isRead)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (book_name, author_name, publication_year, book_price, book_quantity, book_genre, isRead))
            connection.commit()
            print(f"{GREEN}Book '{book_name}' by {author_name} added successfully!{RESET}")

# 🗑️ Remove a book
def remove_book():
    print(f"{RED}Removing a book...{RESET}")
    book_name = input("Enter the title of the book to remove: ")
    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM books WHERE book_name = %s", (book_name,))
            connection.commit()
            print(f"{GREEN}Book '{book_name}' deleted successfully!{RESET}")

# 🔁 Update a book
def update_book():
    print(f"{GREEN}Update the book ...{RESET}")
    book_name:str = input(f"{CYAN}Enter the book name: {RESET}")
    isRead = input("Have you read this book? (yes/no): ").lower() in ['yes', 'y']
    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("update books set isRead=%s where book_name=%s", (isRead,book_name))
        connection.commit()
    print(f"{GREEN}Books updated ...{RESET}")


    
# 👀 View all books
def view_books():
    print(f"{YELLOW}Viewing all books...{RESET}")
    with db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM books")
            books = cursor.fetchall()
            
            if not books:
                print(f"{RED}No books available in the library.{RESET}")
            else:
                print(f"{CYAN}\nLibrary Books:{RESET}")
                for book in books:
                    status = f"{GREEN}Read{RESET}" if book['isRead'] else f"{RED}Not Read{RESET}"
                    print(f"ID: {book['id']}, Title: {book['book_name']}, Author: {book['author_name']}, Status: {status}")

# 📘 Search for a book
def search_book():
    print(f"{MAGENTA}Searching for a book...{RESET}")
    search_by = input("Search by:\n1. Title\n2. Author\nEnter choice: ")

    if search_by == "1":
        book_title = input("Enter the book title: ")
        query = "SELECT * FROM books WHERE book_name = %s"
        param = (book_title,)
    elif search_by == "2":
        book_author = input("Enter the book author: ")
        query = "SELECT * FROM books WHERE author_name = %s"
        param = (book_author,)
    else:
        print(f"{RED}Invalid choice, please select 1 or 2.{RESET}")
        return

    with db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, param)
            books = cursor.fetchall()

            if books:
                for book in books:
                    print(f"{GREEN}Title: {book['book_name']}, Author: {book['author_name']}{RESET}")
            else:
                print(f"{RED}No matching books found.{RESET}")

# 🟠 Main menu
if __name__ == "__main__":
    create_table()
    
    while True:
        print(f"{BLUE}\nLibrary Management System{RESET}")
        print(f"{YELLOW}1. Add a Book{RESET}")
        print(f"{YELLOW}2. Remove a Book{RESET}")
        print(f"{YELLOW}3. Search a Book{RESET}")
        print(f"{YELLOW}4. View All Books{RESET}")
        print(f"{YELLOW}5. Update Status{RESET}")
        
        print(f"{RED}6. Exit{RESET}")
        
        choice = input("Choose an option (1-6): ")
        
        if choice == "1":
            add_book()
        elif choice == "2":
            remove_book()
        elif choice == "3":
            search_book()
        elif choice == "4":
            view_books()
        elif choice == "5":
            update_book()
        elif choice == "6":
            print(f"{RED}Goodbye!{RESET}")
            
            break
        else:
            print(f"{RED}Invalid choice. Please try again.{RESET}")

