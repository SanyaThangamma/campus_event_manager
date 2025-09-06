# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import database

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

app = FastAPI(title="Campus Event Manager")

@app.on_event("startup")
def startup_event():
    database.init_db()

def row_to_dict(row):
    if row is None:
        return None
    return {k: row[k] for k in row.keys()}

@app.get("/", summary="Root")
def read_root():
    return {"message": "Welcome to Campus Event Manager!"}

@app.get("/events", response_model=List[EventOut], summary="List events")
def list_events(college_id: Optional[int] = None):
    conn = database.get_connection()
    if college_id is not None:
        rows = conn.execute("SELECT * FROM events WHERE college_id = ?", (college_id,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM events").fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]

@app.post("/events", response_model=EventOut, summary="Create event")
def create_event(e: EventCreate):
    conn = database.get_connection()
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

@app.get("/events/{event_id}", response_model=EventOut, summary="Get event by id")
def get_event(event_id: int):
    conn = database.get_connection()
    row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Event not found")
    return row_to_dict(row)

@app.put("/events/{event_id}", response_model=EventOut, summary="Update event")
def update_event(event_id: int, e: EventUpdate):
    conn = database.get_connection()
    row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Event not found")

    # Build update dynamically
    fields = {}
    for field in ["name", "date", "location", "description", "college_id"]:
        val = getattr(e, field)
        if val is not None:
            fields[field] = val

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
    conn = database.get_connection()
    row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Event not found")
    conn.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()
    return {"message": "Event deleted"}
