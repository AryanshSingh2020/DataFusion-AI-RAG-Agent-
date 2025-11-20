# backend/app/api/endpoints/query.py
from fastapi import APIRouter, HTTPException
from ...models.pydantic_models import QueryRequest, ApiResponse
from ...services.rag_agent import process_query

router = APIRouter()

@router.post("/", response_model=ApiResponse)
async def handle_user_query(request: QueryRequest):
    """
    Receives a natural language query from the user, processes it using the RAG agent,
    and returns a structured response for the frontend to render.
    """
    if not request.question:
        raise HTTPException(status_code=400, detail="Query question cannot be empty.")
    try:
        result = await process_query(request.question)
        return result
    except Exception as e:
        # This is a general catch-all. In production, you'd have more specific error handling.
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")