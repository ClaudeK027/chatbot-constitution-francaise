from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os

class SemanticSearch:
    def __init__(self, model_name='BAAI/bge-large-en-v1.5'):
        self.model = SentenceTransformer(model_name)
        self.persist_directory = os.path.join(os.getcwd(), "chroma_db")
        self.chroma_client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.chroma_client.get_collection("document_embeddings")

    def search(self, query, n_results=5):
        # Générer l'embedding pour la requête
        query_embedding = self.model.encode(query).tolist()

        # Effectuer la recherche dans ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )

        # Formater les résultats
        formatted_results = []
        for doc, metadata, distance in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
            formatted_results.append({
                'content': doc,
                'metadata': metadata,
                'relevance_score': 1 - distance  # Convertir la distance en score de pertinence
            })

        return formatted_results

    def get_relevant_context(self, query, max_length=1000):
        results = self.search(query)
        context = ""
        for result in results:
            if len(context) + len(result['content']) <= max_length:
                context += result['content'] + " "
            else:
                break
        return context.strip()

