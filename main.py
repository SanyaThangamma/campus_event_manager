from fastapi import FastAPI
from pydantic import BaseModel
import database

app = FastAPI(title="Collegia - College Event Manager")

# Models
class Event(BaseModel):
    name: str
    date: str
    location: str
    description: str
    type: str
    college_id: int

class Student(BaseModel):
    name: str
    email: str

class Feedback(BaseModel):
    student_id: int
    event_id: int
    rating: int
    comments: str

# CRUD Events
@app.get("/events")
def get_events():
    return database.fetch_all_events()

@app.post("/events")
def create_event(event: Event):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (name, date, location, description, type, college_id) VALUES (?, ?, ?, ?, ?, ?)",
                (event.name, event.date, event.location, event.description, event.type, event.college_id))
    conn.commit()
    conn.close()
    return {"message": "Event created successfully"}

# CRUD Students
@app.get("/students")
def get_students():
    return database.fetch_all_students()

@app.post("/students")
def create_student(student: Student):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, email) VALUES (?, ?)", (student.name, student.email))
    conn.commit()
    conn.close()
    return {"message": "Student created successfully"}

# Registration
@app.post("/register")
def register(student_id: int, event_id: int):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO registrations (student_id, event_id, attended) VALUES (?, ?, ?)", (student_id, event_id, 0))
    conn.commit()
    conn.close()
    return {"message": "Student registered"}

# Attendance
@app.patch("/attendance")
def mark_attendance(student_id: int, event_id: int):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE registrations SET attended = 1 WHERE student_id = ? AND event_id = ?", (student_id, event_id))
    conn.commit()
    conn.close()
    return {"message": "Attendance marked"}

# Feedback
@app.post("/feedback")
def feedback(feedback: Feedback):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO feedback (student_id, event_id, rating, comments) VALUES (?, ?, ?, ?)",
                (feedback.student_id, feedback.event_id, feedback.rating, feedback.comments))
    conn.commit()
    conn.close()
    return {"message": "Feedback submitted"}

# Reports
@app.get("/reports/registrations")
def registrations_report():
    conn = database.get_connection()
    rows = conn.execute("SELECT event_id, COUNT(*) as total FROM registrations GROUP BY event_id").fetchall()
    conn.close()
    return rows

@app.get("/reports/attendance")
def attendance_report():
    conn = database.get_connection()
    rows = conn.execute("""
        SELECT event_id, ROUND(SUM(attended)*100.0/COUNT(*),2) as percentage
        FROM registrations GROUP BY event_id
    """).fetchall()
    conn.close()
    return rows

@app.get("/reports/feedback")
def feedback_report():
    conn = database.get_connection()
    rows = conn.execute("SELECT event_id, ROUND(AVG(rating),2) as avg_feedback FROM feedback GROUP BY event_id").fetchall()
    conn.close()
    return rows

@app.get("/reports/top_students")
def top_students():
    conn = database.get_connection()
    rows = conn.execute("""
        SELECT s.name, COUNT(r.event_id) as events_attended
        FROM students s
        JOIN registrations r ON s.id = r.student_id
        GROUP BY s.id
        ORDER BY events_attended DESC
        LIMIT 3
    """).fetchall()
    conn.close()
    return rows

@app.get("/reports/event_type")
def filter_by_type(event_type: str):
    conn = database.get_connection()
    rows = conn.execute("SELECT * FROM events WHERE type = ?", (event_type,)).fetchall()
    conn.close()
    return rows
