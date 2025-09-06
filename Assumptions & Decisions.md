# Assumptions & Decisions

## Assumptions
1. Using **SQLite** as the database for simplicity.
- Validation Plan: Test DB queries locally and ensure persistence in `database.py`.

2. Each **event belongs to a college**, represented by `college_id`.
- Validation Plan: Pass `college_id` to `POST /events` and confirm filtering works.

3. **One feedback per student per event** will be enforced in future updates.
- Validation Plan: Plan to add unique constraint later.

4. **Authentication & user roles** are postponed to Phase 2 (not in prototype).
- Validation Plan: Document requirement and test with mock data only.

---

## Decisions
- Decided on **FastAPI + SQLite** stack for minimal setup.
- Decided to build **CRUD APIs** for `events` as the prototype’s core.


## AI Log Evidence

- AI log screenshots are stored in `docs/ai_log` for evidence.
- Screenshots were taken from Swagger UI while testing the `/events` endpoint.
- This validates that the API works as expected and responses are being recorded.
