import streamlit as st
from llm_interface import LLMInterface, m1, m2
from semantic_search import SemanticSearch
import base64
import time

def get_base64_avatar(text, bg_color):
    from PIL import Image, ImageDraw, ImageFont
    import io

    # Créer une image
    img = Image.new('RGB', (100, 100), color=bg_color)
    d = ImageDraw.Draw(img)
    # Utiliser une police plus grande
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()
    
    # Obtenir la boîte englobante du texte
    left, top, right, bottom = d.textbbox((0, 0), text, font=font)
    text_width = right - left
    text_height = bottom - top
    
    # Centrer le texte
    position = ((100 - text_width) / 2, (100 - text_height) / 2)
    d.text(position, text, fill="white", font=font)
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"

def main():
    st.set_page_config(page_title="Chatbot Constitution Française", layout="wide")
    
    st.markdown("""
    <style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #2C2C2C;
        color: white;
    }
    @keyframes pulse {
        0% { opacity: 0.5; }
        50% { opacity: 1; }
        100% { opacity: 0.5; }
    }
    .loading {
        animation: pulse 1s infinite ease-in-out;
    }
    </style>
    """, unsafe_allow_html=True)

    searcher = SemanticSearch()

    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = m2

    def reset_conversation():
        st.session_state.messages = []

    with st.sidebar:
        st.title("Configuration")
        new_model = st.selectbox("Choisissez le modèle", [m1, m2], 
                                 index=[m1, m2].index(st.session_state.selected_model))
        if new_model != st.session_state.selected_model:
            st.session_state.selected_model = new_model
            reset_conversation()
            st.rerun()

    llm = LLMInterface(model_name=st.session_state.selected_model)

    st.title("Chatbot Constitution Française")

    user_avatar = get_base64_avatar("U", "#3498db")
    m_avatar = get_base64_avatar("M", "#e74c3c")
    p_avatar = get_base64_avatar("P", "#9b59b6")

    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar=user_avatar):
                st.markdown(message["content"])
        else:
            avatar = m_avatar if st.session_state.selected_model == m1 else p_avatar
            with st.chat_message("assistant", avatar=avatar):
                st.markdown(message["content"])

    if prompt := st.chat_input("Posez votre question sur la Constitution française"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=user_avatar):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=m_avatar if st.session_state.selected_model == m1 else p_avatar):
            message_placeholder = st.empty()
            
            # Animation de chargement
            for i in range(3):
                message_placeholder.markdown(f"<p class='loading'>Recherche en cours{'.' * (i+1)}</p>", unsafe_allow_html=True)
                time.sleep(0.5)

            try:
                results = searcher.search(prompt, n_results=3)
                context = "\n\n".join([f"Extrait {i+1}:\nTitre: {r['metadata']['title']}\nArticle: {r['metadata']['article_num']}\nContenu: {r['content']}" for i, r in enumerate(results)])
                
                full_prompt = f"""En tant qu'expert en droit constitutionnel français, veuillez répondre à la question suivante en vous basant uniquement sur les extraits fournis de la Constitution française. Si les extraits ne contiennent pas suffisamment d'informations pour répondre à la question, indiquez-le clairement.

Extraits de la Constitution :
{context}

Question : {prompt}

Réponse :"""

                response = llm.generate_response(full_prompt)
                message_placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

                with st.expander("Sources utilisées"):
                    for i, result in enumerate(results, 1):
                        st.write(f"{i}. {result['metadata']['title']} - Article {result['metadata']['article_num']}")

            except Exception as e:
                error_message = f"Une erreur s'est produite : {str(e)}"
                message_placeholder.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

    st.markdown("---")
    st.caption("Ce chatbot utilise l'IA pour interpréter la Constitution française. Vérifiez les informations importantes.")

    if st.button("Réinitialiser la conversation"):
        reset_conversation()
        st.rerun()

if __name__ == "__main__":
    main()