import streamlit as st
import requests
import io
import base64

def display_image(image_data):
    st.image(io.BytesIO(base64.b64decode(image_data)), use_column_width=True)

st.title("Titanic Dataset Chatbot 🚢")
user_input = st.text_input("Ask a question about the Titanic dataset:")

if st.button("Ask"): 
    response = requests.post("http://127.0.0.1:8000/query", json={"question": user_input}).json()
    
    if "answer" in response:
        st.write(response["answer"])
    elif "image" in response:
        display_image(response["image"]) 
