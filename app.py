# import json
# import streamlit as st

# # File to save and load library data
# LIBRARY_FILE = "library.json"

# def load_library():
#     """Load the library from a file."""
#     try:
#         with open(LIBRARY_FILE, "r") as file:
#             return json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return []

# def save_library(library):
#     """Save the library to a file."""
#     with open(LIBRARY_FILE, "w") as file:
#         json.dump(library, file, indent=4)

# def add_book(library, title, author, year, genre, read_status):
#     """Add a new book to the library."""
#     library.append({
#         "title": title,
#         "author": author,
#         "year": year,
#         "genre": genre,
#         "read": read_status
#     })
#     save_library(library)

# def remove_book(library, title):
#     """Remove a book from the library."""
#     for book in library:
#         if book["title"].lower() == title.lower():
#             library.remove(book)
#             save_library(library)
#             return True
#     return False

# def search_book(library, query, search_by):
#     """Search for a book by title or author."""
#     return [book for book in library if query.lower() in book[search_by].lower()]

# def display_statistics(library):
#     """Display total books and percentage read."""
#     total_books = len(library)
#     read_books = sum(1 for book in library if book["read"])
#     read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
#     return total_books, read_percentage

# # Streamlit UI
# st.set_page_config(page_title="📚 Personal Library Manager", page_icon="📖", layout="wide")
# st.title("📚 Personal Library Manager")
# library = load_library()

# menu = st.sidebar.radio("📌 Menu", ["🏠 Home", "➕ Add a Book", "🗑 Remove a Book", "🔍 Search for a Book", "📚 Display All Books", "📊 Display Statistics"])

# if menu == "🏠 Home":
#     st.header("Welcome to Your Personal Library Manager! 📖")
#     st.write("Manage your book collection easily with this interactive tool.")
#     st.image("https://thumbs.dreamstime.com/b/library-books-background-book-closet-filled-41199253.jpg", use_container_width=True)

# elif menu == "➕ Add a Book":
#     st.header("➕ Add a New Book")
#     title = st.text_input("📖 Book Title")
#     author = st.text_input("✍️ Author")
#     year = st.number_input("📅 Publication Year", min_value=0, max_value=2100, step=1)
#     genre = st.text_input("🎭 Genre")
#     read_status = st.checkbox("✅ Mark as Read")
#     if st.button("📚 Add Book", use_container_width=True):
#         add_book(library, title, author, year, genre, read_status)
#         st.success("✅ Book added successfully!")

# elif menu == "🗑 Remove a Book":
#     st.header("🗑 Remove a Book")
#     title = st.text_input("📖 Enter the title of the book to remove")
#     if st.button("🗑 Remove Book", use_container_width=True):
#         if remove_book(library, title):
#             st.success("✅ Book removed successfully!")
#         else:
#             st.error("❌ Book not found!")

# elif menu == "🔍 Search for a Book":
#     st.header("🔍 Search for a Book")
#     search_by = st.radio("Search by", ["title", "author"], horizontal=True)
#     query = st.text_input("🔎 Enter search term")
#     if st.button("🔍 Search", use_container_width=True):
#         results = search_book(library, query, search_by)
#         if results:
#             for book in results:
#                 status = "✅ Read" if book["read"] else "📖 Unread"
#                 st.markdown(f"**📖 {book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {status}")
#         else:
#             st.warning("❌ No books found!")

# elif menu == "📚 Display All Books":
#     st.header("📚 Your Library")
#     if library:
#         for book in library:
#             status = "✅ Read" if book["read"] else "📖 Unread"
#             st.markdown(f"**📖 {book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {status}")
#     else:
#         st.warning("📭 Your library is empty!")

# elif menu == "📊 Display Statistics":
#     st.header("📊 Library Statistics")
#     total_books, read_percentage = display_statistics(library)
#     col1, col2 = st.columns(2)
#     col1.metric("📚 Total Books", total_books)
#     col2.metric("📖 Percentage Read", f"{read_percentage:.2f}%")
    
#     st.progress(read_percentage / 100)

import sqlite3
import streamlit as st

db_file = "library.db"

def init_db():
    """Create books table if not exists"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        author TEXT,
                        year INTEGER,
                        genre TEXT,
                        read INTEGER)''')
    conn.commit()
    conn.close()

def add_book(title, author, year, genre, read_status):
    """Add a book to the database"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year, genre, read) VALUES (?, ?, ?, ?, ?)",
                   (title, author, year, genre, int(read_status)))
    conn.commit()
    conn.close()

def remove_book(title):
    """Remove a book by title"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE title = ?", (title,))
    conn.commit()
    conn.close()

def search_books(query, search_by):
    """Search books by title or author"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM books WHERE {search_by} LIKE ?", (f"%{query}%",))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_books():
    """Fetch all books"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

def get_statistics():
    """Get total books and read percentage"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM books WHERE read = 1")
    read_books = cursor.fetchone()[0]
    conn.close()
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, read_percentage

# Streamlit UI
st.set_page_config(page_title="📚 Personal Library Manager", page_icon="📖", layout="wide")
st.title("📚 Personal Library Manager")
init_db()

menu = st.sidebar.radio("📌 Menu", ["🏠 Home", "➕ Add a Book", "🗑 Remove a Book", "🔍 Search for a Book", "📚 Display All Books", "📊 Display Statistics"])

if menu == "🏠 Home":
    st.header("Welcome to Your Personal Library Manager! 📖")
    st.write("Manage your book collection easily with this interactive tool.")
    st.image("https://thumbs.dreamstime.com/b/library-books-background-book-closet-filled-41199253.jpg", use_container_width=True)

elif menu == "➕ Add a Book":
    st.header("➕ Add a New Book")
    title = st.text_input("📖 Book Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Publication Year", min_value=0, max_value=2100, step=1)
    genre = st.text_input("🎭 Genre")
    read_status = st.checkbox("✅ Mark as Read")
    if st.button("📚 Add Book", use_container_width=True):
        add_book(title, author, year, genre, read_status)
        st.success("✅ Book added successfully!")

elif menu == "🗑 Remove a Book":
    st.header("🗑 Remove a Book")
    title = st.text_input("📖 Enter the title of the book to remove")
    if st.button("🗑 Remove Book", use_container_width=True):
        remove_book(title)
        st.success("✅ Book removed successfully!")

elif menu == "🔍 Search for a Book":
    st.header("🔍 Search for a Book")
    search_by = st.radio("Search by", ["title", "author"], horizontal=True)
    query = st.text_input("🔎 Enter search term")
    if st.button("🔍 Search", use_container_width=True):
        results = search_books(query, search_by)
        if results:
            for book in results:
                status = "✅ Read" if book[5] else "📖 Unread"
                st.markdown(f"**📖 {book[1]}** by *{book[2]}* ({book[3]}) - {book[4]} - {status}")
        else:
            st.warning("❌ No books found!")

elif menu == "📚 Display All Books":
    st.header("📚 Your Library")
    books = get_all_books()
    if books:
        for book in books:
            status = "✅ Read" if book[5] else "📖 Unread"
            st.markdown(f"**📖 {book[1]}** by *{book[2]}* ({book[3]}) - {book[4]} - {status}")
    else:
        st.warning("📭 Your library is empty!")

elif menu == "📊 Display Statistics":
    st.header("📊 Library Statistics")
    total_books, read_percentage = get_statistics()
    col1, col2 = st.columns(2)
    col1.metric("📚 Total Books", total_books)
    col2.metric("📖 Percentage Read", f"{read_percentage:.2f}%")
    st.progress(read_percentage / 100)

import sqlite3
from tabulate import tabulate

# Database se connection
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Data fetch karna
cursor.execute("SELECT * FROM books")
books = cursor.fetchall()

# Column names lena
cursor.execute("PRAGMA table_info(books)")
columns = [col[1] for col in cursor.fetchall()]

# Table format mein print karna
print(tabulate(books, headers=columns, tablefmt="grid"))

conn.close()
