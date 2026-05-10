from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("tourism.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            tour_id INTEGER,
            FOREIGN KEY(tour_id) REFERENCES tours(id)
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_tour', methods=['GET', 'POST'])
def add_tour():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        price = request.form['price']
        
        conn = sqlite3.connect("tourism.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tours (name, location, price) VALUES (?, ?, ?)", (name, location, price))
        conn.commit()
        conn.close()
        return redirect(url_for('view_tours'))
    return render_template('add_tour.html')

@app.route('/view_tours')
def view_tours():
    conn = sqlite3.connect("tourism.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tours")
    tours = cursor.fetchall()
    conn.close()
    return render_template('view_tours.html', tours=tours)

@app.route('/book_tour', methods=['GET', 'POST'])
def book_tour():
    conn = sqlite3.connect("tourism.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tours")
    tours = cursor.fetchall()
    conn.close()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        tour_id = request.form['tour_id']
        
        conn = sqlite3.connect("tourism.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bookings (name, email, tour_id) VALUES (?, ?, ?)", (name, email, tour_id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_bookings'))
    
    return render_template('book_tour.html', tours=tours)

@app.route('/view_bookings')
def view_bookings():
    conn = sqlite3.connect("tourism.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT bookings.id, bookings.name, bookings.email, 
               tours.name, tours.location, tours.price 
        FROM bookings 
        JOIN tours ON bookings.tour_id = tours.id
    """)
    bookings = cursor.fetchall()
    conn.close()
    return render_template('view_bookings.html', bookings=bookings)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
