// Base URL of the FastAPI backend
const baseUrl = 'http://127.0.0.1:8000';  
let editEventId = null;

// ---------------- FETCH AND DISPLAY EVENTS ----------------
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
            content.classList.add('card-content');
            content.innerHTML = `
                <h3>${e.name}</h3>
                <p><strong>Date:</strong> ${e.date}</p>
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
                    try {
                        const delRes = await fetch(`${baseUrl}/events/${e.id}`, { method: 'DELETE' });
                        if (delRes.ok) fetchEvents();
                        else alert("Failed to delete event.");
                    } catch (err) {
                        console.error("Error deleting event:", err);
                    }
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

// ---------------- POPULATE FORM FOR EDITING ----------------
function populateFormForEdit(event) {
    editEventId = event.id;
    document.getElementById('name').value = event.name;
    document.getElementById('date').value = event.date;
    document.getElementById('location').value = event.location;
    document.getElementById('description').value = event.description;
    document.getElementById('college_id').value = event.college_id;
}

// ---------------- HANDLE EVENT FORM SUBMISSION ----------------
document.getElementById('eventForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const newEvent = {
        name: document.getElementById('name').value,
        date: document.getElementById('date').value,
        location: document.getElementById('location').value,
        description: document.getElementById('description').value,
        college_id: parseInt(document.getElementById('college_id').value),
        type: "General"  // Default type
    };

    try {
        let res;
        if (editEventId) {
            res = await fetch(`${baseUrl}/events/${editEventId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newEvent)
            });
            editEventId = null;
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

// ---------------- HANDLE FEEDBACK FORM SUBMISSION ----------------
document.getElementById('feedbackForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const feedbackData = {
        student_id: 1, // TODO: replace with actual logged-in student
        event_id: parseInt(document.getElementById('event_id').value),
        rating: 5,     // Default rating
        comments: document.getElementById('feedback').value
    };

    try {
        const res = await fetch(`${baseUrl}/feedback`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(feedbackData)
        });
        if (res.ok) {
            alert("Feedback submitted!");
            e.target.reset();
        } else {
            alert("Failed to submit feedback!");
        }
    } catch (err) {
        console.error("Error submitting feedback:", err);
    }
});

// ---------------- INITIAL FETCH ----------------
fetchEvents();
