# main.py - FastAPI application: defines routes for homepage and spam prediction

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from app.predictor import predict_email
import os

app = FastAPI(title="Spam Classifier")


# Mount the static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the static frontend page
@app.get("/", response_class=HTMLResponse)
def homepage():
    index_path = os.path.join("static", "index.html")
    if not os.path.exists(index_path):
        return HTMLResponse("<h3>index.html not found</h3>", status_code=500)
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# Accept POST requests for spam prediction
@app.post("/predict")
async def predict(request: Request):
    # Try to parse JSON body, fallback to form data
    try:
        payload = await request.json()
    except:
        form = await request.form()
        payload = dict(form)

    text = payload.get("text")
    subject = payload.get("subject")

    if not text:
        return JSONResponse({"error": "No 'text' provided"}, status_code=400)

    try:
        # Call helper function to predict spam
        return predict_email(text, subject)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
