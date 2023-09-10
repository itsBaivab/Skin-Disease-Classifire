import streamlit as st
import openai
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build

load_dotenv()

# Set your OpenAI API key and YouTube API key
openai.api_key = os.getenv("OPENAI_API_KEY")
youtube_api_key = os.getenv("YOUTUBE_API_KEY")  # You need to set this environment variable

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

# Add YouTube video search functionality
st.write("\n")
st.header("Search for Disease Treatment Videos on YouTube")
disease_to_search = st.text_input("Enter the disease name to search for treatment videos on YouTube:")
if st.button("Search on YouTube"):
    if disease_to_search:
        # Initialize the YouTube Data API client
        youtube = build('youtube', 'v3', developerKey=youtube_api_key)

        # Perform the YouTube search
        search_response = youtube.search().list(
            q=f"{disease_to_search} treatment",
            part="id,snippet",
            type="video",
            maxResults=5  # You can adjust the number of results here
        ).execute()

        # Display the search results as clickable links
        st.write(f"Search results for '{disease_to_search} treatment' on YouTube:")
        for search_result in search_response.get("items", []):
            video_id = search_result["id"]["videoId"]
            video_title = search_result["snippet"]["title"]
            st.markdown(f"- [{video_title}](https://www.youtube.com/watch?v={video_id})")

        # Display video search results with thumbnails
        st.header("YouTube Video Search Results")

        for search_result in search_response.get("items", []):
            video_title = search_result["snippet"]["title"]
            video_description = search_result["snippet"]["description"]
            video_id = search_result["id"]["videoId"]
            video_thumbnail_url = search_result["snippet"]["thumbnails"]["medium"]["url"]  # Use "medium" format

            # Create a hyperlink around the thumbnail image
            video_link = f"[![{video_title}]({video_thumbnail_url})](https://www.youtube.com/watch?v={video_id})"
            st.markdown(video_link, unsafe_allow_html=True)
            st.write(f"Title: {video_title}")
            st.write(f"Description: {video_description}")
            st.write(f"Video ID: {video_id}")
    else:
        st.warning("Please enter a disease name to search for treatment videos on YouTube.")
