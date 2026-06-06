import os
from typing import List, Dict, Optional
from pathlib import Path

SAMPLE_DOCS = [
    {"id": "1", "title": "Getting Started with Python", "content": "Python is a high-level programming language known for its readability and simplicity. It supports multiple programming paradigms including procedural, object-oriented, and functional programming."},
    {"id": "2", "title": "Introduction to Machine Learning", "content": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. Common algorithms include linear regression, decision trees, and neural networks."},
    {"id": "3", "title": "Deep Learning with Transformers", "content": "Transformer architecture revolutionized natural language processing. Models like BERT and GPT use self-attention mechanisms to process sequential data efficiently. They excel at tasks like translation, summarization, and question answering."},
    {"id": "4", "title": "Vector Databases for RAG", "content": "Retrieval-Augmented Generation (RAG) combines retrieval systems with generative models. Vector databases like ChromaDB store embeddings and enable semantic search, making LLMs more accurate by grounding them in retrieved context."},
    {"id": "5", "title": "Building APIs with FastAPI", "content": "FastAPI is a modern Python web framework for building APIs. It provides automatic OpenAPI documentation, type validation with Pydantic, and async support out of the box. Ideal for high-performance AI services."},
    {"id": "6", "title": "Anomaly Detection Techniques", "content": "Anomaly detection identifies unusual patterns that deviate from expected behavior. Common approaches include Isolation Forest, One-Class SVM, and Autoencoders. Applications include fraud detection, network security, and system monitoring."},
    {"id": "7", "title": "NLP with spaCy and Transformers", "content": "spaCy is an industrial-strength NLP library. Combined with transformer models, it provides state-of-the-art results for tasks like named entity recognition, text classification, and dependency parsing."},
    {"id": "8", "title": "Production ML Workflows", "content": "MLOps practices ensure reliable deployment of machine learning models. Key components include version control for data and models, automated testing, CI/CD pipelines, monitoring, and retraining strategies."},
]


class RAGService:
    def __init__(self):
        self.documents = SAMPLE_DOCS
        self.embeddings = None
        self.collection = None
        self._initialized = False

    async def initialize(self):
        if self._initialized:
            return
        try:
            from sentence_transformers import SentenceTransformer
            import chromadb
            from chromadb.config import Settings as ChromaSettings
            self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
            chroma_client = chromadb.Client(ChromaSettings(anonymized_telemetry=False))
            self.collection = chroma_client.get_or_create_collection("portfolio_docs")
            existing = self.collection.count()
            if existing == 0:
                texts = [d["content"] for d in self.documents]
                ids = [d["id"] for d in self.documents]
                metadatas = [{"title": d["title"]} for d in self.documents]
                embeds = self.encoder.encode(texts).tolist()
                self.collection.add(ids=ids, embeddings=embeds, documents=texts, metadatas=metadatas)
            self._initialized = True
        except Exception as e:
            print(f"RAG init warning (running in demo mode): {e}")
            self._initialized = False

    async def retrieve(self, query: str, k: int = 3) -> List[Dict]:
        await self.initialize()
        if not self._initialized:
            results = []
            for doc in self.documents[:k]:
                results.append({"id": doc["id"], "title": doc["title"], "content": doc["content"], "score": 0.5})
            return results
        query_embedding = self.encoder.encode([query]).tolist()
        results = self.collection.query(query_embeddings=query_embedding, n_results=k)
        docs = []
        for i in range(len(results["ids"][0])):
            docs.append({
                "id": results["ids"][0][i],
                "title": results["metadatas"][0][i].get("title", ""),
                "content": results["documents"][0][i],
                "score": results["distances"][0][i] if results.get("distances") else 0,
            })
        return docs

    async def generate_response(self, query: str, context: List[Dict]) -> str:
        context_text = "\n\n".join([f"[{d['title']}]: {d['content']}" for d in context])
        prompt = f"""You are an AI assistant for a developer portfolio.
Use the following context to answer the question. Be concise and helpful.

Context:
{context_text}

Question: {query}

Answer:"""
        try:
            from openai import OpenAI
            client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
            response = client.chat.completions.create(
                model="mistral",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300,
            )
            return response.choices[0].message.content
        except Exception:
            return self._fallback_response(query, context)

    def _fallback_response(self, query: str, context: List[Dict]) -> str:
        rel_docs = [d["title"] for d in context]
        if not rel_docs:
            return "I couldn't find relevant information to answer your question. Try asking about Python, machine learning, or AI topics."
        return f"Based on my knowledge base, here's what I found:\n\nRelevant documents: {', '.join(rel_docs)}.\n\nI recommend reading these resources for a comprehensive answer about '{query}'. In production, this response would be generated by an LLM using the retrieved context."

    async def recommend(self, query: str, k: int = 5) -> List[Dict]:
        docs = await self.retrieve(query, k=k)
        return [{"title": d["title"], "content": d["content"][:200] + "...", "relevance": round(1 - d["score"], 3) if isinstance(d.get("score"), (int, float)) else 0.5} for d in docs]


rag_service = RAGService()
