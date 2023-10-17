from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import shutil
from pathlib import Path

app = FastAPI()

origins = [
    "http://localhost", 
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class File(BaseModel):
    course: str
    date: str

@app.post('/api/image')
async def get_image(image: UploadFile):
    upload_dir = Path("uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Create a unique filename for the uploaded image
    image_path = upload_dir / image.filename

    with image_path.open("wb") as image_file:
        shutil.copyfileobj(image.file, image_file)

    return {"message": "Image uploaded successfully"}

@app.post('/api/submit', tags=["form"])
async def get_formData(file: File):
    print(file)

@app.get("/api/data")
def get_json_data():
    data = {
        "key1": "value1",
        "key2": "value2",
        # Add more data as needed
    }
    return data
