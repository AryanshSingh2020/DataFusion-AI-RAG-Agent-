# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints import query

app = FastAPI(
    title="Valuefy RAG Agent API",
    description="API for querying financial data using natural language.",
    version="1.0.0"
)

# --- CORS Middleware ---
# This allows your React frontend (running on a different port) to communicate with this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # The origin of your React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include API Routers ---
app.include_router(query.router, prefix="/api/query", tags=["Query"])

@app.get("/", tags=["Root"])
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "Welcome to the Valuefy RAG Agent API!"}