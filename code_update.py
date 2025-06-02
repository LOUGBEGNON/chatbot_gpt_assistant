import os
import openai
import streamlit as st
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Liste des contextes
contexts = {
    "Universitaire": "Tu es un assistant universitaire utile. Tu aides les étudiants avec leurs questions sur les cours, emplois du temps, examens et vie académique. Sois précis et concis.",
    "Professionnel": "Tu es un assistant professionnel. Tu aides les utilisateurs avec leurs questions sur le travail, la productivité, les entretiens, les outils bureautiques, etc.",
    "Vie personnelle": "Tu es un assistant personnel amical. Tu aides les utilisateurs à gérer leur quotidien, bien-être, relations et conseils de vie.",
    "Neutre": "Tu es un assistant intelligent et polyvalent qui répond à toute question de manière claire, utile et adaptée."
}

# Initialiser la sélection du domaine
if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = None
    st.session_state.initialized = False

# Sélection du domaine au démarrage
if not st.session_state.initialized:
    st.title("🤖 Assistant Polyvalent")
    domain = st.selectbox("Choisissez un domaine :", list(contexts.keys()))
    if st.button("Démarrer l'assistant"):
        st.session_state.selected_domain = domain
        st.session_state.messages = [
            {"role": "system", "content": contexts[domain]}
        ]
        st.session_state.initialized = True
        st.rerun()
    st.stop()  # Bloque l'exécution tant qu'on n'a pas choisi de domaine

# Interface principale après sélection
st.title(f"🤖 Assistant - {st.session_state.selected_domain}")

# Fonction pour générer une réponse
def generate_response(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
        temperature=0.7
    )
    response = completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": response})
    return response

# Affichage de l'historique
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Entrée utilisateur
prompt = st.chat_input("Posez votre question...")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = generate_response(prompt)
        st.markdown(response)
