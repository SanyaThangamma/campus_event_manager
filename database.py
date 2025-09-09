import sqlite3
from sqlite3 import Connection
from typing import List, Dict

DB_PATH = "collegia.db"

# ---------------- DATABASE CONNECTION ----------------
def get_connection() -> Connection:
    """
    Returns a SQLite connection object with row_factory set to Row
    so that results can be accessed like dictionaries.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- INITIALIZATION ----------------
def init_db() -> None:
    """Create tables if they do not exist"""
    conn = get_connection()
    cursor = conn.cursor()

    # Events table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        location TEXT,
        description TEXT,
        type TEXT,
        college_id INTEGER
    )
    """)

    # Students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    """)

    # Registrations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        student_id INTEGER,
        event_id INTEGER,
        attended INTEGER DEFAULT 0,
        PRIMARY KEY (student_id, event_id),
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
        FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
    )
    """)

    # Feedback table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        student_id INTEGER,
        event_id INTEGER,
        rating INTEGER CHECK(rating BETWEEN 1 AND 5),
        comments TEXT,
        PRIMARY KEY (student_id, event_id),
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
        FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

# ---------------- DUMMY DATA ----------------
def insert_dummy_data() -> None:
    """Insert some sample events, students, registrations, and feedback"""
    conn = get_connection()
    cursor = conn.cursor()

    # Events
    cursor.execute("""INSERT OR IGNORE INTO events (id, name, date, location, description, type, college_id)
                      VALUES (1, "Tech Talk", "2025-09-10", "Auditorium", "Talk on latest tech trends", "Seminar", 101)""")
    cursor.execute("""INSERT OR IGNORE INTO events (id, name, date, location, description, type, college_id)
                      VALUES (2, "Python Workshop", "2025-09-12", "Lab 1", "Hands-on Python workshop", "Workshop", 101)""")

    # Students
    cursor.execute("""INSERT OR IGNORE INTO students (id, name, email) VALUES (1, "Alice", "alice@example.com")""")
    cursor.execute("""INSERT OR IGNORE INTO students (id, name, email) VALUES (2, "Bob", "bob@example.com")""")

    # Registrations
    cursor.execute("INSERT OR IGNORE INTO registrations (student_id, event_id, attended) VALUES (1, 1, 1)")
    cursor.execute("INSERT OR IGNORE INTO registrations (student_id, event_id, attended) VALUES (2, 1, 0)")
    cursor.execute("INSERT OR IGNORE INTO registrations (student_id, event_id, attended) VALUES (1, 2, 1)")

    # Feedback
    cursor.execute("INSERT OR IGNORE INTO feedback (student_id, event_id, rating, comments) VALUES (1, 1, 5, 'Great event!')")
    cursor.execute("INSERT OR IGNORE INTO feedback (student_id, event_id, rating, comments) VALUES (2, 1, 4, 'Informative session')")

    conn.commit()
    conn.close()
    print("Dummy data inserted successfully.")

# ---------------- FETCH FUNCTIONS ----------------
def fetch_all_events() -> List[Dict]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM events").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def fetch_all_students() -> List[Dict]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ---------------- MAIN ----------------
if __name__ == "__main__":
    init_db()
    insert_dummy_data()
