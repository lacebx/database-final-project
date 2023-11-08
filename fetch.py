import requests
import mysql.connector
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
# Specify the path to the JSON file
json_file_path = "gutendex_data.json"

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Yoursenpai1",
    database="mydatabase"
)
cursor = db.cursor()


# Read the JSON data from the file
with open(json_file_path, "r") as json_file:
    json_data = json.load(json_file)

        
        # Iterate through the JSON data and insert it into the database
for item in json_data['results']:
            # Extract and insert book data into the Book table
            book_id = item['id']
            title = item['title']
            subjects = ', '.join(item['subjects'])
            download_count = item['download_count']
            authors = json.dumps(item['authors'])
            translators = json.dumps(item['translators'])
            bookshelves = ', '.join(item['bookshelves'])
            languages = ', '.join(item['languages'])
            copyright = item['copyright']
            media_type = item['media_type']
            formats = json.dumps(item['formats'])
            
            # Insert data into the Book table
            book_sql = "INSERT INTO Book (id, title, subjects, authors, translators, bookshelves, languages, copyright, media_type, formats, download_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            book_val = (book_id, title, subjects, authors, translators, bookshelves, languages, copyright, media_type, formats, download_count)
            cursor.execute(book_sql, book_val)

            # Extract author data and insert into the Author table
            for author_data in item['authors']:
                author_name = author_data['name']
                author_birth_year = author_data['birth_year']
                author_death_year = author_data['death_year']

                author_sql = "INSERT INTO Author (name, birth_year, death_year) VALUES (%s, %s, %s)"
                author_val = (author_name, author_birth_year, author_death_year)
                cursor.execute(author_sql, author_val)

            # Extract format data and insert into the Format table
            format_data = item['formats']
            for format_type, format_url in format_data.items():
                format_sql = "INSERT INTO Format (book_id, mime_type, url) VALUES (%s, %s, %s)"
                format_val = (book_id, format_type, format_url)
                cursor.execute(format_sql, format_val)

        # Commit changes and close the database connection
db.commit()
cursor.close()
db.close()

