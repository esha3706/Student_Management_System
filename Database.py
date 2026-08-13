import sqlite3
def create_database():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    # Admin Login Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)
    # Student Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        gender TEXT,
        age INTEGER,
        course TEXT,
        phone TEXT,
        email TEXT,
        address TEXT
    )
    """)
    # Default Admin Account
    cursor.execute(
        "SELECT * FROM admin WHERE email=?",
        ("esha@gmail.com",)
    )
    if cursor.fetchone() is None:
        cursor.execute("""
        INSERT INTO admin(email,password)
        VALUES(?,?)
        """,
        ("esha@gmail.com","Esha@123")
        )
    conn.commit()
    conn.close()