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

# In Memory Storage for the embeddings and metadata
documents = {}

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

    documents[file.filename] = {    # Store the metadata and embeddings in the in-memory storage
        "chunks": page_chunk,
        "embeddings": embeddings
    }

    return {
        "filename": file.filename,
        "saved": path,
        "char_count": len(cleaned_text),
        "preview": cleaned_text[:100],  # Return the first 100 characters as a preview
        "first_chunk": page_chunk[0]
    }

@app.get("/documents")      # Endpoint to retrieve the list of uploaded documents along with their metadata (filename and embeddings shape)
def get_document():
    return {
        "uploaded_documents": list(documents.keys())
    }

@app.get("/documents/{filename}")   # Endpoint to retrieve the metadata and embeddings for a specific document based on its filename
def get_document_by_filename(filename: str):
    if filename not in documents:
        return {"error": "File not found"}
    return {
        "filename": filename,
        "embeddings": list(documents[filename]["embeddings"].shape),  # Convert numpy array to list for JSON serialization
    }


# Upload pdf
# save pdf
# extract text from pdf
# clean text
# chunking of text
# creating embeddings for each chunk
# store it in memory / db
# chatting system