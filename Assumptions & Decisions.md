# Assumptions & Decisions

## Assumptions

1. **SQLite** is used as the database for simplicity.
   - **Validation Plan:** Test database queries locally and ensure data persistence via `database.py`.

2. Each **event belongs to a college**, represented by `college_id`.
   - **Validation Plan:** Pass `college_id` to `POST /events` and confirm proper filtering.

3. **One feedback per student per event** will be enforced in future updates.
   - **Validation Plan:** Plan to add a unique constraint later.

4. **Authentication & user roles** are postponed to Phase 2 (not included in the prototype).
   - **Validation Plan:** Document requirement and test using mock data only.

=======
1. Using **SQLite** as the database for simplicity.
   - **Validation Plan:** Test DB queries locally and ensure persistence in `database.py`.

2. Each **event belongs to a college**, represented by `college_id`.
   - **Validation Plan:** Pass `college_id` to `POST /events` and confirm filtering works.

3. **One feedback per student per event** will be enforced in future updates.
   - **Validation Plan:** Plan to add a unique constraint later.

4. **Authentication & user roles** are postponed to Phase 2 (not in prototype).
   - **Validation Plan:** Document requirement and test with mock data only.



## Decisions

- Chose **FastAPI + SQLite** stack for minimal setup and simplicity.
- Built **CRUD APIs** for `events` as the core functionality of the prototype.



## AI Log Evidence

- AI log screenshots are stored in `docs/ai_log` for evidence.
- Screenshots were captured from Swagger UI while testing the `/events` endpoint.
- This validates that the API works as expected and that responses are correctly recorded.


## AI Log Screenshots

![Terminal window displaying FastAPI server startup logs](doc/ai_log/Screenshot%202025-09-07%20103222.png)
![POST request to events endpoint with JSON payload confirming creation](doc/ai_log/Screenshot%202025-09-07%20103234.png)
![GET request to retrieve all events with JSON response](doc/ai_log/Screenshot%202025-09-07%20103242.png)
![PUT request to update an event with confirmation response](doc/ai_log/Screenshot%202025-09-07%20103251.png)
![DELETE request to remove an event with confirmation response](doc/ai_log/Screenshot%202025-09-07%20103256.png)
