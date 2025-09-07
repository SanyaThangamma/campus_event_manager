# database.py
import sqlite3
from sqlite3 import Connection
from typing import List, Tuple

DB_PATH = "events.db"

def get_connection() -> Connection:
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Initialize the database tables."""
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

    # Registrations table (many-to-many relationship)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        student_id INTEGER,
        event_id INTEGER,
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

def insert_dummy_data() -> None:
    """Insert sample data to test the database."""
    conn = get_connection()
    cursor = conn.cursor()

    # Insert events
    cursor.execute("INSERT OR IGNORE INTO events (id, name, date, location, description, college_id) VALUES (?, ?, ?, ?, ?, ?)",
                (1, "Tech Talk", "2025-09-10", "Auditorium", "Talk on latest tech trends", 101))
    cursor.execute("INSERT OR IGNORE INTO events (id, name, date, location, description, college_id) VALUES (?, ?, ?, ?, ?, ?)",
                (2, "Python Workshop", "2025-09-12", "Lab 1", "Hands-on Python workshop", 101))

    # Insert students
    cursor.execute("INSERT OR IGNORE INTO students (id, name, email) VALUES (?, ?, ?)",
                (1, "Alice", "alice@example.com"))
    cursor.execute("INSERT OR IGNORE INTO students (id, name, email) VALUES (?, ?, ?)",
                (2, "Bob", "bob@example.com"))

    # Register students for events
    cursor.execute("INSERT OR IGNORE INTO registrations (student_id, event_id) VALUES (?, ?)", (1, 1))
    cursor.execute("INSERT OR IGNORE INTO registrations (student_id, event_id) VALUES (?, ?)", (2, 1))
    cursor.execute("INSERT OR IGNORE INTO registrations (student_id, event_id) VALUES (?, ?)", (1, 2))

    # Insert feedback
    cursor.execute("INSERT OR IGNORE INTO feedback (student_id, event_id, rating, comments) VALUES (?, ?, ?, ?)",
                (1, 1, 5, "Great event!"))
    cursor.execute("INSERT OR IGNORE INTO feedback (student_id, event_id, rating, comments) VALUES (?, ?, ?, ?)",
                (2, 1, 4, "Informative session"))

    conn.commit()
    conn.close()

def fetch_all_events() -> List[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    conn.close()
    return events

def fetch_all_students() -> List[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return students

def fetch_registrations() -> List[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registrations")
    regs = cursor.fetchall()
    conn.close()
    return regs

def fetch_feedback() -> List[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback")
    feedbacks = cursor.fetchall()
    conn.close()
    return feedbacks

# Initialize DB and insert dummy data (run once)
if __name__ == "__main__":
    init_db()
    insert_dummy_data()
    print("Database initialized and dummy data inserted.")
