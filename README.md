# Chatbot Constitution Française

Ce projet implémente un chatbot basé sur la technique de Retrieval Augmented Generation (RAG) pour répondre aux questions sur la Constitution française. Il utilise une interface Streamlit pour une interaction conviviale.

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

## Installation

1. Clonez le dépôt :
   ```
   git clone https://github.com/ClaudeK027/chatbot-constitution-francaise
   cd chatbot-constitution-francaise
   ```

2. Créez un environnement virtuel :
   ```
   python -m venv chatbot_env
   ```

3. Activez l'environnement virtuel(optionnel) :
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
![image](https://github.com/user-attachments/assets/d771da9d-465c-409d-b8f3-0b16b4386167)
![image](https://github.com/user-attachments/assets/d4d0e5e0-8fc1-4e12-b769-d29bfd6970f3)
![image](https://github.com/user-attachments/assets/71e98322-b20e-4ee0-8ddb-5dfaee3b91c8)




## Dépannage

- Si vous rencontrez des problèmes avec l'installation de chromadb assurez vous d'avoir installé Desktop developpement with C++ via Visual Studio Build Tools
- Si vous rencontrez des problèmes avec l'API locale des modèles de langage, assurez-vous qu'Ollama est correctement installé et que les modèles sont disponibles.
- En cas d'erreur lors du chargement du PDF, vérifiez que le fichier `constitution.pdf` est présent et accessible.

## En savoir plus.

Pour en savoir plus consultez  les fichier `Explications.ipynb` qui explique en détails le fonctionnement de chaque script utilisés dans ce projet.


