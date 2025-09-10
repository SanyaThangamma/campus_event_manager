// Base URL of the FastAPI backend
const baseUrl = "http://127.0.0.1:8000";

// ---------------- FETCH EVENTS ----------------
async function loadEvents() {
const res = await fetch(`${baseUrl}/events`);
const events = await res.json();
const list = document.getElementById("eventList");
list.innerHTML = "";

events.forEach(event => {
    const li = document.createElement("li");
    li.innerHTML = `
    <h3>${event.name}</h3>
    <p>${event.date} - ${event.location}</p>
    <p>${event.description}</p>
    <small>Type: ${event.type}</small>
    `;
    list.appendChild(li);
});
}

// ---------------- FETCH STUDENTS ----------------
async function loadStudents() {
const res = await fetch(`${baseUrl}/students`);
const students = await res.json();
const list = document.getElementById("studentList");
list.innerHTML = "";

students.forEach(student => {
    const li = document.createElement("li");
    li.innerHTML = `
    <h3>${student.name}</h3>
    <p>${student.email}</p>
    `;
    list.appendChild(li);
});
}

// ---------------- FETCH STATS ----------------
async function fetchStats() {
try {
    // Events
    const eventsRes = await fetch(`${baseUrl}/events`);
    const events = await eventsRes.json();
    document.getElementById("statEvents").textContent = events.length;

    // Students
    const studentsRes = await fetch(`${baseUrl}/students`);
    const students = await studentsRes.json();
    document.getElementById("statStudents").textContent = students.length;

    // Registrations
    const regRes = await fetch(`${baseUrl}/reports/registrations`);
    const registrations = await regRes.json();
    const totalRegs = registrations.reduce((sum, r) => sum + r.total_registrations, 0);
    document.getElementById("statRegistrations").textContent = totalRegs;

    // Feedback
    const feedbackRes = await fetch(`${baseUrl}/reports/feedback`);
    const feedback = await feedbackRes.json();
    const avgFeedback = feedback.length
    ? (feedback.reduce((sum, f) => sum + f.avg_feedback, 0) / feedback.length).toFixed(1)
    : 0;
    document.getElementById("statFeedback").textContent = avgFeedback;
} catch (err) {
    console.error("Error fetching stats:", err);
}
}

// ---------------- FORM HANDLERS ----------------
document.getElementById("eventForm").addEventListener("submit", async (e) => {
e.preventDefault();
const data = {
    name: document.getElementById("eventName").value,
    date: document.getElementById("eventDate").value,
    location: document.getElementById("eventLocation").value,
    description: document.getElementById("eventDescription").value,
    type: document.getElementById("eventType").value,
    college_id: parseInt(document.getElementById("eventCollegeId").value)
};

await fetch(`${baseUrl}/events`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
});

loadEvents();
fetchStats();
e.target.reset();
});

document.getElementById("studentForm").addEventListener("submit", async (e) => {
e.preventDefault();
const data = {
    name: document.getElementById("studentName").value,
    email: document.getElementById("studentEmail").value
};

await fetch(`${baseUrl}/students`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
});

loadStudents();
fetchStats();
e.target.reset();
});

// ---------------- INIT ----------------
loadEvents();
loadStudents();
fetchStats();
