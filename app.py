from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return jsonify({"message": "Lumina Backend Running"})


def init_db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            genre TEXT,
            year INTEGER,
            rating INTEGER,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/books", methods=["GET"])
def get_books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "id": b[0],
            "title": b[1],
            "author": b[2],
            "genre": b[3],
            "year": b[4],
            "rating": b[5],
            "status": b[6]
        } for b in books
    ])

@app.route("/add", methods=["POST"])
def add_book():
    data = request.json
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO books (title, author, genre, year, rating, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["title"],
        data["author"],
        data["genre"],
        data["year"],
        data["rating"],
        data["status"]
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Book added"})

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_book(id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Deleted successfully"})
