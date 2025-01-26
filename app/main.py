import whisper
import torch
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import tempfile
import os

# Load Whisper model
model = whisper.load_model("medium")

app = FastAPI()

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        # Transcribe audio
        result = model.transcribe(temp_file_path)
        
        return JSONResponse(content={
            "text": result["text"],
            "language": result.get("language", "unknown")
        })
    
    finally:
        # Clean up temporary file
        os.unlink(temp_file_path)

# Optional: GPU check
@app.get("/gpu_check")
def check_gpu():
    return {
        "cuda_available": torch.cuda.is_available(),
        "cuda_device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    }