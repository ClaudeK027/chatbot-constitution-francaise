from pdf_processor import PDFProcessor
from embedding_generator import EmbeddingGenerator
from semantic_search import SemanticSearch
from llm_interface import LLMInterface
import os

def format_context(results):
    context = ""
    for i, result in enumerate(results[:3], 1):  # Utiliser les 3 premiers résultats
        context += f"Extrait {i}:\n"
        context += f"Titre: {result['metadata']['title']}\n"
        context += f"Article: {result['metadata']['article_num']}\n"
        context += f"Contenu: {result['content']}\n\n"
    return context.strip()

def main():
    pdf_path = "constitution.pdf"
    
    '''# Traitement du PDF (si ce n'est pas déjà fait)
    processor = PDFProcessor(pdf_path)
    chunks = processor.process()

    # Génération et stockage des embeddings (si ce n'est pas déjà fait)
    embedding_gen = EmbeddingGenerator()
    embedding_gen.process_and_store(chunks)'''

    # Création des objets de recherche sémantique et d'interface LLM
    searcher = SemanticSearch()
    llm = LLMInterface()

    print("Chatbot de la Constitution française")
    print("-----------------------------------")
    print("Posez vos questions sur la Constitution française. Tapez 'q' pour quitter.")

    while True:
        query = input("\nVotre question : ")
        if query.lower() == 'q':
            break

        # Recherche sémantique
        results = searcher.search(query, n_results=3)  # Récupérer les 3 meilleurs résultats

        # Formater le contexte pour le LLM
        context = format_context(results)

        # Préparer le prompt pour le LLM
        prompt = f"""En tant qu'expert en droit constitutionnel français, veuillez répondre à la question suivante en vous basant uniquement sur les extraits fournis de la Constitution française. Si les extraits ne contiennent pas suffisamment d'informations pour répondre à la question, indiquez-le clairement.

Extraits de la Constitution :
{context}

Question : {query}

Réponse :"""

        # Générer la réponse avec le LLM
        response = llm.generate_response(prompt)

        print("\nRéponse du chatbot :")
        print(response)

        # Afficher les sources utilisées
        print("\nSources utilisées :")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['metadata']['title']} - Article {result['metadata']['article_num']}")

if __name__ == "__main__":
    main()