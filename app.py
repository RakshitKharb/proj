import streamlit as st
from utils.text_generation import generate_text_response
from utils.summarize_youtube import summarize_youtube_video
from utils.image_generation import generate_image_from_prompt
import logging

# Set up logging to the console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    st.title("Multimodal AI Application")

    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose the app mode",
                                    ["Home", "Text Summarization", "YouTube Summarization", "Image Generation"])

    if app_mode == "Home":
        st.markdown("""
        ## Welcome to the Multimodal AI Application
        Use the sidebar to navigate between different functionalities.
        """)

    elif app_mode == "Text Summarization":
        st.header("Text Summarization")
        text_input = st.text_area("Enter the text you want to summarize:", height=200)
        if st.button("Summarize"):
            if text_input:
                try:
                    summary = generate_text_response(text_input)
                    st.success("Summary:")
                    st.write(summary)
                    logging.info("Text summarization successful.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    logging.error(f"Text summarization error: {e}")
            else:
                st.warning("Please enter text to summarize.")

    elif app_mode == "YouTube Summarization":
        st.header("YouTube Video Summarization")
        youtube_url = st.text_input("Enter the YouTube video URL:")
        if st.button("Summarize Video"):
            if youtube_url:
                try:
                    summary = summarize_youtube_video(youtube_url)
                    st.success("Video Summary:")
                    st.write(summary)
                    logging.info("YouTube summarization successful.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    logging.error(f"YouTube summarization error: {e}")
            else:
                st.warning("Please enter a YouTube URL.")

    elif app_mode == "Image Generation":
        st.header("Image Generation")
        prompt = st.text_input("Enter the image prompt:")
        if st.button("Generate Image"):
            if prompt:
                try:
                    image = generate_image_from_prompt(prompt)
                    st.image(image, caption="Generated Image")
                    logging.info("Image generation successful.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    logging.error(f"Image generation error: {e}")
            else:
                st.warning("Please enter a prompt for image generation.")

if __name__ == "__main__":
    main()
