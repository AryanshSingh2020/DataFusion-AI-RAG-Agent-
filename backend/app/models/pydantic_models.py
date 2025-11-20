# backend/app/models/pydantic_models.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Union

class QueryRequest(BaseModel):
    """API Request model for an incoming user query."""
    question: str
    history: List[Dict[str, str]] = [] # To support conversational follow-ups

class ChartData(BaseModel):
    """Data model for a chart."""
    type: str = Field(..., description="Type of chart, e.g., 'pie', 'bar', 'line'")
    data: List[Dict[str, Any]] = Field(..., description="Data points for the chart. Example: [{'name': 'Sector A', 'value': 400}]")

class TableData(BaseModel):
    """Data model for a table."""
    headers: List[str] = Field(..., description="List of column headers")
    rows: List[List[Any]] = Field(..., description="List of rows, where each row is a list of cell values")

class TextData(BaseModel):
    """Data model for a simple text response."""
    answer: str = Field(..., description="The plain text answer to the user's query.")

class ApiResponse(BaseModel):
    """The final structured response from the API."""
    type: str = Field(..., description="The type of content in the response: 'text', 'table', or 'chart'")
    content: Union[TextData, TableData, ChartData]