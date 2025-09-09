🎓Collegia-Campus Event Managemnet System

Collegia is a full-feautured web application designed to streamline the management of college events.It allows administrators to create, update and manage events , while students can register, provide feedback
and track event participation. Built with FastAPI, SQLite and a modern React frontend, Collegia emphasizes simplicity, usability and efficiency.

✨Key Features:
1) Event MAnagemnt (create , update, delete, list)
2) Student registration and participation tracking
3) Feedback collection per event
4) Multi-tenant support for handling multiple colleges
5) RESTful APIs for easy integration with the frontend or other services
6) Clean and intuitive user interface

🛠️Tech Stack:
1) Backend - Python, FastAPI, SQLite
2) Frontend - React.js
3) Version Control - Git & GitHub
4) Environment Managemnt - Python Virtual environment(venv)
5) Other Tools/Libraries:
    -> pydantic - fr data validation
    -> SQAlchemy - for database interactions
    -> Axios(frontend) - for API requests

⚙️How it Works:
1) Admin Side :
   ->Admins can log in and manage events
   ->They can view all registered students and collected feedback

2)Student Side:
   ->Stduents can browse upcoming events and registeer for them.
   ->They can submit feedback after attending events.

3)APIs:
   ->Backend exposes RESTful APIs for event , student, registration and feedback management.
   ->Frontend consumes these PIs to provide a dynamic user experience.

4)Database:
   ->SQLite is used for lightweight storage.
   ->Each event and registration is associated with a college ID to support multi-tenancy.

🚀Installation & Setup:

1)Clone the repository:
    git clone <repo-url>
    cd campus_event_manager

2)Set up virtual environment and activate:
    python -m venv venv
    source venv/bin/activate   # Linux/macOS
    venv\Scripts\activate      # Windows

3)Install dependencies:
    pip install -r requirements.txt

4)Run the backend server:
    uvicorn main:app --reload


5)Frontend:
    npm install
    npm start

6)Access the app:
    Frontend: http://localhost:3000
    API Docs: http://127.0.0.1:8000/docs
