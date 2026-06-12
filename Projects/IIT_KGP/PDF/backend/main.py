# pip install fastapi uvicorn
# pip install python-multipart pypdf
#pip install sentence-transformers
# Command to run the server: uvicorn main:app --reload

import os
from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import re

app = FastAPI()

#model call
model = SentenceTransformer('all-MiniLM-L6-v2')  # Load the pre-trained model for generating embeddings

# cleaning the text by removing extra spaces and newlines, and stripping leading/trailing whitespace
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with a single space
    return text.strip()

# chunking the text into smaller parts to make it easier to process. The chunk size and overlap can be adjusted based on the use case.
def chunk(text,chunk_size=1000, chunk_overlap=200):     # chunk_overlap is the number of characters that will be repeated in the next chunk to maintain context
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

@app.get("/health")
def health_check():
    return {"Message": "Server is running"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    # save pdf in upload folder
    path = os.path.join("upload", file.filename)
    with open(path, "wb") as f:
        f.write(await file.read())

    pdf_reader = PdfReader(path)

    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    cleaned_text = clean_text(text)
    page_chunk = chunk(cleaned_text)
    embeddings = model.encode(page_chunk)  # Generate embeddings for each chunk of text

    return {
        "filename": file.filename,
        "saved": path,
        "char_count": len(cleaned_text),
        "preview": cleaned_text[:100],  # Return the first 100 characters as a preview
        "first_chunk": page_chunk[0]
    }