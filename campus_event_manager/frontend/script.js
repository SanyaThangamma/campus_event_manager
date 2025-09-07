const baseUrl = 'http://127.0.0.1:8000';
let editEventId = null;

// Fetch and display all events
async function fetchEvents() {
    const res = await fetch(`${baseUrl}/events`);
    const events = await res.json();
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
            <p><strong>Location:</strong> ${e.location}</p>
            <p>${e.description}</p>
            <p><strong>College ID:</strong> ${e.college_id}</p>
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
                await fetch(`${baseUrl}/events/${e.id}`, { method: 'DELETE' });
                fetchEvents();
            }
        };

        actions.appendChild(editBtn);
        actions.appendChild(deleteBtn);
        li.appendChild(content);
        li.appendChild(actions);
        list.appendChild(li);
    });
}

// Populate form for editing
function populateFormForEdit(event) {
    editEventId = event.id;
    document.getElementById('name').value = event.name;
    document.getElementById('date').value = event.date;
    document.getElementById('location').value = event.location;
    document.getElementById('description').value = event.description;
    document.getElementById('college_id').value = event.college_id;
}

// Handle event form submission
document.getElementById('eventForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const newEvent = {
        name: document.getElementById('name').value,
        date: document.getElementById('date').value,
        location: document.getElementById('location').value,
        description: document.getElementById('description').value,
        college_id: parseInt(document.getElementById('college_id').value)
    };

    if (editEventId) {
        await fetch(`${baseUrl}/events/${editEventId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newEvent)
        });
        editEventId = null;
    } else {
        await fetch(`${baseUrl}/events`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newEvent)
        });
    }

    fetchEvents();
    e.target.reset();
});

// Handle feedback submission
document.getElementById('feedbackForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const feedbackData = {
        student_name: document.getElementById('student_name').value,
        event_id: parseInt(document.getElementById('event_id').value),
        feedback: document.getElementById('feedback').value
    };

    await fetch(`${baseUrl}/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(feedbackData)
    });

    alert("Feedback submitted!");
    e.target.reset();
});

// Initial fetch
fetchEvents();
