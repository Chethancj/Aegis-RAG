from fastapi import FastAPI

app = FastAPI(
    title="AegisRAG",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "project": "AegisRAG",
        "status": "running"
    }