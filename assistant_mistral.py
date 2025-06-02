import os
import streamlit as st
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from huggingface_hub import login
login(token="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")


# Chargement des variables d'environnement
load_dotenv()


# Charger le modèle Mistral
# @st.cache_resource
# def load_llm():
#     model_name = "mistralai/Mistral-7B-Instruct-v0.1"
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelForCausalLM.from_pretrained(
#         model_name,
#         # device_map="auto",
#         # load_in_4bit=True  # Réduit la mémoire nécessaire
#     )
#     return pipeline(
#         "text-generation",
#         model=model,
#         tokenizer=tokenizer,
#         max_new_tokens=512
#     )

# Modifier juste la partie load_llm():
@st.cache_resource
def load_llm():
    model_name = "HuggingFaceH4/zephyr-7b-alpha"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype="auto"
    )
    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256
    )

llm = load_llm()

# Initialiser l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system",
         "content": "Tu es un assistant universitaire. Réponds aux questions sur les cours, examens et vie étudiante de manière concise."}
    ]


# Fonction pour générer une réponse
def generate_response(prompt):
    # Formater le prompt pour Mistral
    messages = st.session_state.messages.copy()
    messages.append({"role": "user", "content": prompt})

    # Créer le prompt formaté
    formatted_prompt = ""
    for msg in messages:
        if msg["role"] == "system":
            formatted_prompt += f"<s>[INST] {msg['content']} [/INST]"
        else:
            formatted_prompt += f"{msg['content']}</s>"

    # Génération
    response = llm(
        formatted_prompt,
        temperature=0.7,
        do_sample=True
    )[0]['generated_text']

    # Nettoyer la réponse
    response = response.replace(formatted_prompt, "").strip()
    st.session_state.messages.append({"role": "assistant", "content": response})
    return response


# Interface Streamlit
st.title("🤖 Assistant Universitaire (Mistral 7B)")

# Afficher l'historique
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