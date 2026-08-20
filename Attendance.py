from flask import Flask, render_template, request, redirect
import sqlite3, os

app= Flask(__name__)
DB_PATH = "data/attendance.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY, user TEXT, date TEXT, status TEXT)")
    

    c.execute("SELECT COUNT(*) from attendance")
    if c.fetchone()[0] == 0:
        sample_records = [ 
            ("Nour", "2026-08-06", "present"),
            ("Asser", "2026-08-09", "Absent"),
            ("moaz", "2026-08-07", "Present")
        ]
        c.executemany("INSERT INTO attendance (user, date, status) VALUES (?, ?, ?)", sample_records)
    conn.commit()
    conn.close()

@app.route('/')
def login():
    return render_template ("login.html")   

@app.route('/mark', methods=['POST'])
def mark():
     user = request.form['user']
     date = request.form['date']
     status = request.form['status']
     conn = sqlite3.connect(DB_PATH)
     c = conn.cursor()
     c.execute("INSERT INTO attendance (user, date, status)  VALUES(?, ?, ?)", (user, date, status))
     conn.commit()
     conn.close()
     return redirect('/history')

@app.route('/history')
def history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM attendance")
    records = c.fetchall()
    conn.close()
    return render_template('history.html', records=records)


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT",5000))
    app.run(debug=True, host='0.0.0.0', port=port)