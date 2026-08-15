from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

# Import the logic from your existing LangChain script
# We will modify that script slightly in the next step so it can be imported cleanly.
from mysql_text_to_sql_starter_code import run_text_to_sql

app = FastAPI()

# Allow the frontend to talk to the backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any frontend during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the structure of the incoming data
class QueryRequest(BaseModel):
    question: str

# Define the API endpoint
@app.post("/api/ask")
async def ask_database(request: QueryRequest):
    try:
        print(f"Received question: {request.question}")
        # Call the LangChain function
        result = run_text_to_sql(request.question)
        
        # Return the generated SQL and the data
        return {
            "sql_query": result["sql_query"],
            "data": result["data"]
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Start the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)