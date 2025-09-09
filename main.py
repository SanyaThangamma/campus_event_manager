from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import database
from typing import List, Dict

# ---------------- FastAPI App ----------------
app = FastAPI(title="Collegia - College Event Manager")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local testing, allows any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Models ----------------
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

# ---------------- CRUD EVENTS ----------------
@app.get("/events", response_model=List[Dict])
def get_events():
    return database.fetch_all_events()

@app.post("/events")
def create_event(event: Event):
    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO events (name, date, location, description, type, college_id) VALUES (?, ?, ?, ?, ?, ?)",
            (event.name, event.date, event.location, event.description, event.type, event.college_id)
        )
        conn.commit()
        event_id = cursor.lastrowid
    return {**event.dict(), "id": event_id, "message": "Event created successfully"}

# ---------------- CRUD STUDENTS ----------------
@app.get("/students", response_model=List[Dict])
def get_students():
    return database.fetch_all_students()

@app.post("/students")
def create_student(student: Student):
    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, email) VALUES (?, ?)", (student.name, student.email))
        conn.commit()
        student_id = cursor.lastrowid
    return {"id": student_id, **student.dict(), "message": "Student created successfully"}

# ---------------- REGISTRATION ----------------
@app.post("/register")
def register(student_id: int, event_id: int):
    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO registrations (student_id, event_id, attended) VALUES (?, ?, ?)",
            (student_id, event_id, 0)
        )
        conn.commit()
    return {"message": "Student registered"}

# ---------------- ATTENDANCE ----------------
@app.patch("/attendance")
def mark_attendance(student_id: int, event_id: int):
    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE registrations SET attended = 1 WHERE student_id = ? AND event_id = ?",
            (student_id, event_id)
        )
        conn.commit()
    return {"message": "Attendance marked"}

# ---------------- FEEDBACK ----------------
@app.post("/feedback")
def feedback(feedback: Feedback):
    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO feedback (student_id, event_id, rating, comments) VALUES (?, ?, ?, ?)",
            (feedback.student_id, feedback.event_id, feedback.rating, feedback.comments)
        )
        conn.commit()
    return {"message": "Feedback submitted"}

# ---------------- REPORTS ----------------
@app.get("/reports/registrations", response_model=List[Dict])
def registrations_report():
    with database.get_connection() as conn:
        rows = conn.execute("SELECT event_id, COUNT(*) as total FROM registrations GROUP BY event_id").fetchall()
    return [{"event_id": row[0], "total_registrations": row[1]} for row in rows]

@app.get("/reports/attendance", response_model=List[Dict])
def attendance_report():
    with database.get_connection() as conn:
        rows = conn.execute("""
            SELECT event_id, ROUND(SUM(attended)*100.0/COUNT(*),2) as percentage
            FROM registrations GROUP BY event_id
        """).fetchall()
    return [{"event_id": row[0], "attendance_percentage": row[1]} for row in rows]

@app.get("/reports/feedback", response_model=List[Dict])
def feedback_report():
    with database.get_connection() as conn:
        rows = conn.execute(
            "SELECT event_id, ROUND(AVG(rating),2) as avg_feedback FROM feedback GROUP BY event_id"
        ).fetchall()
    return [{"event_id": row[0], "avg_feedback": row[1]} for row in rows]

@app.get("/reports/top_students", response_model=List[Dict])
def top_students():
    with database.get_connection() as conn:
        rows = conn.execute("""
            SELECT s.name, COUNT(r.event_id) as events_attended
            FROM students s
            JOIN registrations r ON s.id = r.student_id
            GROUP BY s.id
            ORDER BY events_attended DESC
            LIMIT 3
        """).fetchall()
    return [{"name": row[0], "events_attended": row[1]} for row in rows]

@app.get("/reports/event_type", response_model=List[Dict])
def filter_by_type(event_type: str):
    with database.get_connection() as conn:
        rows = conn.execute("SELECT * FROM events WHERE type = ?", (event_type,)).fetchall()
    return [
        {
            "id": row[0],
            "name": row[1],
            "date": row[2],
            "location": row[3],
            "description": row[4],
            "type": row[5],
            "college_id": row[6]
        } for row in rows
    ]
