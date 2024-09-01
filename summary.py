import streamlit as st
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Initialize summarization pipeline
summarizer = pipeline("summarization", model="t5-small")

# Helper function to extract text from a YouTube video transcript
def get_youtube_transcript(url):
    try:
        video_id = re.search(r"v=([a-zA-Z0-9_-]+)", url).group(1)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return ""

# Streamlit app layout
st.set_page_config(page_title="Summarify", layout="wide")
st.sidebar.image("path_to_your_logo.png", use_column_width=True)
st.sidebar.title("Summarify")
st.sidebar.subheader("Options")
option = st.sidebar.selectbox("Select an option:", ["YouTube Link Summarization"])

if option == "YouTube Link Summarization":
    st.title("YouTube Link Summarization")
    url = st.text_input("Enter the YouTube video URL:")
    if url:
        with st.spinner("Fetching transcript..."):
            transcript = get_youtube_transcript(url)
            if transcript:
                st.write("**Transcript:**")
                st.write(transcript)
                if st.button("Summarize"):
                    with st.spinner("Summarizing..."):
                        summary = summarizer(transcript, max_length=500, min_length=100, do_sample=False)
                        st.write("**Summary:**")
                        st.write(summary[0]['summary_text'])
