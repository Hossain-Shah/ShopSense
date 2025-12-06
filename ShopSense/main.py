from fastapi import FastAPI, UploadFile, File
import shutil
from ocr import run_ocr
from extract import extract_structured

app = FastAPI()

@app.post("/extract")
async def extract_invoice(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    filepath = f"temp_{file.filename}"
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # OCR
    text = run_ocr(filepath)

    # Extract structured information
    data = extract_structured(text)

    return data
