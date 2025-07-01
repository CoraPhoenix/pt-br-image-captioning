import torch
import io
from PIL import Image
from fastapi import FastAPI, UploadFile, File
from transformers import pipeline
from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)
import asyncio

app = FastAPI()

processor = BlipProcessor.from_pretrained('./captioning/fine_tuned_model')
model = BlipForConditionalGeneration.from_pretrained('./captioning/fine_tuned_model')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

@app.post("/generate_caption")
async def generate_caption(img: UploadFile = File(...)):
    # get image bytes
    image_bytes = await img.read()
    # converts bytes to a PIL object and process it
    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    inputs = processor(pil_img, return_tensors="pt").to(device)

    # generate the caption
    with torch.no_grad():
        ids = model.generate(**inputs, max_new_tokens=30)

    caption = processor.decode(ids[0], skip_special_tokens=True)
    return {"caption": caption}