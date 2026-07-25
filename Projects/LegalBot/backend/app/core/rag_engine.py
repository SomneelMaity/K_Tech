"""
Core RAG (Retrieval-Augmented Generation) Engine
"""
from typing import List, Dict, Any, Optional
from loguru import logger
import asyncio
from pathlib import Path

from app.core.config import settings


class RAGEngine:
    """
    Core RAG system for LegalBot
    Handles: Query → Retrieve → Generate → Cite
    """
    
    def __init__(self):
        self.initialized = False
        self.vector_store = None
        self.embedding_model = None
        self.llm_client = None
        self.loaded_segments = set()
        
    async def initialize(self):
        """Initialize the RAG engine components"""
        try:
            logger.info("Initializing RAG engine...")
            
            # Initialize embedding model
            await self._init_embeddings()
            
            # Initialize vector store
            await self._init_vector_store()
            
            # Initialize LLM client
            await self._init_llm()
            
            self.initialized = True
            logger.info("RAG engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG engine: {e}")
            raise
    
    async def _init_embeddings(self):
        """Initialize the embedding model"""
        from sentence_transformers import SentenceTransformer
        
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        logger.info("Embedding model loaded")
    
    async def _init_vector_store(self):
        """Initialize the vector database"""
        if settings.VECTOR_DB_TYPE == "faiss":
            from app.core.vector_stores.faiss_store import FAISSVectorStore
            self.vector_store = FAISSVectorStore()
        elif settings.VECTOR_DB_TYPE == "chroma":
            from app.core.vector_stores.chroma_store import ChromaVectorStore
            self.vector_store = ChromaVectorStore()
        else:
            raise ValueError(f"Unsupported vector DB type: {settings.VECTOR_DB_TYPE}")
        
        await self.vector_store.initialize()
        logger.info(f"Vector store initialized: {settings.VECTOR_DB_TYPE}")
    
    async def _init_llm(self):
        """Initialize the LLM client"""
        if settings.LLM_PROVIDER == "openai":
            from openai import AsyncOpenAI
            self.llm_client = AsyncOpenAI(
                api_key=settings.LLM_API_KEY,
                base_url=settings.LLM_API_BASE
            )
        elif settings.LLM_PROVIDER == "anthropic":
            from anthropic import AsyncAnthropic
            self.llm_client = AsyncAnthropic(api_key=settings.LLM_API_KEY)
        else:
            raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
        
        logger.info(f"LLM client initialized: {settings.LLM_PROVIDER}")
    
    async def load_segment(self, segment_id: str):
        """Load a specific segment's knowledge base"""
        if segment_id in self.loaded_segments:
            logger.info(f"Segment already loaded: {segment_id}")
            return
        
        kb_path = Path(f"knowledge-base/{segment_id}")
        if not kb_path.exists():
            logger.warning(f"Knowledge base not found for segment: {segment_id}")
            return
        
        logger.info(f"Loading segment: {segment_id}")
        await self.vector_store.load_segment(segment_id, kb_path)
        self.loaded_segments.add(segment_id)
        logger.info(f"Segment loaded: {segment_id}")
    
    async def load_all_segments(self):
        """Load all available segments"""
        segments = [
            "s1-consumer",
            "s2-property",
            "s3-family",
            "s4-cybercrime",
            "s5-employment",
            "s6-police",
            "s7-women-child",
            "s8-seniors",
            "s9-rti",
            "s10-msme"
        ]
        
        tasks = [self.load_segment(segment) for segment in segments]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def query(
        self,
        query_text: str,
        segment: Optional[str] = None,
        state: Optional[str] = None,
        top_k: int = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Main query method: Retrieve + Generate
        
        Args:
            query_text: User's question
            segment: Optional segment filter (s1-consumer, etc.)
            state: Optional state filter (for state-specific laws)
            top_k: Number of documents to retrieve
            
        Returns:
            Dict with answer, sources, citations
        """
        if not self.initialized:
            raise RuntimeError("RAG engine not initialized")
        
        top_k = top_k or settings.RAG_TOP_K
        
        # Step 1: Embed the query
        query_embedding = await self._embed_query(query_text)
        
        # Step 2: Retrieve relevant documents
        retrieved_docs = await self.vector_store.search(
            query_embedding=query_embedding,
            query_text=query_text,
            top_k=top_k,
            segment=segment,
            state=state,
            threshold=settings.RAG_SIMILARITY_THRESHOLD
        )
        
        if not retrieved_docs:
            return {
                "answer": "I don't have enough information to answer this question accurately. "
                         "Please consult a legal professional or contact NALSA/DLSA for free legal aid.",
                "sources": [],
                "confidence": "low"
            }
        
        # Step 3: Rerank if enabled
        if settings.RAG_RERANK:
            retrieved_docs = await self._rerank_documents(query_text, retrieved_docs)
        
        # Step 4: Generate answer with citations
        answer_data = await self._generate_answer(query_text, retrieved_docs, **kwargs)
        
        return answer_data
    
    async def _embed_query(self, query_text: str) -> List[float]:
        """Generate embedding for query text"""
        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        embedding = await loop.run_in_executor(
            None,
            self.embedding_model.encode,
            query_text
        )
        return embedding.tolist()
    
    async def _rerank_documents(
        self,
        query: str,
        documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Rerank retrieved documents using cross-encoder or LLM
        TODO: Implement actual reranking
        """
        # For now, return as-is (already sorted by similarity)
        return documents
    
    async def _generate_answer(
        self,
        query: str,
        context_docs: List[Dict[str, Any]],
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Generate answer using LLM with retrieved context
        """
        # Build context from retrieved documents
        context = self._build_context(context_docs)
        
        # Build prompt
        prompt = self._build_prompt(query, context, language)
        
        # Call LLM
        if settings.LLM_PROVIDER == "openai":
            response = await self.llm_client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(language)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS
            )
            answer = response.choices[0].message.content
        
        # Extract citations from context docs
        sources = [
            {
                "text": doc.get("content", ""),
                "metadata": doc.get("metadata", {}),
                "score": doc.get("score", 0.0)
            }
            for doc in context_docs[:3]  # Top 3 sources
        ]
        
        return {
            "answer": answer,
            "sources": sources,
            "confidence": self._calculate_confidence(context_docs),
            "disclaimer": self._get_disclaimer(language)
        }
    
    def _build_context(self, documents: List[Dict[str, Any]]) -> str:
        """Build context string from retrieved documents"""
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            metadata = doc.get("metadata", {})
            content = doc.get("content", "")
            
            source_info = f"[Source {i}]"
            if metadata.get("act"):
                source_info += f" {metadata['act']}"
            if metadata.get("section"):
                source_info += f", Section {metadata['section']}"
            if metadata.get("state"):
                source_info += f" ({metadata['state']})"
            
            context_parts.append(f"{source_info}\n{content}\n")
        
        return "\n\n".join(context_parts)
    
    def _build_prompt(self, query: str, context: str, language: str) -> str:
        """Build the prompt for LLM"""
        return f"""Answer the following legal question based ONLY on the provided context from Indian laws and verified sources.

Question: {query}

Context:
{context}

Guidelines:
1. Answer in simple, clear language (8th-grade reading level)
2. ALWAYS cite the specific law/section/act when mentioning it
3. If the context doesn't contain enough information, say "I don't have enough verified information"
4. NEVER fabricate section numbers, court names, or procedures
5. For state-specific matters, specify which state the information applies to
6. If emergency situation (violence, arrest, fraud), mention relevant helpline numbers
7. Format your answer with clear sections if appropriate

Answer:"""
    
    def _get_system_prompt(self, language: str) -> str:
        """Get system prompt for LLM"""
        return """You are LegalBot, an AI assistant providing general legal information about Indian law.

CRITICAL RULES:
- You provide INFORMATION, not legal advice (Advocates Act 1961)
- Only use information from the provided context
- NEVER invent section numbers, acts, or legal procedures
- Always cite your sources with [act name, section number]
- Use simple, clear language (8th-grade level)
- For emergencies, prioritize safety and helpline numbers
- Route complex matters to NALSA/DLSA/Tele-Law

Emergency Helplines:
- Cybercrime: 1930
- Women in distress: 181
- Child helpline: 1098
- Elder helpline: 14567
- Consumer: 1915

You must add a disclaimer: "This is general legal information, not legal advice. For your specific situation, consult a lawyer or contact NALSA/DLSA for free legal aid."
"""
    
    def _calculate_confidence(self, documents: List[Dict[str, Any]]) -> str:
        """Calculate confidence level based on retrieval scores"""
        if not documents:
            return "low"
        
        avg_score = sum(doc.get("score", 0) for doc in documents) / len(documents)
        
        if avg_score > 0.85:
            return "high"
        elif avg_score > 0.7:
            return "medium"
        else:
            return "low"
    
    def _get_disclaimer(self, language: str) -> str:
        """Get legal disclaimer"""
        disclaimers = {
            "en": "⚖️ This is general legal information, not legal advice. For your specific situation, consult a lawyer or contact NALSA/DLSA for free legal aid.",
            "hi": "⚖️ यह सामान्य कानूनी जानकारी है, कानूनी सलाह नहीं। अपनी विशिष्ट स्थिति के लिए, किसी वकील से परामर्श करें या निःशुल्क कानूनी सहायता के लिए NALSA/DLSA से संपर्क करें।"
        }
        return disclaimers.get(language, disclaimers["en"])
    
    async def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up RAG engine...")
        if self.vector_store:
            await self.vector_store.close()
        self.initialized = False
        logger.info("RAG engine cleanup complete")


# Global instance
rag_engine = RAGEngine()
