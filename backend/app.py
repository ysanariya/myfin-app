# app.py
# FastAPI server for MyFin backend
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from parser import parse_hdfc_txt
from db import create_expenses_table, get_connection

# Create FastAPI instance
app = FastAPI()

# Initialize database table
create_expenses_table()

@app.get("/")
def home():
    """
    Home endpoint
    """
    return {"message": "Welcome to MyFin Local Expense Tracker!"}

@app.post("/upload-txt/")
async def upload_txt(file: UploadFile = File(...)):
    try:
        expenses = parse_hdfc_txt(await file.read())
        return {"parsed_rows": expenses[:10], "total_rows": len(expenses)}
    except ValueError as ve:
        return JSONResponse(content={"error": str(ve)}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": f"Unexpected error: {e}"}, status_code=500)