import streamlit as st
import openai
from dotenv import load_dotenv
load_dotenv()
import os


# Set your OpenAI API key
# openai.api_key = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI
st.title("Skin Disease Diagnosis Assistant")

# User input
user_input = st.text_input("Describe the patient's condition and symptoms:")
prompt = f"Describe the treatment options for {user_input}. Provide 3 examples, each within 150 words."
if st.button("Get Treatment Recommendations"):
    if prompt:
        # Create a list of message objects as per OpenAI's API requirements
        messages = [
            {"role": "system", "content": "You are a skin disease diagnosis doctor."},
            {"role": "user", "content": prompt}
        ]
        
        # Call the OpenAI API for chat completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Extract and display the assistant's response
        assistant_response = response['choices'][0]['message']['content']
        st.write("Skin Disease Diagnosis Doctor:", assistant_response)
    else:
        st.warning("Please describe the patient's condition and symptoms.")
