# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sqlite3

# ----- Database setup -----
DB_NAME = "events.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        location TEXT,
        description TEXT,
        college_id INTEGER
    )
    """)
    conn.commit()
    conn.close()

def fetch_all_events():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM events").fetchall()
    conn.close()
    return rows

# ----- Pydantic Models -----
class EventCreate(BaseModel):
    name: str
    date: str
    location: Optional[str] = ""
    description: Optional[str] = ""
    college_id: Optional[int] = None

class EventUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    college_id: Optional[int] = None

class EventOut(BaseModel):
    id: int
    name: str
    date: str
    location: Optional[str] = None
    description: Optional[str] = None
    college_id: Optional[int] = None

# ----- FastAPI App -----
app = FastAPI(title="Campus Event Manager")

# --- CORS middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (good for testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Initialize DB on startup -----
@app.on_event("startup")
def startup_event():
    init_db()

# ----- Helper -----
def row_to_dict(row):
    if row is None:
        return None
    return {k: row[k] for k in row.keys()}

# ----- Routes -----
@app.get("/", summary="Root")
def read_root():
    return {"message": "Welcome to Campus Event Manager!"}

@app.get("/events", response_model=List[EventOut], summary="List all events")
def list_events(college_id: Optional[int] = None):
    events = fetch_all_events()
    if college_id is not None:
        events = [e for e in events if e["college_id"] == college_id]
    return [dict(e) for e in events]

@app.post("/events", response_model=EventOut, summary="Create event")
def create_event(e: EventCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO events (name, date, location, description, college_id) VALUES (?, ?, ?, ?, ?)",
        (e.name, e.date, e.location, e.description, e.college_id),
    )
    conn.commit()
    event_id = cur.lastrowid
    row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    conn.close()
    return row_to_dict(row)

@app.get("/events/{event_id}", response_model=EventOut, summary="Get event by ID")
def get_event(event_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Event not found")
    return row_to_dict(row)

@app.put("/events/{event_id}", response_model=EventOut, summary="Update event")
def update_event(event_id: int, e: EventUpdate):
    conn = get_connection()
    row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Event not found")

    # Dynamically update fields
    fields = {f: getattr(e, f) for f in ["name", "date", "location", "description", "college_id"] if getattr(e, f) is not None}
    if fields:
        set_clause = ", ".join([f"{k} = ?" for k in fields.keys()])
        params = list(fields.values()) + [event_id]
        conn.execute(f"UPDATE events SET {set_clause} WHERE id = ?", params)
        conn.commit()

    row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    conn.close()
    return row_to_dict(row)

@app.delete("/events/{event_id}", summary="Delete event")
def delete_event(event_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Event not found")
    conn.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()
    return {"message": "Event deleted successfully"}