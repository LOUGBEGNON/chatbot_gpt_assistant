import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
    model = AutoModelForCausalLM.from_pretrained(
        "mistralai/Mistral-7B-Instruct-v0.1",
        device_map="auto",
        # load_in_4bit=True  # Optimisation pour MacBook
    )
    return tokenizer, model

tokenizer, model = load_model()

user_input = st.text_input("Posez votre question universitaire")
if user_input:
    inputs = tokenizer(user_input, return_tensors="pt").to("mps")
    outputs = model.generate(**inputs, max_new_tokens=200)
    st.write(tokenizer.decode(outputs[0], skip_special_tokens=True))