# pip install fastapi uvicorn
# pip install python-multipart pypdf
#pip install sentence-transformers
# Command to run the server: uvicorn main:app --reload
# qdarnt sdk
# pip install qdrant-client python-dotenv

import os
from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import re
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Document
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import uuid

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

app = FastAPI()

#model call
model = SentenceTransformer('all-MiniLM-L6-v2')  # Load the pre-trained model for generating embeddings
openai_client = OpenAI(api_key=OPENAI_API_KEY)
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

# create collection
COLLECTION_NAME = "pdf_chunks"
collections = qdrant.get_collections()
existing = [
    c.name
    for c in collections.collections
]
if COLLECTION_NAME not in existing:
    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

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
        chunks.append(text[i:i+chunk_size])     # Append a chunk of text to the list of chunks
    return chunks

@app.get("/health")
def health_check():
    return {"Message": "Server is running"}

@app.post("/upload-pdf")        # Endpoint to handle PDF file uploads, extract text, clean it, chunk it, generate embeddings, and store the metadata and embeddings in memory. The endpoint returns the filename, saved path, character count of the cleaned text, a preview of the cleaned text, and the first chunk of text as a response.
async def upload_pdf(file: UploadFile = File(...)):

    # save pdf in upload folder
    path = os.path.join("upload", file.filename)
    with open(path, "wb") as f:     # Save the uploaded PDF file to the "upload" directory
        f.write(await file.read())  # async await is used to read the file content asynchronously, which allows the server to handle other requests while waiting for the file to be read

    pdf_reader = PdfReader(path)

    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    cleaned_text = clean_text(text)
    page_chunk = chunk(cleaned_text)
    embeddings = model.encode(page_chunk)  # Generate embeddings for each chunk of text, model.encode() is used to convert the chunks of text into numerical vectors that capture the semantic meaning of the text, which can be used for various NLP tasks such as similarity search, clustering, or classification.

    points = []
    for idx, (chunk, embedding) in enumerate(
        zip(page_chunk, embeddings)
    ):

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={
                    "filename":
                        file.filename,

                    "chunk_id":
                        idx,

                    "text":
                        chunk
                }
            )
        )

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

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