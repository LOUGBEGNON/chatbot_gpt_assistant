import os
import openai
import streamlit as st
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configurer OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialiser l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system",
         "content": "Tu es un assistant universitaire utile. Tu aides les étudiants avec leurs questions sur les cours, emplois du temps, examens et vie académique. Sois précis et concis."}
    ]


# Fonction pour générer une réponse avec OpenAI
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


# Interface Streamlit
st.title("🤖 Assistant Universitaire")

# Afficher l'historique du chat
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Entrée utilisateur
prompt = st.chat_input("Posez votre question sur la vie universitaire...")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = generate_response(prompt)
        st.markdown(response)