
# personal library manager
import mysql.connector
import streamlit as st


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        host="https://personal-library-manager-sakeena.streamlit.app/",
        user="Sakeena",  
        password="03701131858", 
        database="library_db"
    )

# Add a Book
def add_book(title, author, year, genre, read_status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year, genre, read_status) VALUES (%s, %s, %s, %s, %s)",
                   (title, author, year, genre, read_status))
    conn.commit()
    conn.close()

# Remove a Book
def remove_book(title):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE title = %s", (title,))
    conn.commit()
    conn.close()

# Get All Books
def get_all_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

# Search Books
def search_books(query, search_by):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM books WHERE {search_by} LIKE %s", (f"%{query}%",))
    results = cursor.fetchall()
    conn.close()
    return results

# Get Statistics
def get_statistics():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 1")
    read_books = cursor.fetchone()[0]
    conn.close()
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, read_percentage

# Streamlit UI Setup
st.set_page_config(page_title="📚 Personal Library Manager", page_icon="📖", layout="wide")
st.title("📚 Personal Library Manager")

menu = st.sidebar.radio("📌 Menu", ["🏠 Home", "➕ Add a Book", "🗑 Remove a Book", "🔍 Search for a Book", "📚 Display All Books", "📊 Display Statistics", "🚪 Exit"])

# Home Page
if menu == "🏠 Home":
    st.header("Welcome to Your Personal Library Manager! 📖")
    st.write("Manage your book collection easily with this interactive tool.")
    st.image("https://thumbs.dreamstime.com/b/library-books-background-book-closet-filled-41199253.jpg", use_container_width=True)

# Add a Book
elif menu == "➕ Add a Book":
    st.header("➕ Add a New Book")
    title = st.text_input("📖 Book Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Publication Year", min_value=0, max_value=2100, step=1)
    genre = st.text_input("🎭 Genre")
    read_status = st.checkbox("✅ Mark as Read")
    if st.button("📚 Add Book", use_container_width=True):
        if title and author and year and genre:
            add_book(title, author, year, genre, read_status)
            st.success("✅ Book added successfully!")
        else:
            st.warning("❌ Please fill in all fields!")

# Remove a Book
elif menu == "🗑 Remove a Book":
    st.header("🗑 Remove a Book")
    title = st.text_input("📖 Enter the title of the book to remove")
    if st.button("🗑 Remove Book", use_container_width=True):
        remove_book(title)
        st.success("✅ Book removed successfully!")

# Search for a Book
elif menu == "🔍 Search for a Book":
    st.header("🔍 Search for a Book")
    search_by = st.radio("Search by", ["title", "author"], horizontal=True)
    query = st.text_input("🔎 Enter search term")
    if st.button("🔍 Search", use_container_width=True):
        results = search_books(query, search_by)
        if results:
            for book in results:
                status = "✅ Read" if book[5] else "📖 Unread"
                st.markdown(f"🔹 **Title:** *{book[1]}*  \n🔹 **Author:** *{book[2]}*  \n🔹 **Year:** *{book[3]}*  \n🔹 **Genre:** *{book[4]}*  \n🔹 **Status:** {status}")
        else:
            st.warning("❌ No books found!")

# Display All Books
elif menu == "📚 Display All Books":
    st.header("📚 Your Library")
    books = get_all_books()
    if books:
        for book in books:
            status = "✅ Read" if book[5] else "📖 Unread"
            st.markdown(f"🔹 **Title:** *{book[1]}*  \n🔹 **Author:** *{book[2]}*  \n🔹 **Year:** *{book[3]}*  \n🔹 **Genre:** *{book[4]}*  \n🔹 **Status:** {status}")
    else:
        st.warning("📭 Your library is empty!")

# Display Statistics
elif menu == "📊 Display Statistics":
    st.header("📊 Library Statistics")
    total_books, read_percentage = get_statistics()
    col1, col2 = st.columns(2)
    col1.metric("📚 Total Books", total_books)
    col2.metric("📖 Percentage Read", f"{read_percentage:.2f}%")
    st.progress(read_percentage / 100)

# Exit Option
elif menu == "🚪 Exit":
    st.header("🚪 Exiting Program")
    st.write("Thank you for using Personal Library Manager! 📚")
    balloon = st.balloons()