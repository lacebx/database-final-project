import mysql.connector
from tkinter import *

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Yoursenpai1",
    database="finalp"
)
cursor = db.cursor()


def search_books():
    # Clear the result text box
    result_text.delete(1.0, END)

    # Get the search keyword
    keyword = search_entry.get()

    # Search for books with the keyword in the title
    query = "SELECT * FROM Books WHERE title LIKE %s"
    value = ("%" + keyword + "%",)
    cursor.execute(query, value)
    books = cursor.fetchall()

    # Display the search results
    for book in books:
        result_text.insert(END, f"Title: {book[1]}\n")
        result_text.insert(END, f"Author(s): {get_authors(book[0])}\n")
        result_text.insert(END, f"Subjects: {get_subjects(book[0])}\n")
        result_text.insert(END, "------------------------\n")

    # Clear the search entry
    search_entry.delete(0, END)


def get_authors(book_id):
    # Retrieve the authors of the book
    query = "SELECT name FROM Authors WHERE book_id = %s"
    value = (book_id,)
    cursor.execute(query, value)
    authors = cursor.fetchall()

    # Format the authors' names
    author_names = [author[0] for author in authors]
    return ", ".join(author_names)


def get_subjects(book_id):
    # Retrieve the subjects of the book
    query = "SELECT subject FROM Subjects WHERE book_id = %s"
    value = (book_id,)
    cursor.execute(query, value)
    subjects = cursor.fetchall()

    # Format the subjects
    subject_names = [subject[0] for subject in subjects]
    return ", ".join(subject_names)


# Create the main window
window = Tk()
window.title("Book Search")
window.geometry("400x300")

# Create the search label and entry
search_label = Label(window, text="Search:")
search_label.pack()

search_entry = Entry(window, width=30)
search_entry.pack()

# Create the search button
search_button = Button(window, text="Search", command=search_books)
search_button.pack()

# Create the result text box
result_text = Text(window, width=50, height=10)
result_text.pack()

# Start the GUI main loop
window.mainloop()

# Close the database connection
cursor.close()
db.close()