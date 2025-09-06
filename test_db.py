from database import fetch_all_events, fetch_all_students, fetch_registrations, fetch_feedback

print("Events:")
for e in fetch_all_events():
    print(dict(e))

print("\nStudents:")
for s in fetch_all_students():
    print(dict(s))

print("\nRegistrations:")
for r in fetch_registrations():
    print(dict(r))

print("\nFeedback:")
for f in fetch_feedback():
    print(dict(f))
