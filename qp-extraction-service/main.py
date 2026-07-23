import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from pipeline.preprocessing import preprocess_document
from pipeline.layout import run_layout_detection

load_dotenv()
app = FastAPI()

class PreprocessRequest(BaseModel):
    filePath: str
    documentId: str

class LayoutRequest(BaseModel):
    documentId: str
    pages: List[Dict]

@app.post("/preprocess")
def preprocess(req: PreprocessRequest):
    pages = preprocess_document(req.filePath, req.documentId, os.getenv("STORAGE_PATH"), dpi=300)
    return {"documentId": req.documentId, "pages": pages}

@app.post("/detect-layout")
def detect_layout(req: LayoutRequest):
    results = run_layout_detection(req.pages, req.documentId, os.getenv("STORAGE_PATH"))
    return {"documentId": req.documentId, "layout": results}