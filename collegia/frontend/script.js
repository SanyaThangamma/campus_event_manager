const baseUrl = 'http://127.0.0.1:8000';
let editEventId = null;

// ---------------- NAVIGATION ----------------
document.querySelectorAll(".nav-links a").forEach(link => {
    link.addEventListener("click", (e) => {
        e.preventDefault();

        // Hide all sections
        document.querySelectorAll(".main-content section").forEach(sec => sec.style.display = "none");

        // Show selected section
        document.querySelector(link.getAttribute("href")).style.display = "block";

        // Update active link
        document.querySelectorAll(".nav-links a").forEach(a => a.classList.remove("active"));
        link.classList.add("active");
    });
});

// ---------------- FETCH EVENTS ----------------
async function fetchEvents() {
    try {
        const res = await fetch(`${baseUrl}/events`);
        const events = await res.json() || [];
        const list = document.getElementById('eventsList');
        list.innerHTML = '';

        events.forEach(e => {
            const li = document.createElement('li');
            li.classList.add('event-card');

            const content = document.createElement('div');
            content.innerHTML = `
                <h3>${e.name}</h3>
                <p><strong>Date:</strong> ${new Date(e.date).toLocaleDateString()}</p>
                <p><strong>Location:</strong> ${e.location || '-'}</p>
                <p>${e.description || ''}</p>
                <p><strong>College ID:</strong> ${e.college_id}</p>
                <p><strong>Type:</strong> ${e.type}</p>
            `;

            const actions = document.createElement('div');
            actions.classList.add('card-actions');

            const editBtn = document.createElement('button');
            editBtn.textContent = 'Edit';
            editBtn.onclick = () => populateFormForEdit(e);

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Delete';
            deleteBtn.onclick = async () => {
                if (confirm(`Delete event "${e.name}"?`)) {
                    const delRes = await fetch(`${baseUrl}/events/${e.id}`, { method: 'DELETE' });
                    if (delRes.ok) fetchEvents();
                    else alert("Failed to delete event.");
                }
            };

            actions.appendChild(editBtn);
            actions.appendChild(deleteBtn);
            li.appendChild(content);
            li.appendChild(actions);
            list.appendChild(li);
        });
    } catch (err) {
        console.error("Error fetching events:", err);
    }
}

// ---------------- EDIT EVENT ----------------
function populateFormForEdit(event) {
    editEventId = event.id;
    document.getElementById('name').value = event.name;
    document.getElementById('date').value = event.date.split("T")[0];
    document.getElementById('location').value = event.location;
    document.getElementById('description').value = event.description;
    document.getElementById('college_id').value = event.college_id;
    document.getElementById('type').value = event.type;
    document.querySelector('#eventForm button').textContent = "Update Event";
}

// ---------------- SAVE EVENT ----------------
document.getElementById('eventForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const newEvent = {
        name: document.getElementById('name').value,
        date: document.getElementById('date').value,
        location: document.getElementById('location').value,
        description: document.getElementById('description').value,
        college_id: parseInt(document.getElementById('college_id').value),
        type: document.getElementById('type').value
    };

    // Validation: prevent past dates
    if (new Date(newEvent.date) < new Date()) {
        alert("Date cannot be in the past!");
        return;
    }

    try {
        let res;
        if (editEventId) {
            res = await fetch(`${baseUrl}/events/${editEventId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newEvent)
            });
            editEventId = null;
            document.querySelector('#eventForm button').textContent = "Save Event";
        } else {
            res = await fetch(`${baseUrl}/events`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newEvent)
            });
        }

        if (res.ok) {
            fetchEvents();
            e.target.reset();
        } else {
            alert("Failed to save event!");
        }
    } catch (err) {
        console.error("Error saving event:", err);
    }
});

// ---------------- FETCH STUDENTS ----------------
async function fetchStudents() {
    try {
        const res = await fetch(`${baseUrl}/students`);
        const students = await res.json() || [];
        const list = document.getElementById('studentsList');
        list.innerHTML = '';

        students.forEach(s => {
            const li = document.createElement('li');
            li.textContent = `${s.id}. ${s.name} (${s.email})`;
            list.appendChild(li);
        });
    } catch (err) {
        console.error("Error fetching students:", err);
    }
}

// ---------------- ADD STUDENT ----------------
document.getElementById('studentForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const newStudent = {
        name: document.getElementById('student_name').value,
        email: document.getElementById('student_email').value
    };

    try {
        const res = await fetch(`${baseUrl}/students`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newStudent)
        });

        if (res.ok) {
            fetchStudents();
            e.target.reset();
        } else {
            const errorData = await res.json();
            alert(`Failed to add student: ${errorData.detail || 'Unknown error'}`);
        }
    } catch (err) {
        console.error("Error adding student:", err);
    }
});

// ---------------- SUBMIT FEEDBACK ----------------
document.getElementById('feedbackForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const feedbackData = {
        student_id: parseInt(document.getElementById('student_id').value),
        event_id: parseInt(document.getElementById('event_id').value),
        rating: parseInt(document.getElementById('rating').value),
        comments: document.getElementById('comments').value
    };

    try {
        const res = await fetch(`${baseUrl}/feedback`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(feedbackData)
        });

        if (res.ok) {
            document.getElementById('feedbackMsg').textContent = "✅ Feedback submitted!";
            e.target.reset();
        } else {
            document.getElementById('feedbackMsg').textContent = "❌ Failed to submit feedback!";
        }
    } catch (err) {
        console.error("Error submitting feedback:", err);
    }
});

// ---------------- INITIAL LOAD ----------------
fetchEvents();
fetchStudents();
