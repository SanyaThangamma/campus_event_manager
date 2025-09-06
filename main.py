from fastapi import FastAPI

app = FastAPI(title="Campus Event Manager")

@app.get("/")
def read_root():
    return {"message": "Welcome to Campus Event Manager!"}
