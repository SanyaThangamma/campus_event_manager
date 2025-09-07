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



## Decisions

- Chose **FastAPI + SQLite** stack for minimal setup and simplicity.
- Built **CRUD APIs** for `events` as the core functionality of the prototype.



## AI Log Evidence

- AI log screenshots are stored in `docs/ai_log` for evidence.
- Screenshots were captured from Swagger UI while testing the `/events` endpoint.
- This validates that the API works as expected and that responses are correctly recorded.

