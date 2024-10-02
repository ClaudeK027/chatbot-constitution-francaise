from sentence_transformers import SentenceTransformer
import chromadb
import os
import numpy as np
from typing import List, Dict
from sklearn.preprocessing import normalize

class EmbeddingGenerator:
    def __init__(self, model_name='BAAI/bge-large-en-v1.5'):
        self.model = SentenceTransformer(model_name)
        self.persist_directory = os.path.join(os.getcwd(), "chroma_db")
        self.chroma_client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.chroma_client.get_or_create_collection("document_embeddings")

    def generate_embeddings(self, chunks: List[Dict]):
        texts = [chunk.page_content for chunk in chunks]
        
        # Générer des embeddings avec SentenceTransformer
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Normalisation L2 des embeddings
        embeddings = normalize(embeddings)
        
        return embeddings

    def store_embeddings(self, chunks: List[Dict], embeddings: np.ndarray):
        ids = [str(i) for i in range(len(chunks))]
        metadatas = [
            {
                "source": chunk.metadata.get('source', ''),
                "title": chunk.metadata.get('title', ''),
                "article_num": chunk.metadata.get('article_num', '')
            } 
            for chunk in chunks
        ]
        texts = [chunk.page_content for chunk in chunks]
        
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

    def process_and_store(self, chunks: List[Dict]):
        embeddings = self.generate_embeddings(chunks)
        self.store_embeddings(chunks, embeddings)
        print(f"Generated and stored embeddings for {len(chunks)} chunks.")

    def get_collection_info(self):
        return {
            "name": self.collection.name,
            "count": self.collection.count()
        }

    def get_similar_chunks(self, query: str, n_results: int = 5):
        query_embedding = self.generate_embeddings([{"page_content": query}])
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        return results

    def update_embeddings(self, chunks: List[Dict]):
        """Mise à jour des embeddings pour les chunks existants."""
        embeddings = self.generate_embeddings(chunks)
        ids = [str(i) for i in range(len(chunks))]
        self.collection.update(
            ids=ids,
            embeddings=embeddings.tolist(),
            metadatas=[chunk.metadata for chunk in chunks],
            documents=[chunk.page_content for chunk in chunks]
        )
        print(f"Updated embeddings for {len(chunks)} chunks.")