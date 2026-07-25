"""
FAISS Vector Store Implementation
"""
from typing import List, Dict, Any, Optional
import faiss
import numpy as np
import pickle
from pathlib import Path
from loguru import logger

from app.core.config import settings


class FAISSVectorStore:
    """
    FAISS-based vector store for semantic search
    """
    
    def __init__(self):
        self.index = None
        self.documents = []  # Store metadata alongside vectors
        self.dimension = settings.EMBEDDING_DIMENSION
        self.segment_indices = {}  # Separate indices per segment
    
    async def initialize(self):
        """Initialize FAISS index"""
        logger.info("Initializing FAISS vector store...")
        
        # Create directory if it doesn't exist
        vector_path = Path(settings.VECTOR_DB_PATH)
        vector_path.mkdir(parents=True, exist_ok=True)
        
        # Try to load existing index
        index_path = vector_path / "faiss.index"
        docs_path = vector_path / "documents.pkl"
        
        if index_path.exists() and docs_path.exists():
            logger.info("Loading existing FAISS index...")
            self.index = faiss.read_index(str(index_path))
            with open(docs_path, "rb") as f:
                self.documents = pickle.load(f)
            logger.info(f"Loaded {self.index.ntotal} vectors from existing index")
        else:
            logger.info("Creating new FAISS index...")
            # Create flat L2 index (can upgrade to IVF for large datasets)
            self.index = faiss.IndexFlatL2(self.dimension)
            self.documents = []
        
        logger.info("FAISS vector store initialized")
    
    async def load_segment(self, segment_id: str, kb_path: Path):
        """
        Load a segment's knowledge base
        
        Expected structure:
        kb_path/
          entries.jsonl  (one JSON object per line)
        """
        entries_file = kb_path / "entries.jsonl"
        
        if not entries_file.exists():
            logger.warning(f"No entries file found for {segment_id}: {entries_file}")
            return
        
        logger.info(f"Loading knowledge entries from {entries_file}")
        
        # This is a placeholder - actual implementation would:
        # 1. Read entries from JSONL
        # 2. Generate embeddings
        # 3. Add to FAISS index
        # 4. Store metadata
        
        # For now, just log
        logger.info(f"Segment {segment_id} loaded (placeholder)")
    
    async def add_documents(
        self,
        embeddings: np.ndarray,
        documents: List[Dict[str, Any]]
    ):
        """
        Add documents with their embeddings to the index
        
        Args:
            embeddings: numpy array of shape (n_docs, dimension)
            documents: list of document metadata dicts
        """
        if embeddings.shape[0] != len(documents):
            raise ValueError("Number of embeddings must match number of documents")
        
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Embedding dimension {embeddings.shape[1]} doesn't match {self.dimension}")
        
        # Add to FAISS index
        start_idx = self.index.ntotal
        self.index.add(embeddings.astype('float32'))
        
        # Add metadata
        for i, doc in enumerate(documents):
            doc['_index'] = start_idx + i
            self.documents.append(doc)
        
        logger.info(f"Added {len(documents)} documents. Total: {self.index.ntotal}")
    
    async def search(
        self,
        query_embedding: List[float],
        query_text: str,
        top_k: int = 5,
        segment: Optional[str] = None,
        state: Optional[str] = None,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant documents
        
        Args:
            query_embedding: Query vector
            query_text: Original query text (for hybrid search)
            top_k: Number of results to return
            segment: Optional segment filter
            state: Optional state filter
            threshold: Minimum similarity threshold
            
        Returns:
            List of documents with scores
        """
        if self.index.ntotal == 0:
            logger.warning("FAISS index is empty")
            return []
        
        # Convert to numpy array
        query_vector = np.array([query_embedding], dtype='float32')
        
        # Search in FAISS (returns L2 distances)
        # Note: FAISS returns distances, not similarities
        # For cosine similarity, we'd need to normalize vectors
        k = min(top_k * 3, self.index.ntotal)  # Retrieve more for filtering
        distances, indices = self.index.search(query_vector, k)
        
        # Convert L2 distances to similarity scores (0-1 range)
        # similarity = 1 / (1 + distance)
        similarities = 1 / (1 + distances[0])
        
        # Retrieve documents with filtering
        results = []
        for idx, score in zip(indices[0], similarities):
            if idx == -1:  # FAISS returns -1 for missing results
                continue
            
            if score < threshold:
                continue
            
            doc = self.documents[idx].copy()
            metadata = doc.get('metadata', {})
            
            # Apply filters
            if segment and metadata.get('segment') != segment:
                continue
            
            if state and metadata.get('state') and metadata['state'] != state:
                continue
            
            doc['score'] = float(score)
            results.append(doc)
            
            if len(results) >= top_k:
                break
        
        logger.info(f"Found {len(results)} results for query")
        return results
    
    async def save(self):
        """Save index and documents to disk"""
        vector_path = Path(settings.VECTOR_DB_PATH)
        vector_path.mkdir(parents=True, exist_ok=True)
        
        index_path = vector_path / "faiss.index"
        docs_path = vector_path / "documents.pkl"
        
        faiss.write_index(self.index, str(index_path))
        with open(docs_path, "wb") as f:
            pickle.dump(self.documents, f)
        
        logger.info(f"Saved FAISS index with {self.index.ntotal} vectors")
    
    async def close(self):
        """Save and cleanup"""
        await self.save()
        logger.info("FAISS vector store closed")
