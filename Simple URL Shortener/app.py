from flask import Flask, request, redirect, render_template
import sqlite3
import string
import random
import os

app = Flask(__name__)

# ----------------------
# Database Initialization
# ----------------------
def init_db():
    if not os.path.exists("database.db"):
        with sqlite3.connect("database.db") as conn:
            conn.execute('''CREATE TABLE urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_code TEXT NOT NULL UNIQUE
            )''')

# ----------------------
# Generate Short Code
# ----------------------
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# ----------------------
# Home Page & Form
# ----------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        short_code = generate_short_code()

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO urls (original_url, short_code) VALUES (?, ?)", (original_url, short_code))
            conn.commit()

        short_url = request.host_url + short_code
        return render_template('index.html', short_url=short_url)

    return render_template('index.html', short_url=None)

# ----------------------
# Redirect to Original URL
# ----------------------
@app.route('/<short_code>')
def redirect_to_url(short_code):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT original_url FROM urls WHERE short_code = ?", (short_code,))
        result = cursor.fetchone()

        if result:
            return redirect(result[0])
        else:
            return "Short URL not found!", 404

# ----------------------
# Run App
# ----------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
