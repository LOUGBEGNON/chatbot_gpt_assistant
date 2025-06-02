import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Charger la clé API depuis .env
load_dotenv()
API_TOKEN = os.getenv("HF_API_TOKEN")

# Configuration de l'API
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


# Interface Streamlit
st.title("🤖 Assistant Universitaire (Mistral 7B via API)")

# Historique de conversation
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system",
         "content": "Tu es un assistant universitaire spécialisé dans les questions académiques. Réponds en français de manière concise et précise."}
    ]

# Afficher l'historique
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Gestion de la conversation
if prompt := st.chat_input("Posez votre question..."):
    # Ajout du message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    # Préparation du prompt pour Mistral
    conversation = [f"<s>[INST] {msg['content']} [/INST]" if msg['role'] == 'system' else msg['content']
                    for msg in st.session_state.messages]
    full_prompt = "\n".join(conversation)

    # Appel à l'API
    with st.spinner("L'assistant réfléchit..."):
        try:
            output = query({
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": 300,
                    "temperature": 0.7,
                    "do_sample": True
                }
            })

            # Extraction de la réponse
            if isinstance(output, list):
                response = output[0]['generated_text'].replace(full_prompt, "").strip()
            else:
                response = output['generated_text'].replace(full_prompt, "").strip()

            # Affichage
            with st.chat_message("assistant"):
                st.write(response)

            # Mise à jour de l'historique
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"Erreur lors de l'appel à l'API: {str(e)}")