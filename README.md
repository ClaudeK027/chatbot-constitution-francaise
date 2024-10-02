# Chatbot Constitution Française

Ce projet implémente un chatbot basé sur la technique de Retrieval Augmented Generation (RAG) pour répondre aux questions sur la Constitution française. Il utilise une interface Streamlit pour une interaction conviviale.

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

## Installation

1. Clonez le dépôt :
   ```
   git clone https://github.com/votre-nom-utilisateur/chatbot-constitution-francaise.git
   cd chatbot-constitution-francaise
   ```

2. Créez un environnement virtuel :
   ```
   python -m venv chatbot_env
   ```

3. Activez l'environnement virtuel :
   - Sur Windows :
     ```
     chatbot_env\Scripts\activate
     ```
   - Sur macOS et Linux :
     ```
     source chatbot_env/bin/activate
     ```

4. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Assurez-vous que le fichier PDF de la Constitution française (`constitution.pdf`) est présent dans le répertoire du projet.

2. Assurez-vous d'avoir une installation locale d'Ollama avec les modèles Mistral et Phi-2 configurés.

## Utilisation

1. Lancez l'application Streamlit :
   ```
   streamlit run streamlit_app.py
   ```

2. Ouvrez votre navigateur et accédez à l'URL indiquée (généralement `http://localhost:8501`).

3. Utilisez l'interface pour poser vos questions sur la Constitution française.

## Structure du projet

- `streamlit_app.py` : Application principale Streamlit
- `pdf_processor.py` : Traitement du PDF de la Constitution
- `embedding_generator.py` : Génération et stockage des embeddings
- `semantic_search.py` : Recherche sémantique
- `llm_interface.py` : Interface avec les modèles de langage
- `main.py` : Script principal (utilisé pour le développement/test)

## L'interface 


## Dépannage

- Si vous rencontrez des problèmes avec l'API locale des modèles de langage, assurez-vous qu'Ollama est correctement installé et que les modèles sont disponibles.
- En cas d'erreur lors du chargement du PDF, vérifiez que le fichier `constitution.pdf` est présent et accessible.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

[Insérez ici les informations de licence]
