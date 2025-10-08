# app.py
# FastAPI server for MyFin backend
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from parser import parse_hdfc_txt
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Add this
templates = Jinja2Templates(directory="templates")
#app.mount("/static", StaticFiles(directory="backend/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload-txt/")
async def upload_txt(file: UploadFile = File(...)):
    try:
        expenses = parse_hdfc_txt(await file.read())
        return {"parsed_rows": expenses[:10], "total_rows": len(expenses)}
    except ValueError as ve:
        return JSONResponse(content={"error": str(ve)}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": f"Unexpected error: {e}"}, status_code=500)